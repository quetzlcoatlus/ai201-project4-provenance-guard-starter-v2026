# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

A submission goes to the /submit route as a POST and requires a "creator_id" and a "text" attribute. "text" contains the text to analyze and "creator_id" is just the id of the submission's creator. This is 

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** Perplexity. Essentially, how predictable a piece of text is.

**Why that might differ between human and AI writing:** Text written by an AI is statistically determined. Next token of text is predicted from the previous. So we expect AI written text to be highly "predictable" with that constraint.

**What it can't see:** It can't guarantee falsify authorship. It can false positive on people who write with strict grammar, or someone that is less familiar with the language (young or used to another language). It also false negatives on ornate prose that contains rare words.

### Signal two — the style signal

**What it measures:** The shape of text and not single word predictability. Includes several metrics:
- sentence_length_spread, the standard deviation of sentence length (in words) divided by the mean. Higher means more human. Counted in the style score.
- type_token_ratio, unique words divided by total words, averaged over sliding 50-word windows (MATTR) so long and short texts are comparable. Higher means more varied vocabulary. **Computed but weighted 0:** on my samples it ran the opposite way from the expected direction (the AI sample had the *higher* ratio, 0.915 vs 0.808), and counting it dragged clear-AI text toward human.
- punctuation_density, expressive punctuation marks per word: `, ; : ( ) ! ?`, em/en dashes, `--` and ellipses. Periods are excluded because sentence endings would dominate the count. Counted in the style score.

Each counted metric goes through an S-curve so it becomes a 0–1 sub-score where higher means more AI (low spread → AI, low punctuation → AI). The style score is the mean of the two sub-scores.

**Why that might differ between human and AI writing:** Generated prose, as a consequence of most likely next word, tends to have lower sentence_length_spread with a narrower vocabulary band (debatably true, more true for model sameness across texts) and AI tends to have more formal, regular punctuation.

**What it can't see:** If chunks are really words or not. Prone to being fooled. Short text all three aren't particularly strong. Unlike the model signal, it reads the whole text (no 400-token limit). Difference in genre can also be stronger than the difference between human and AI (i.e. text message vs. essay). Plain writing with short, even sentences and little punctuation looks AI-like to both metrics.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** I lean hard against false positives (criterion 1). A text is only called AI when there is enough of it to judge *and* both signals agree.

1. **Average** the model score and the style score with equal weight.
2. **Pull thin evidence toward the middle.** `scoring.evidence_confidence` gives a confidence from 0 to 1, and the score becomes `0.5 + (average − 0.5) × confidence`. Confidence is the product of three factors:
   - **length:** 0 at 40 words or fewer, rising linearly to 1 at 100 words;
   - **style coverage:** the share of counted style metrics that could be measured (a single sentence has no spread, so 0.5);
   - **model coverage:** the model only reads the first 400 tokens, so its half of the evidence counts only for the share it read (`0.5 + 0.5 × share read`).
   
   Each factor below 1 adds a warning to the response and the audit log.
3. **Agreement gate.** A confident label needs both signals on the same side: high-confidence AI needs both ≥ 0.6, and high-confidence human needs both ≤ 0.4. If the score crosses a threshold but the signals disagree, it is clamped 0.01 inside the unsure band, so the label is "unsure" but the score still shows which way it leaned.
4. **Label** with a wider-than-even unsure band that is shifted toward AI: human at or below 0.35, AI at or above 0.75.

**The numbers:**

| Setting | Value | Where |
|---|---|---|
| Signal weights (model / style) | 0.5 / 0.5 | `config.py` |
| Model signal curve (perplexity midpoint / steepness) | 35 / 4 (was 45 / 1.6) | `detector.py::model_signal` |
| Style curves (midpoint / steepness) | spread 0.70 / 4, punctuation 0.07 / 4 | `stylometry.py::STYLE_CALIBRATION` |
| Style metric weights | spread 1, punctuation 1, TTR 0 | `stylometry.py::STYLE_WEIGHTS` |
| Length confidence ramp | 40 → 100 words | `config.py` |
| Agreement gate (AI floor / human ceiling / margin) | 0.6 / 0.4 / 0.01 | `config.py` |
| Thresholds (human / AI) | 0.35 / 0.75 | `config.py` |

