# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-08 18:35
- Auto-marked BROKE (5xx, crash, no response): **1**
- Left for you to judge: **55**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `c_05025a0c5c1f` | unsure | 0.360 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `c_256a8bcef0c0` | unsure | 0.359 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `c_f9dbd92bb3c5` | unsure | 0.595 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `c_ebf301d3773e` | unsure | 0.523 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `c_acd9979a748e` | unsure | 0.360 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `c_ec43b39f2d31` | unsure | 0.360 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `c_4dd65d62d815` | unsure | 0.550 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `c_6c3773bbed7e` | unsure | 0.500 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `c_9f4af97a6637` | unsure | 0.626 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `c_7f0221344451` | unsure | 0.644 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `c_ff6a03886059` | unsure | 0.487 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `c_6bfc5453ab9b` | unsure | 0.598 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `c_be42fccc38ff` | unsure | 0.645 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `c_cb7481bf75e4` | unsure | 0.598 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `c_b601460a2a69` | unsure | 0.606 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `c_69ad615075d6` | unsure | 0.574 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `c_7c55a6ef37f7` | unsure | 0.537 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `c_ce6a057228a1` | unsure | 0.500 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `c_f977d3b52f32` | unsure | 0.478 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `c_3ed1d6e40473` | unsure | 0.474 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `c_58fc6fcd3755` | unsure | 0.512 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `c_e368cc5ce568` | unsure | 0.502 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `c_1340590c784a` | unsure | 0.500 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `c_3ad4f73843a4` | unsure | 0.414 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `c_724eed157910` | unsure | 0.500 |  |
| MF04 | malformed | text is only punctuation | 200 | `c_ce476a3dd126` | unsure | 0.500 |  |
| MF05 | malformed | text is a very long single word | 200 | `c_6c8e0db8acf3` | unsure | 0.500 |  |
| MF06 | malformed | text is emoji only | 200 | `c_654263ef9f03` | unsure | 0.500 |  |
| MF07 | malformed | text is right-to-left script | 200 | `c_f072995d4a2d` | unsure | 0.500 |  |
| MF08 | malformed | text is 60,000 characters | 200 | `c_69c219789a57` | unsure | 0.614 |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 200 | `c_63d8b12d92fa` | unsure | 0.500 |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 200 | `c_22a13cb2f2c6` | unsure | 0.500 |  |
| RQ07 | malformed | body is a JSON array, not an object | 500 | `—` | — | — | BROKE |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_2c3895f19cab` | unsure | 0.500 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_e6d7c9cc66f1` | unsure | 0.500 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_bb0eadbb5238` | unsure | 0.500 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_1d3032953c90` | unsure | 0.500 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_8939f47b08ec` | unsure | 0.500 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 1 | 19 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "c_05025a0c5c1f",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.36,
  "model_score": 0.0061,
  "style_score": 0.529,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "c_256a8bcef0c0",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.3592,
  "model_score": 0.4873,
  "style_score": 0.1814,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "c_f9dbd92bb3c5",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5947,
  "model_score": 0.6732,
  "style_score": 0.5162,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "c_ebf301d3773e",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.5227,
  "model_score": 0.532,
  "style_score": 0.5271,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "c_acd9979a748e",
  "creator_id": "attacker_EV05",
  "guess": "unsure",
  "confidence": 0.36,
  "model_score": 0.0533,
  "style_score": 0.4506,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "c_ec43b39f2d31",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.36,
  "model_score": 0.4321,
  "style_score": 0.0766,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "c_4dd65d62d815",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.5501,
  "model_score": 0.4663,
  "style_score": 0.7446,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "c_6c3773bbed7e",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0215,
  "style_score": 0.487,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "c_9f4af97a6637",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.626,
  "model_score": 0.7619,
  "style_score": 0.4902,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "c_7f0221344451",
  "creator_id": "attacker_EV10",
  "guess": "unsure",
  "confidence": 0.6438,
  "model_score": 0.9998,
  "style_score": 0.4544,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "c_ff6a03886059",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.4869,
  "model_score": 0.548,
  "style_score": 0.4258,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "c_6bfc5453ab9b",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.5975,
  "model_score": 0.8311,
  "style_score": 0.4938,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "c_be42fccc38ff",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.6448,
  "model_score": 0.927,
  "style_score": 0.477,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "c_cb7481bf75e4",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.5978,
  "model_score": 0.9531,
  "style_score": 0.466,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "c_b601460a2a69",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.6059,
  "model_score": 0.9219,
  "style_score": 0.5016,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "c_69ad615075d6",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.5735,
  "model_score": 0.9822,
  "style_score": 0.3851,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "c_7c55a6ef37f7",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.5375,
  "model_score": 0.9823,
  "style_score": 0.2545,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "c_ce6a057228a1",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.054,
  "style_score": 0.4361,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "c_f977d3b52f32",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.4783,
  "model_score": 0.2008,
  "style_score": 0.2773,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "c_3ed1d6e40473",
  "creator_id": "attacker_PI02",
  "guess": "unsure",
  "confidence": 0.4737,
  "model_score": 0.0121,
  "style_score": 0.3553,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "c_58fc6fcd3755",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5118,
  "model_score": 0.4873,
  "style_score": 0.6074,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "c_e368cc5ce568",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.5024,
  "model_score": 0.2675,
  "style_score": 0.7591,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "c_1340590c784a",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.607,
  "style_score": 0.9073,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "c_3ad4f73843a4",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.4141,
  "model_score": 0.3966,
  "style_score": 0.4316,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "c_724eed157910",
  "creator_id": "attacker_MF03",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0,
  "style_score": 0.25,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "c_ce476a3dd126",
  "creator_id": "attacker_MF04",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0,
  "style_score": 0.5,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "c_6c8e0db8acf3",
  "creator_id": "attacker_MF05",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 1.0,
  "style_score": 0.25,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "c_654263ef9f03",
  "creator_id": "attacker_MF06",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 1.0,
  "style_score": 0.5,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "c_f072995d4a2d",
  "creator_id": "attacker_MF07",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.9907,
  "style_score": 0.5,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 200,
  "content_id": "c_69c219789a57",
  "creator_id": "attacker_MF08",
  "guess": "unsure",
  "confidence": 0.6138,
  "model_score": 1.0,
  "style_score": 0.4415,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 200,
  "content_id": "c_63d8b12d92fa",
  "creator_id": null,
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0199,
  "style_score": 0.25,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 200,
  "content_id": "c_22a13cb2f2c6",
  "creator_id": {
    "id": "x"
  },
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0002,
  "style_score": 0.25,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 500,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "response wasn't JSON: <!doctype html>\n<html lang=en>\n  <head>\n    <title>AttributeError: &#39;list&#39; object has no attribute &#39;get&#39;\n // Werkzeug Debugger</title>\n    <link rel=\"stylesheet\" href=\"?__debugger__=yes",
  "verdict": "BROKE"
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "c_2c3895f19cab",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0001,
  "style_score": 0.25,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "c_e6d7c9cc66f1",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0001,
  "style_score": 0.25,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "c_bb0eadbb5238",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0001,
  "style_score": 0.25,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "c_1d3032953c90",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0001,
  "style_score": 0.25,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "c_8939f47b08ec",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0001,
  "style_score": 0.25,
  "label": "We can't say whether a person or AI wrote this. Our checks gave mixed results, which is common and doesn't mean anything is wrong.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
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
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
