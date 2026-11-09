#!/usr/bin/env python3
"""
Run your five criteria three times each.  <- UNIT 8, MILESTONE 3

    python app.py                              # in one terminal
    python run_eval.py --label before          # in another
    python run_eval.py --label after

The attack set tests what staff thought to test. This tests what *you* thought
to test, and the two rarely overlap much. Both count.

Fill in `scenarios.py` first — that's where you say what each criterion needs
run against it. A criterion about false positives needs your own writing. One
about label coverage needs inputs across the score range.

!! Three trials, and **your first signal runs a model, so identical input can
score differently twice.** That's exactly why repeats matter here.

This does the sending and the recording. It does not decide whether a trial
passed — that depends on the criterion you wrote, so the Verdict column comes
back blank.
"""

import argparse
import datetime as dt
import json
import sys
import uuid
from pathlib import Path

import config

# Windows consoles often run a codepage that can't print every character in
# this file's help text. Without this, `--help` ends in a UnicodeEncodeError
# traceback instead of the help — which is a miserable first thing to hit.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(errors="replace")
    except (AttributeError, ValueError):  # not a normal text stream
        pass


DEFAULT_URL = f"http://{config.HOST}:{config.PORT}"


def bodies_for(scenario):
    """
    The request bodies one scenario sends.

    A "texts" scenario gets a creator_id made up for it. A "bodies" scenario is
    sent exactly as written, which is how a bad-input criterion says things a
    string can't — no `text` field, a null, something enormous.
    """
    if scenario.get("bodies"):
        return list(scenario["bodies"])
    return [
        {"text": text, "creator_id": f"eval_{scenario['name'][:12]}_{i}"}
        for i, text in enumerate(scenario["texts"], 1)
    ]


APPEAL_REASONING = "Eval appeal: checking the appeal path records this. The wording doesn't matter."


def run_appeal_trial(requests, args, scenario, trial):
    """
    One trial of an "appeal" scenario. Sending text to /submit can't test the
    appeal path, so this:

      1. submits each text with its own creator_id and appeals the content_id
         that comes back                                         -> expect 200
      2. appeals the first of those again                        -> expect 409
      3. appeals a content_id that was never issued              -> expect 404

    and then reads /log to check each one left the right trace. Returns one
    result per request, each with `passed` and a list of `problems`.
    """
    def post(route, body):
        response = requests.post(f"{args.url}{route}", json=body, timeout=args.timeout)
        return response.status_code, (response.json() if response.content else {})

    results = []

    # 1. Submit, then appeal what came back — whatever the label was.
    for i, text in enumerate(scenario["texts"], 1):
        creator_id = f"eval_appeal_t{trial}_{i}"
        result = {"step": "appeal", "expected": 200, "status": None,
                  "creator_id": creator_id, "content_id": None, "problems": []}
        try:
            status, payload = post("/submit", {"text": text, "creator_id": creator_id})
            result["content_id"] = payload.get("content_id")
            if status != 200 or not result["content_id"]:
                result["problems"].append(f"/submit returned {status} with no content_id")
            else:
                result["status"], _ = post("/appeal", {"content_id": result["content_id"],
                                                      "reasoning": APPEAL_REASONING})
        except Exception as exc:  # noqa: BLE001
            result["problems"].append(f"{type(exc).__name__}: {exc}")
        results.append(result)

    # 2. A repeat appeal on something already under_review.
    appealed = [r for r in results if r["status"] == 200]
    repeat = {"step": "repeat appeal", "expected": 409, "status": None,
              "content_id": appealed[0]["content_id"] if appealed else None, "problems": []}
    if not appealed:
        repeat["problems"].append("no appeal succeeded, so there was nothing to repeat")
    else:
        try:
            repeat["status"], _ = post("/appeal", {"content_id": repeat["content_id"],
                                                  "reasoning": APPEAL_REASONING})
        except Exception as exc:  # noqa: BLE001
            repeat["problems"].append(f"{type(exc).__name__}: {exc}")
    results.append(repeat)

    # 3. A content_id that was never issued. Fresh each time so its log entry
    #    can't be confused with an earlier run's.
    unknown = {"step": "unknown content_id", "expected": 404, "status": None,
               "content_id": f"c_eval_unknown_{uuid.uuid4().hex[:8]}", "problems": []}
    try:
        unknown["status"], payload = post("/appeal", {"content_id": unknown["content_id"],
                                                     "reasoning": APPEAL_REASONING})
        if unknown["content_id"] not in json.dumps(payload):
            unknown["problems"].append("404 response doesn't name the content_id")
    except Exception as exc:  # noqa: BLE001
        unknown["problems"].append(f"{type(exc).__name__}: {exc}")
    results.append(unknown)

    # Check every result against the audit log.
    try:
        entries = requests.get(f"{args.url}/log", timeout=args.timeout).json()["entries"]
    except Exception as exc:  # noqa: BLE001
        entries = []
        for result in results:
            result["problems"].append(f"couldn't read /log: {type(exc).__name__}: {exc}")

    def logged(content_id, event):
        return [e for e in entries if e.get("content_id") == content_id and e.get("event") == event]

    for result in results:
        if result["status"] is not None and result["status"] != result["expected"]:
            result["problems"].append(f"got {result['status']}, expected {result['expected']}")
        cid = result["content_id"]
        if not cid:
            continue

        appeals = logged(cid, "appeal")
        if result["step"] == "appeal":
            if len(appeals) != 1:
                result["problems"].append(f"{len(appeals)} appeal entries in the log, expected 1")
            for entry in appeals:
                expected = {"status": "under_review", "creator_id": result["creator_id"],
                            "reasoning": APPEAL_REASONING}
                for field, value in expected.items():
                    if entry.get(field) != value:
                        result["problems"].append(f"log {field} is {entry.get(field)!r}, expected {value!r}")
                if not entry.get("timestamp"):
                    result["problems"].append("log entry has no timestamp")
        else:
            # A refused appeal leaves a rejection and no new appeal entry.
            if not logged(cid, "rejected"):
                result["problems"].append("no event: \"rejected\" entry in the log")
            if len(appeals) != (1 if result["step"] == "repeat appeal" else 0):
                result["problems"].append(f"{len(appeals)} appeal entries in the log after refusal")

    for result in results:
        result["passed"] = not result["problems"]
    return results