I made the curves steeper so clear cases land near the ends. That keeps the AI label reachable even with a strict 0.75 threshold.

Results on the bundled samples plus two texts I wrote to test the rule (`plain_human`: a plain, short-sentence personal paragraph; `edited_ai`: an AI-style paragraph rewritten casually). They were identical across repeated runs.

| Text | Words | Model | Style | Average | Confidence | Combined | Label |
|---|---|---|---|---|---|---|---|
| clearly_ai | 92 | 0.858 | 0.881 | 0.870 | 0.867 | 0.820 | AI |
| borderline | 67 | 0.071 | 0.554 | 0.313 | 0.450 | 0.416 | unsure |
| clearly_human | 94 | 0.173 | 0.176 | 0.174 | 0.900 | 0.207 | human |
| plain_human (mine) | 64 | 0.843 | 0.969 | 0.906 | 0.400 | 0.662 | unsure |
| edited_ai (mine) | 57 | 0.047 | 0.263 | 0.155 | 0.283 | 0.402 | unsure |

**Known weakness:** `plain_human` would be a false positive (0.906 before the shrink) because *both* signals read plain writing as AI, so the gate can't help. It is only saved because it is short. A longer plain text would probably still be flagged. The length ramp was also tuned on these short samples, so it needs re-checking against my criterion 1 and 3 texts.

**Where it lives:** `scoring.py::combine_signals` (with `scoring.py::evidence_confidence` supplying the confidence)

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**

`samples/borderline.json`, which appears to be a lightly edited version of the `clearly_ai` text (same topic and the same prioritize / cut distractions / take breaks structure, rewritten in a casual voice).

| Signal | Score | Leans |
|---|---|---|
| model signal | 0.071 | strongly human |
| style signal | 0.554 | AI |
| average (0.5 / 0.5) | 0.313 | human (below 0.35) |
| after thin-evidence shrink (67 words, confidence 0.45) | 0.416 | unsure |

Why they split:
- **The model signal reads the words.** Casual edits like "frazzled", "wreck focus", "you're" and British spellings make the next word harder to predict. Its perplexity (66) is even higher than the clearly-human sample's (52), so the model calls it strongly human.
- **The style signal reads the shape, and the edit didn't change the shape much.** Sentence lengths are still fairly even (spread 0.465, sub-score 0.84 AI). The added em dash and semicolon raise punctuation density (0.090, sub-score 0.27 human), but not enough to outweigh the even sentences.

What the rule does: the plain average (0.313) would have labelled it high-confidence human, because the model signal is so sure. Two parts of the rule stop that:
- **The shrink:** at 67 words there isn't enough text to trust either signal fully, so the score is pulled to 0.416, inside the unsure band.
- **The gate:** even with a longer text and no shrink, the gate would block the human label, because the style signal (0.554) is above the 0.4 human ceiling. The score would be clamped to 0.36.

Either way it comes out unsure. That is the outcome I want for a case like this: two methods disagreeing is real uncertainty, and the label should say so instead of picking a side.

---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.35 (inclusive) | We think this was probably written by a person. |
| unsure | above 0.35 and below 0.75 | We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong. |
| high-confidence AI | 0.75 – 1.00 (inclusive) | Our checks say this reads as likely AI-generated. If you wrote this yourself, you can ask for a review. |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

My first draft was "We're not sure if this is written by a person, but we don't think it was written by AI." It had three problems:
- **It contradicted itself.** If it's not a person and not AI, who wrote it?
- **The doubt landed on the writer.** The first thing it questioned was whether a person wrote it.
- **It overclaimed.** "We don't think it was written by AI" isn't true across the whole band. Scores up to 0.749 land here, including texts that lean AI, like my plain-writing test at 0.662.

