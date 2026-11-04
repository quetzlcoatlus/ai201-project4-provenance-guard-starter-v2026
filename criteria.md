# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1.

<!-- Your criterion. It must name a number. -->
Of 5 pieces (my 3 borderline texts, which are my writing partly edited with AI, and 2 pieces
written entirely by me), 0 come back with `guess: "ai"` (combined score ≥ `AI_THRESHOLD`), in each of 3 trials. An `unsure` result does not count as a false positive.


**Why this target:**

False positives are expensive for the platform's brand PR and potential profit (due to loss of a client), so we want to minimize the chances of false positives even at the cost of false negatives. The high-confidence AI label should only appear when the service is extremely certain; sending a writer to `unsure` is acceptable, accusing them is not.

---

## 2.

<!-- Your criterion. -->
5 of 5 first appeals, in each of 3 trials, sent as a POST to `/appeal` with `content_id` and
`reasoning` against a `content_id` that `/submit` returned, each add one new entry to
`logs/audit.jsonl` with `event: "appeal"`, `status: "under_review"`, a timestamp, the
`content_id`, the original submission's `creator_id`, and the `reasoning`. In the same trials, an
appeal on an unknown `content_id` gets a 404 naming that `content_id`, and a second appeal on a
`content_id` already `under_review` gets a 409 and adds no appeal entry. Every 404 and 409 writes
an `event: "rejected"` entry to the audit log.


**Why this target:**

An appeal that isn't seen causes PR damage and is required for someone to reconstruct what happened post-hoc. Therefore, appeals are recorded without fail. The path doesn't run a model, so in theory it is fully deterministic and anything less than 5 of 5 is a bug, not noise.

---

## 3.

<!-- Your criterion. -->
All 9 pre-labelled inputs (3 AI, 3 borderline, 3 human) reach their intended label in each of 3 trials: text I labelled AI gets high-confidence AI, text I labelled borderline gets unsure, and text I labelled human gets high-confidence human.


**Why this target:**

The thresholds are constants I set by hand, not something learned from data. If the combining rule squeezes scores into a narrow range, a label can end up unreachable, and the service quietly becomes a two-label (or one-label) system. Requiring each label to be reached *by the input meant for it* also rules out a pass where all three labels appear but on the wrong texts.

---

## 4.

<!-- Your criterion. -->
Across 3 pre-labelled clearly-AI and 3 pre-labelled clearly-human samples, the lowest clearly-AI
combined score is at least 0.3 above the highest clearly-human combined score, in each of 3 trials.


**Why this target:**

0.3 is the width of my unsure band (0.35–0.65). If the two groups' closest pair is at least that far apart, the two groups can sit on opposite sides of the band rather than both crowding into it. Measuring the closest pair, not the averages, means a single badly-scored sample can't hide behind the others. A gap any narrower would mean small run-to-run changes in the model signal could push clear cases across a threshold.

---

## 5.

<!-- Your criterion. -->
In each of 3 trials, every request where `text` is missing, `null`, empty (including whitespace-only), or not a string gets a 400 with a JSON body naming the problem, and never a 500. Every request whose `text` is over 400 tokens is still scored, and its response includes a `warnings` entry saying only the first 400 tokens were analyzed.


**Why this target:**

We need error handling for missing or empty because there's no difference between human and AI written content in that context. A 400 tells the caller the mistake is in their request, not the service. Long texts aren't wrong, so they shouldn't be rejected, but the model signal only reads the first 400 tokens, so the writer deserves to know that part of their work wasn't looked at.

> **Note:** there's no hard cap on request size yet. The model signal is bounded by truncation,
> but the style signal and the request itself aren't, so a multi-megabyte body is still accepted.
> A cap (e.g. a 413 via Flask's `MAX_CONTENT_LENGTH`) is out of scope for this criterion.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
