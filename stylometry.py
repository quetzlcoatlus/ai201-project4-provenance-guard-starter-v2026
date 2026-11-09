"""
Signal two: the style signal. ← YOU BUILD THIS IN MILESTONE 4

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics
from typing import Optional


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures — YOU BUILD THESE ─────────────────────────────────────

def sentence_length_spread(text: str) -> Optional[float]:
    """
    How much sentence length varies: coefficient of variation (CV) of
    sentence lengths in words = stdev / mean.

    Returns:
        Raw CV, unbounded, >= 0. **Higher means more human** (burstier).
        Not scaled to 0–1 here; style_signal is responsible for scaling.
        Rough guide: AI prose often ~0.25–0.45, human often ~0.5–0.9.

        None if fewer than 2 sentences with at least one word each — there is
        no spread to measure. The caller decides what that means.
    """
    lengths = [len(words(s)) for s in sentences(text)]
    lengths = [n for n in lengths if n > 0]   # drop "sentences" with no words
    if len(lengths) < 2:
        return None
    return statistics.stdev(lengths) / statistics.mean(lengths)


MATTR_WINDOW = 50


def type_token_ratio(text: str) -> Optional[float]:
    """
    Lexical variety as a moving-average type-token ratio (MATTR).

    Slides a 50-word window across the text one word at a time, takes
    unique/total inside each window, and averages them. This keeps long and
    short texts comparable, unlike plain TTR which falls as text grows.
    Texts shorter than the window fall back to plain TTR over the whole text.

    Returns:
        A float between 0 and 1. Higher means more varied vocabulary.
        Direction vs. AI/human is NOT assumed — check it on calibration inputs.
        None if the text has no words.
    """
    tokens = words(text)
    if not tokens:
        return None
    if len(tokens) < MATTR_WINDOW:
        return len(set(tokens)) / len(tokens)

    ratios = [
        len(set(tokens[i:i + MATTR_WINDOW])) / MATTR_WINDOW
        for i in range(len(tokens) - MATTR_WINDOW + 1)
    ]
    return statistics.mean(ratios)


# Expressive punctuation — periods deliberately excluded. Longer forms are
# listed first so "--" and "..." count as one mark, not two hyphens / dots.
# A single hyphen is not counted (it is mostly word-internal: "well-known").
EXPRESSIVE_PUNCT = re.compile(r"—|–|--|\.\.\.|…|[,;:()!?]")


def punctuation_density(text: str) -> Optional[float]:
    """
    Expressive punctuation marks per word.

    Counts: , ; : ( ) ! ?  em dash —  en dash –  double hyphen --
            ellipsis … and its typed form ...
    Excludes: periods (sentence ends dominate otherwise), single hyphens,
              quotes and apostrophes.

    Returns:
        A float >= 0 (marks per word; typical prose is roughly 0.05–0.25).
        Direction vs. AI/human is NOT assumed — check it on calibration inputs.
        None if the text has no words.
    """
    n_words = len(words(text))
    if n_words == 0:
        return None
    return len(EXPRESSIVE_PUNCT.findall(text)) / n_words


# ── Combining them ───────────────────────────────────────────────────────────

# Per-metric calibration: (midpoint, steepness).
#   midpoint  — the raw value that maps to 0.5 (coin flip).
#   steepness — how sharply the sub-score moves either side of the midpoint.
# Spread and TTR use the "LOW raw value -> AI" direction (folk directions).
# Punctuation is flipped to "HIGH -> AI" (see HIGH_MEANS_AI below).
# Midpoints sit between the clearly_ai and clearly_human sample values.
# Steepness 4 (was 2.5) pushes clear cases toward the ends so a strict
# AI threshold stays reachable — idea 1, "spread the scores out".
# Calibrated on only 3 samples — re-check on the Milestone 4 inputs.
STYLE_CALIBRATION = {
    "sentence_length_spread": (0.70, 4.0),   # samples: AI 0.41, human 1.13
    "type_token_ratio":       (0.86, 20.0),  # samples: AI 0.92, human 0.81 (!)
    "punctuation_density":    (0.07, 4.0),   # samples: AI 0.04, human 0.10
}

# How much each metric counts in the style score (weighted mean).
# TTR is weighted 0: on the samples it ran opposite to the folk direction
# (AI text had the HIGHER ratio) and dragged clear-AI text toward human.
# It is still computed so its raw value can be inspected.
STYLE_WEIGHTS = {
    "sentence_length_spread": 1.0,
    "type_token_ratio":       0.0,
    "punctuation_density":    1.0,
}

# Metrics scored in the "HIGH raw value -> AI" direction instead.
# Punctuation was flipped in unit 8: on the criterion texts the bundled-sample
# direction was backwards. The AI texts are comma-heavy (0.089-0.105 marks per
# word, lists and "First," / "However," transitions) while my casual writing
# is sparse (0.029-0.039), so "low -> AI" scored AI text as human and my own
# writing as AI. The midpoint (0.07) still sits between the two groups.
HIGH_MEANS_AI = {"punctuation_density"}

NEUTRAL = 0.5   # sub-score used when a metric can't be measured


def _low_means_ai(value: float, midpoint: float, steepness: float) -> float:
    """
    Logistic on log(value), same form as detector.model_signal:
    value == midpoint -> 0.5, value below midpoint -> toward 1 (AI),
    value above midpoint -> toward 0 (human). value 0 -> 1.0.
    """
    if value <= 0:
        return 1.0
    return 1.0 / (1.0 + (value / midpoint) ** steepness)


def style_signal(text: str) -> tuple[float, list[str]]:
    """
    The style signal as a 0–1 score. **Higher means more likely AI.**

    Rule:
      1. Direction — spread and TTR are flipped so LOW raw value -> AI;
         punctuation runs the other way (HIGH_MEANS_AI):
           low sentence-length spread  -> AI (even, marching sentences)
           low type-token ratio        -> AI (narrower vocabulary)
           high punctuation density    -> AI (comma lists, transitions)
         Note: on the 3 bundled samples, TTR actually ran the other way
         (AI text had the HIGHER ratio), so it is weighted 0 for now
         (STYLE_WEIGHTS). Spread and punctuation count equally.
      2. Scale — each raw value goes through a logistic curve around its own
         midpoint (STYLE_CALIBRATION), giving a 0–1 sub-score.
      3. Combine — weighted mean of the sub-scores (STYLE_WEIGHTS).
      4. Missing — a counted metric that returns None contributes NEUTRAL
         (0.5) and adds a warning, so thin text drifts toward "unsure".
         Metrics with weight 0 are skipped entirely.

    Returns:
        (score, warnings) — score rounded to 4 places in [0, 1];
        warnings is a list of human-readable strings for the audit trace.
    """
    raw = {
        "sentence_length_spread": sentence_length_spread(text),
        "type_token_ratio": type_token_ratio(text),
        "punctuation_density": punctuation_density(text),
    }
    why_missing = {
        "sentence_length_spread": "fewer than 2 sentences",
        "type_token_ratio": "no words",
        "punctuation_density": "no words",
    }

    weighted_sum = 0.0
    total_weight = 0.0
    warnings = []
    for name, value in raw.items():
        weight = STYLE_WEIGHTS[name]
        if weight == 0:
            continue
        if value is None:
            sub = NEUTRAL
            warnings.append(
                f"Style signal: {name} could not be measured "
                f"({why_missing[name]}); counted as neutral {NEUTRAL}."
            )
        else:
            midpoint, steepness = STYLE_CALIBRATION[name]
            sub = _low_means_ai(value, midpoint, steepness)
            if name in HIGH_MEANS_AI:
                sub = 1.0 - sub
        weighted_sum += weight * sub
        total_weight += weight

    score = weighted_sum / total_weight
    return round(min(max(score, 0.0), 1.0), 4), warnings


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    score, warnings = style_signal(text)
    print(f"style_signal             {score}   (higher = more likely AI)")
    for w in warnings:
        print(f"  warning: {w}")