def describe(body):
    """A short, readable note of what was sent — for the report."""
    if set(body) == {"text", "creator_id"} and isinstance(body.get("text"), str):
        text = body["text"]
        return text[:70] if text else "(empty text)"
    return json.dumps(body)[:120]


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--label", default="")
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--timeout", type=float, default=90.0)
    args = parser.parse_args()

    try:
        import requests
    except ImportError:
        print("The `requests` package isn't installed.\n"
              "Run: pip install -r requirements.txt", file=sys.stderr)
        sys.exit(1)

    try:
        import scenarios
    except ImportError:
        print("No scenarios.py found. Milestone 3 starts by filling it in.",
              file=sys.stderr)
        sys.exit(1)

    problems = scenarios.validate()
    if problems:
        print("scenarios.py has problems:\n", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        sys.exit(1)

    try:
        requests.get(f"{args.url}/health", timeout=5)
    except Exception:  # noqa: BLE001
        print(f"Nothing answering at {args.url}. Start it:  python app.py",
              file=sys.stderr)
        sys.exit(1)

    if args.trials < 3:
        print(f"!! {args.trials} trial(s). The submission asks for three.\n")

    rows = []
    for scenario in scenarios.SCENARIOS:
        print(f"\n{scenario['name']}  (criterion {scenario.get('criterion') or '—'})")

        trials = []
        for trial in range(1, args.trials + 1):
            if scenario.get("appeal"):
                results = run_appeal_trial(requests, args, scenario, trial)
                trials.append(results)
                passed = sum(r["passed"] for r in results)
                failed = [r["step"] for r in results if not r["passed"]]
                print(f"  trial {trial}: {passed}/{len(results)} checks passed"
                      + (f" (failed: {', '.join(failed)})" if failed else ""))
                continue

            results = []
            for i, body in enumerate(bodies_for(scenario), 1):
                preview = describe(body)
                try:
                    response = requests.post(f"{args.url}/submit", json=body,
                                             timeout=args.timeout)
                    payload = response.json() if response.content else {}
                    results.append({
                        "status": response.status_code,
                        "content_id": payload.get("content_id"),
                        "guess": payload.get("guess"),
                        "confidence": payload.get("confidence"),
                        "combined_score": payload.get("combined_score"),
                        "model_score": payload.get("model_score"),
                        "style_score": payload.get("style_score"),
                        "label": payload.get("label"),
                        "warnings": payload.get("warnings"),
                        # Only set on a refused request (a 4xx).
                        "error": payload.get("error"),
                        "reason": payload.get("reason"),
                        "message": payload.get("message"),
                        "sent": preview,
                    })
                except Exception as exc:  # noqa: BLE001
                    results.append({"status": None, "error": f"{type(exc).__name__}: {exc}",
                                    "sent": preview})

            trials.append(results)
            # A refused request has no guess, so show its status code instead.
            guesses = [r.get("guess") or str(r.get("status") or "—") for r in results]
            print(f"  trial {trial}: {', '.join(guesses)}")

        rows.append({"scenario": scenario, "trials": trials})

    write_report(rows, args)


def write_report(rows, args):
    config.RESULTS_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    label = f"_{args.label}" if args.label else ""
    path = config.RESULTS_DIR / f"run_{stamp}{label}.md"

    n = args.trials
    headers = " | ".join(f"Run {i}" for i in range(1, n + 1))
    divider = "|".join(["---"] * n)

    lines = [
        f"# Run log{f' — {args.label}' if args.label else ''}",
        "",
        "- Produced by: `run_eval.py::main`",
        "- Service: `app.py::submit` · scoring: `scoring.py::combine_signals`",
        f"- {n} trials per criterion · {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "Fill in Target from `criteria.md`, and Run and Verdict from the output",
        "underneath. Whether a trial passed depends on the criterion you wrote.",
        "",
        f"| Criterion | Target | {headers} | Verdict |",
        f"|---|---|{divider}|---|",
    ]

    for row in rows:
        scenario = row["scenario"]
        number = scenario.get("criterion")
        name = f"{number}. {scenario['name']}" if number else scenario["name"]
        lines.append(f"| {name} |  | {' | '.join([' '] * n)} |  |")

    lines += ["", "---", "", "## What actually came back", "",
              "Real output. Paste the relevant parts into your README — the rubric",
              "asks for the actual JSON, not a description of it.", ""]

    for row in rows:
        scenario = row["scenario"]
        lines += [f"### {scenario['name']}", ""]
        for trial_number, results in enumerate(row["trials"], 1):
            lines += [f"**Trial {trial_number}**", "", "```json",
                      json.dumps(results, indent=2), "```", ""]

    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {path.relative_to(config.ROOT)}")
    print("Commit it. It's the evidence the test actually happened.")


if __name__ == "__main__":
    main()