The final wording makes the *checks* the thing that's uncertain, not the writer. It says why ("mixed results") and that this is common, because most texts land in this band when they're short or the two signals disagree, which is a limit of the tool. It ends by saying nothing is wrong, so a writer who wrote every word isn't left wondering whether they've been flagged. It makes no claim in either direction, so it stays honest whether the score is 0.36 or 0.74.

---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "...", "creator_id": "..."}'
```

```json
{                                                                                                                                                    
  "combined_score": 0.8204,                                                                                                                          
  "confidence": 0.8204,                                                                                                                              
  "content_id": "c_6c8a6475a60e",                          
  "creator_id": "demo_instructor",
  "evidence_confidence": 0.8667,
  "guess": "ai",
  "label": "Our checks say this reads as likely AI-generated. If you wrote this yourself, you can ask for a review.",
  "model_score": 0.8582,
  "style_score": 0.8811,
  "warnings": [
    "Short text (92 words): score pulled toward 'unsure' (length confidence 0.87; full confidence at 100 words)."
  ]
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "...", "reasoning": "..."}'
```

```json
{                                                                                                                                                    
  "content_id": "c_6c8a6475a60e",                                                                                                                    
  "creator_id": "demo_instructor",                                                                                                                   
  "message": "Thanks \u2014 your appeal has been recorded and a person will review it.",
  "original_guess": "ai",
  "status": "under_review"
}
```

**Second Appeal**

```json
{
  "error": "conflict",
  "message": "Submission \"c_6c8a6475a60e\" has already been appealed and is under review.",
  "reason": "already_under_review"
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json
{                                                                                                                                                    
  "count": 3,                                                                                                                                        
  "entries": [                                                                                                                                       
    {                                                                                                                                                
      "combined_score": 0.8204,                            
      "content_id": "c_6c8a6475a60e",
      "creator_id": "demo_instructor",
      "evidence_confidence": 0.8667,
      "guess": "ai",
      "label": "Our checks say this reads as likely AI-generated. If you wrote this yourself, you can ask for a review.",
      "model_score": 0.8582,
      "status": "decided",
      "style_score": 0.8811,
      "timestamp": "2026-11-04T21:37:21+00:00",
      "warnings": [
        "Short text (92 words): score pulled toward 'unsure' (length confidence 0.87; full confidence at 100 words)."
      ]
    },
    {
      "content_id": "c_6c8a6475a60e",
      "creator_id": "demo_instructor",
      "event": "appeal",
      "reasoning": "I wrote this myself as a short guide on time management. It is plain and structured because it was meant as a quick checklist for my team, not because it was generated.",
      "status": "under_review",
      "timestamp": "2026-11-04T21:41:43+00:00"
    },
    {
      "content_id": "c_6c8a6475a60e",
      "creator_id": "demo_instructor",
      "event": "rejected",
      "reason": "already_under_review",
      "route": "appeal",
      "status": "rejected",
      "timestamp": "2026-11-04T21:42:05+00:00"
    }
  ]
}
```

---

## How I Used AI

I used AI throughout: to brainstorm and write my acceptance criteria, for the first version of `/submit` in `app.py`, and for the scoring and labels. These are the two moments that shaped the service most.

**Moment 1: Weighting the combining rule against false positives**

- *What I asked for:* Ideas for leaning hard against false positives (criterion 1). My own first idea was to raise the AI threshold to something like 0.875, but I suspected that would make the AI label unreachable (criterion 3).
- *What came back:* Confirmation that a high threshold alone would break criterion 3, because my scores were bunched in the middle (clear AI 0.674, clear human 0.443). It suggested five options: steeper calibration curves to spread the scores out, an agreement gate where both signals must agree before an AI label, pulling thin evidence toward 0.5, letting the style signal argue for human more than for AI, and a modest threshold shift. It recommended steeper curves plus the gate with a 0.75 threshold. Simulating that on my samples showed two problems: `borderline` would be labelled human, and a plain human-written test paragraph would still be labelled AI.
- *What I changed:* I made the decisions at each step. I chose a **symmetric** gate, so the human label also needs both signals to agree, because that is what sends `borderline` to unsure. I chose to **drop** TTR (weight 0) rather than flip its direction, even though flipping scored slightly better on the plain paragraph, because the flipped result only cleared the threshold by 0.002. I added the thin-evidence shrink as well. I picked the 40→100 word ramp, included the truncation and missing-metric factors, and left out the signal-disagreement factor because it overlaps with the gate. The README records that the plain paragraph is only saved because it is short.

**Moment 2: The wording of the "unsure" label**

- *What I asked for:* Criticism of my draft unsure label, "We're not sure if this is written by a person, but we don't think it was written by AI.", read as if I had written every word myself.
- *What came back:* Five problems. The label contradicted itself (not a person, not AI). It cast doubt on the writer first. It claimed "not AI" across a band that includes AI-leaning scores. It gave no reason. It used "is written" where "was written" was meant. Three rewrites followed, each making the *checks* the uncertain thing. It also flagged my AI label as too blunt for the one label that will reach real writers by mistake, and suggested pointing to the appeal.
- *What I changed:* I picked the third rewrite for unsure. I rewrote the AI label myself to soften it and add the appeal path: "Our checks say this reads as likely AI-generated. If you wrote this yourself, you can ask for a review." I kept my human label unchanged.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 5 per minute, 50 per day

**Why those numbers and not others:** A real writer probably wouldn't do more than 50 submissions a day. Maybe 5 a minute is reasonable if they make a mistake etc. A script sending a ton would go past this.
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. --> A caller counts as one creator_id associated with an account. This gets around being rate limited by address but need to be wary that someone can use a script to manipulate creator_id.

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```
200 200 200 200 200 429 429 429 429 429 429 429 429 429 429
```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

{
  "id": "EV01",
  "status": 200,
  "content_id": "c_161aea20893f",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.4904,
  "model_score": 0.0061,
  "style_score": 0.9683,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": "BROKE"
}

{
  "id": "EV02",
  "status": 200,
  "content_id": "c_42d5f8cde735",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.5518,
  "model_score": 0.4873,
  "style_score": 0.6345,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": "BROKE"
}

{
  "id": "EV04",
  "status": 200,
  "content_id": "c_491cd68729bc",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.6921,
  "model_score": 0.532,
  "style_score": 0.9691,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": "BROKE"
}

{
  "id": "EV06",
  "status": 200,
  "content_id": "c_889fe1ddf521",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.4843,
  "model_score": 0.4321,
  "style_score": 0.5316,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": "BROKE"
}

{
  "id": "EV07",
  "status": 200,
  "content_id": "c_db73536e3993",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.4339,
  "model_score": 0.4663,
  "style_score": 0.2554,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": "BROKE"
}

{
  "id": "EV08",
  "status": 200,
  "content_id": "c_6c7facb07c55",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0215,
  "style_score": 0.987,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": "BROKE"
}

{
  "id": "FP03",
  "status": 200,
  "content_id": "c_24a6d2401d62",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.8239,
  "model_score": 0.927,
  "style_score": 0.977,
  "label": "Our checks say this reads as likely AI-generated. If you wrote this yourself, you can ask for a review.",
  "error": null,
  "verdict": "BROKE"
}

{
  "id": "MF03",
  "status": 200,
  "content_id": "c_f5abb537d002",
  "creator_id": "attacker_MF03",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0,
  "style_score": 0.75,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": "BROKE"
}

{
  "id": "MF05",
  "status": 200,
  "content_id": "c_b28ed26f2218",
  "creator_id": "attacker_MF05",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 1.0,
  "style_score": 0.75,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": "BROKE"
}

{
  "id": "FL01_06",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "BROKE"
}
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

FP03 being marked as AI had the worst outcome in my opinion. Non-native English speaker writing carefully. Could come off extremely discouraging, especially while someone is trying to learn something as time consuming/difficult as a language. I'd want to reassure them that it's the style and model predictability and not a statement about them or their ability.

---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My own writing flagged as AI (`guess: "ai"`) | 0 of 5 | 0/5 | 0/5 | 0/5 | MET |
| 2. Appeal path: 5 appeals logged as `under_review`, repeat gets 409, unknown id gets 404, refusals logged | 7 of 7 checks | 7/7 | 7/7 | 7/7 | MET |
| 3. Pre-labelled inputs reach their intended label | 9 of 9 | 3/9 | 3/9 | 3/9 | MISSED |
| 4. Lowest clearly-AI combined score minus highest clearly-human combined score | ≥ 0.30 | −0.051 | −0.051 | −0.051 | MISSED |
| 5. Bad input: 6 malformed bodies get a 400 naming the problem, long text gets a 200 with a truncation warning | 7 of 7 | 7/7 | 7/7 | 7/7 | MET |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

`results/run_2026-11-08_1819_before.md`, produced by `run_eval.py::main` (service: `app.py::submit`, scoring: `scoring.py::combine_signals`). Criterion 3, label coverage, trial 1. Texts in order: 3 clearly AI, 3 borderline, 3 clearly human.

```json
[
  {
    "status": 200,
    "content_id": "c_220e33fab2f9",
    "guess": "unsure",
    "confidence": 0.74,
    "combined_score": 0.74,
    "model_score": 0.9405,
    "style_score": 0.5816,
    "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
    "warnings": [],
    "error": null,
    "reason": null,
    "message": null,
    "sent": "Coffee is more than just a beverage; it is a rich tapestry of culture,"
  },
  {
    "status": 200,
    "content_id": "c_67a2eb6904ff",
    "guess": "unsure",
    "confidence": 0.7355,
    "combined_score": 0.7355,
    "model_score": 0.8976,
    "style_score": 0.5735,
    "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
    "warnings": [],
    "error": null,
    "reason": null,
    "message": null,
    "sent": "Time management is a crucial skill that can significantly enhance both"
  },
  {
    "status": 200,
    "content_id": "c_19b88eba6f7e",
    "guess": "unsure",
    "confidence": 0.74,
    "combined_score": 0.74,
    "model_score": 0.9872,
    "style_score": 0.5804,
    "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
    "warnings": [],
    "error": null,
    "reason": null,
    "message": null,
    "sent": "The ocean is a vast and mysterious realm that plays a vital role in su"
  },
  {
    "status": 200,
    "content_id": "c_efff6a3b841c",
    "guess": "unsure",
    "confidence": 0.5892,
    "combined_score": 0.5892,
    "model_score": 0.3858,
    "style_score": 0.7927,
    "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
    "warnings": [],
    "error": null,
    "reason": null,
    "message": null,
    "sent": "I apparently convinced someone to rethink their transphobia. A few day"
  },
  {
    "status": 200,
    "content_id": "c_7dc170ab1841",
    "guess": "unsure",
    "confidence": 0.572,
    "combined_score": 0.572,
    "model_score": 0.301,
    "style_score": 0.843,
    "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
    "warnings": [],
    "error": null,
    "reason": null,
    "message": null,
    "sent": "Last night I dreamed I was in a plane crash, or at least I think I was"
  },
  {
    "status": 200,
    "content_id": "c_25702169117c",
    "guess": "unsure",
    "confidence": 0.6001,
    "combined_score": 0.6001,
    "model_score": 0.4116,
    "style_score": 0.7886,
    "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
    "warnings": [],
    "error": null,
    "reason": null,
    "message": null,
    "sent": "Persona is probably my favorite game series that I've ever played. Wha"
  },
  {
    "status": 200,
    "content_id": "c_3a710eb1677e",
    "guess": "unsure",
    "confidence": 0.5585,
    "combined_score": 0.5585,
    "model_score": 0.2202,
    "style_score": 0.8968,
    "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
    "warnings": [],
    "error": null,
    "reason": null,
    "message": null,
    "sent": "Convinced a guy to stop being transphobic apparently. Other day he was"
  },
  {
    "status": 200,
    "content_id": "c_ef436befb2fd",
    "guess": "ai",
    "confidence": 0.7864,
    "combined_score": 0.7864,
    "model_score": 0.8177,
    "style_score": 0.7552,
    "label": "Our checks say this reads as likely AI-generated. If you wrote this yourself, you can ask for a review.",
    "warnings": [],
    "error": null,
    "reason": null,
    "message": null,
    "sent": "The world is in chaos, but for the bosses, it's all going according to"
  },
  {
    "status": 200,
    "content_id": "c_25257817d63d",
    "guess": "unsure",
    "confidence": 0.7356,
    "combined_score": 0.7356,
    "model_score": 0.8763,
    "style_score": 0.5949,
    "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
    "warnings": [],
    "error": null,
    "reason": null,
    "message": null,
    "sent": "Democratic socialists know that no one has to live like this. If we li"
  }
]
```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->

Every miss and broken attack comes down to five problems. Style sub-scores and perplexities below are recomputed from `stylometry.py` and `detector.py` on the same texts.

**1. Punctuation density points the wrong way. Stage: signal two, then the combining rule's gate.**
*Criterion 3 (AI texts land in unsure) and criterion 4.*

All three AI texts scored high on the model signal (0.90–0.99), but their style scores were only 0.57–0.58. Sentence-length spread did its job: spreads of 0.10–0.42 gave AI sub-scores of 0.89–1.00. Punctuation density did the opposite. The AI texts are full of comma lists and transitions ("culture, history, and community", "First,", "However,"), giving 0.089–0.105 marks per word. That is above my 0.07 midpoint, so punctuation read them as human (sub-scores 0.16–0.27).

Averaged together, the style score stayed below the gate's 0.6 AI floor. Coffee (average 0.761) and ocean (0.784) both crossed the 0.75 threshold, but the gate clamped them to exactly 0.74 because the style signal disagreed. Time management (0.7355) didn't reach the threshold at all.

The cause is my calibration. I set "low punctuation → AI" from three bundled samples, and on my criterion texts that direction is reversed:

| Text | Punctuation per word | Punctuation sub-score |
|---|---|---|
| AI texts | 0.089–0.105 | 0.16–0.27 (human) |
| My own writing | 0.032–0.039 | 0.92–0.96 (AI) |
| Transphobia post | 0.029 | 0.97 (AI) |

**2. Both signals read polished human prose as AI, so the gate can't help. Stage: signal one and signal two together.**
*Criterion 3 ("world is in chaos" labelled AI), criterion 4's negative gap, and attack FP03.*

The gate only protects a writer when the two signals disagree. Formal, polished writing makes them agree. "The world is in chaos" has a perplexity of 24.1, close to the AI texts' 11.8–20.3. Its sentences are even (spread 0.24, sub-score 0.99). So the model scored 0.82 and style scored 0.76. Both were above 0.6, the gate passed, and it was labelled AI at 0.786. That is the highest human score, which is why criterion 4's gap is −0.051.

FP03, a non-native speaker writing carefully, fails the same way: model 0.93, style 0.98, labelled AI at 0.824. Simple, careful, regular writing is predictable *and* evenly shaped. My two signals were meant to be independent checks, but on this kind of writer they share the blind spot. The DSA text (model 0.88, perplexity 21.5) only escaped because punctuation (0.37) pulled its style score down to 0.59.

Problem 1 also blocks the human label. The casual transphobia post scored 0.22 on the model signal (human), but its sparse punctuation pushed style to 0.90. The gate needs both signals ≤ 0.4 for a human label, so it landed in unsure (0.5585). No text reached high-confidence human.

**3. One weakened signal is enough to dodge the AI label. Stage: the combining rule (agreement gate, then the thin-evidence shrink).**
*Attacks EV01, EV02, EV04, EV05, EV06, EV07 and EV08.*

The AI label needs the average to reach 0.75 *and* both signals to be at least 0.6. An attacker only has to push one signal below 0.6, or keep the text short. I built this rule on purpose to avoid false positives, and this is what it costs.

- **EV01 (typos).** The attack aimed at word variety in signal two, but TTR is weighted 0, so it actually hit signal one. Misspellings are rare tokens, so perplexity jumped and the model scored 0.006. Style still said AI (0.97), so the gate made it unsure (0.490).
- **EV04 (unusual words).** Same route: the model dropped to 0.53, below the 0.6 floor. At 86 words the shrink also pulled it to 0.692.
- **EV02 and EV06 (broken-up sentences, one very long and one very short).** These raise sentence-length spread, so style fell to 0.63 and 0.53 and the average fell below 0.75. The model was already only 0.49 and 0.43, so sentence shape alone wasn't the whole story.
- **EV07 (punctuation padding).** Problem 1 used deliberately: extra punctuation dropped style to 0.26. It was also a single sentence, so spread couldn't be measured and confidence fell to 0.475.
- **EV05 (heavy human edit).** The model fell to 0.05. After a heavy edit the text is arguably mostly human, so this one is the least clear-cut.
- **EV08 (below the token window).** At 10 words, length confidence is 0, so the score is forced to exactly 0.5. Any text under 40 words gets this free pass.

**4. `/submit` accepts input with no scorable words, and doesn't check `creator_id`. Stage: the route.**
*Attacks MF03–MF08, RQ02, RQ06 and RQ07.*

The route only checks that `text` is a non-empty string, then hands it to the signals.

- **MF03–MF07 (control characters, punctuation only, one very long word, emoji, right-to-left script).** All pass that check and have at least 3 tokens, so the model doesn't raise. `stylometry.words` only matches `[a-z0-9']`, so emoji, punctuation and non-Latin script count as 0 words, and the rest are a handful of words at most. All five are under the 40-word floor, so confidence drops to 0 and the score is forced to 0.5. Each one got a 200, a `content_id` and an "unsure" label for text nobody could have judged.
- **MF08 (60,000 characters).** Accepted, because there's no size cap. The model read only the first 3%, while style read all of it, and it came back unsure at 0.741, just below the AI line.
- **RQ02 and RQ06 (no `creator_id`, or one that's an object).** The route never checks `creator_id`. RQ02 was logged as `"unknown"`. RQ06 wrote `{"id": "x"}` straight into the audit log as the creator.
- **RQ07 (body is a JSON array).** `request.get_json(silent=True) or {}` only replaces an empty body. A non-empty list passes through, and `payload.get` raises `AttributeError`. The result is a 500 that returns the Werkzeug debugger page. `/appeal` has an `isinstance(payload, dict)` guard; `/submit` doesn't, so this one is still open.

**5. Anonymous callers share one rate-limit bucket. Stage: the route's rate-limit key.**
*Attacks RQ10 and RQ11 (got a 429 where a 400 was expected).*

`rate_limit_key` falls back to the caller's address when there's no string `creator_id`. RQ02, RQ06, RQ07, RQ08 and RQ09 had no usable `creator_id`, so all five counted against localhost's 5-per-minute limit. That used up the bucket before RQ10 and RQ11 arrived, so they got a 429 instead of the 400 their bad bodies deserved. A real user with a malformed client would also see "too many submissions" instead of being told what was wrong.

---

## The Improvement

**What I changed:** I flipped the direction of the punctuation-density metric in the style signal, from "low punctuation → AI" to "high punctuation → AI". It's one change in `stylometry.py`: a new `HIGH_MEANS_AI` set containing `punctuation_density`. `style_signal` subtracts that metric's sub-score from 1. The midpoint (0.07), the steepness (4), the weights and everything in the combining rule are unchanged. The midpoint already sits between the two groups (AI texts 0.089–0.105 marks per word, my writing 0.029–0.039). Only the direction was wrong.

**Which diagnosis pointed at it:** Diagnosis 1, punctuation density pointing the wrong way. I had set the direction from three bundled samples, and on my criterion texts it was reversed. That is why the AI texts' style scores sat at 0.57–0.58, under the gate's 0.6 floor, which held coffee and ocean at 0.74. It also pushed my casual writing's style scores up to 0.79–0.90. One wrong direction on one metric produced most of the criterion 3 and 4 misses, and EV07 used the same weakness on purpose by padding with punctuation. Flipping it should let the AI texts clear the gate, and should stop sparse, casual human writing from reading as AI.

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
