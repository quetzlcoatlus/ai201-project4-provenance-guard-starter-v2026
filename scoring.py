"""
Turning two numbers into one, and one number into something a person can read.
← YOU BUILD THIS IN MILESTONES 4 AND 5

Two functions live here, and both are stubs.

`combine_signals` is where your false-positive decision from Milestone 1
actually gets made. Everything above it — the labels, the appeal path — is
downstream of a number this function produced.

`score_to_label` is where you stop writing for a machine and start writing for
a person. A score of 0.62 means nothing to a writer.

⚠️ Your README's **Signals and Scoring** section has to name the file and
function holding your combining rule. The grader checks your code against what
you claim, so that line should read `scoring.py::combine_signals`.
"""

import config


def evidence_confidence(text: str) -> tuple[float, list[str]]:
    """
    How much evidence the text gives the signals, from 0 (none) to 1 (full).
    combine_signals uses it to pull thin-evidence scores toward 0.5.

    confidence = length × style_coverage × model_coverage

      length          0 at <= CONFIDENCE_MIN_WORDS words, 1 at >= CONFIDENCE_FULL_WORDS,
                      linear between. Short text is the least reliable input.
      style_coverage  share of counted style metrics (weight > 0) that could
                      be measured, e.g. one sentence -> no spread -> 0.5.
      model_coverage  the model only reads the first DETECTOR_MAX_TOKENS
                      tokens, so its half of the evidence is partial on long
                      text: WEIGHT_STYLE + WEIGHT_MODEL × (share of tokens read).

    Returns:
        (confidence, warnings) — warnings explain each factor below 1, for
        the audit trace.
    """
    import detector
    import stylometry

    warnings = []

    n_words = len(stylometry.words(text))
    lo, hi = config.CONFIDENCE_MIN_WORDS, config.CONFIDENCE_FULL_WORDS
    length = min(max((n_words - lo) / (hi - lo), 0.0), 1.0)
    if length < 1.0:
        warnings.append(
            f"Short text ({n_words} words): score pulled toward 'unsure' "
            f"(length confidence {length:.2f}; full confidence at {hi} words)."
        )

    measures = {
        "sentence_length_spread": stylometry.sentence_length_spread,
        "type_token_ratio": stylometry.type_token_ratio,
        "punctuation_density": stylometry.punctuation_density,
    }
    counted = [name for name, w in stylometry.STYLE_WEIGHTS.items() if w > 0]
    measured = [name for name in counted if measures[name](text) is not None]
    style_coverage = len(measured) / len(counted) if counted else 0.0
    if style_coverage < 1.0:
        warnings.append(
            f"Only {len(measured)} of {len(counted)} style measures could be "
            f"computed: score pulled toward 'unsure'."
        )

    n_tokens = detector.token_count(text)
    read_share = min(1.0, config.DETECTOR_MAX_TOKENS / n_tokens) if n_tokens else 1.0
    model_coverage = config.WEIGHT_STYLE_SIGNAL + config.WEIGHT_MODEL_SIGNAL * read_share
    if model_coverage < 1.0:
        warnings.append(
            f"Model signal read {read_share:.0%} of the text: score pulled "
            f"toward 'unsure' (model coverage {model_coverage:.2f})."
        )

    return round(length * style_coverage * model_coverage, 4), warnings


def combine_signals(model_score: float, style_score: float, confidence: float = 1.0) -> float:
    """
    Combine two 0–1 signals into one 0–1 score. ← TODO (Milestone 4)

    Both inputs point the same way: higher means more likely AI. Your output
    should too.

    Args:
        model_score: from `detector.model_signal` — how predictable the text is.
        style_score: from `stylometry.style_signal` — the shape of the text.

    Returns:
        A float from 0.0 (confidently human) to 1.0 (confidently AI).

    ⚠️ **Write the rule down before you code it, and put the numbers in your
    README.** A weighted average is the obvious choice and it is not the only
    one. Things worth thinking about:

      - **What happens when they disagree?** One signal at 0.9 and the other at
        0.1 averages to 0.5 — "unsure". Is that what you want? It might be
        exactly right: two methods disagreeing IS uncertainty. Or you might
        decide one signal is more trustworthy when they split.

      - **Which way do you want to be wrong?** Weighting toward the signal that
        reads more human means fewer false accusations and more AI text
        getting through. There's no weighting that avoids the trade.

      - Milestone 4 asks you to find a case where your two signals split and
        write it down. That case is what this rule exists to handle.

    The weights in config.py are placeholders. Change them, or ignore them and
    write a different rule.
    """
    # Rule: weighted average, thin-evidence shrink, then a symmetric agreement gate.
    #   1. Average the two signals (weights in config, currently 0.5 / 0.5).
    #   2. Pull toward 0.5 by `confidence` (from evidence_confidence):
    #        0.5 + (average - 0.5) * confidence
    #      Thin evidence (short text, unmeasured style metrics, truncation)
    #      can't produce a confident label. confidence=1.0 leaves it unchanged.
    #   3. A confident label needs both signals to agree:
    #        AI    -> both >= AGREE_AI_FLOOR
    #        human -> both <= AGREE_HUMAN_CEILING
    #   4. If the score crosses a threshold but the signals disagree, clamp
    #      it just inside the unsure band. Disagreement IS uncertainty, and
    #      one signal alone should never accuse a writer.
    confidence = min(max(confidence, 0.0), 1.0)
    average = (
        config.WEIGHT_MODEL_SIGNAL * model_score
        + config.WEIGHT_STYLE_SIGNAL * style_score
    )
    average = 0.5 + (average - 0.5) * confidence

    if average >= config.AI_THRESHOLD and min(model_score, style_score) < config.AGREE_AI_FLOOR:
        average = config.AI_THRESHOLD - config.GATE_MARGIN
    elif average <= config.HUMAN_THRESHOLD and max(model_score, style_score) > config.AGREE_HUMAN_CEILING:
        average = config.HUMAN_THRESHOLD + config.GATE_MARGIN

    return round(average, 4)


def score_to_label(score: float) -> tuple[str, str]:
    """
    Turn a score into a guess and the text a reader actually sees.
    ← TODO (Milestone 5)

    Returns:
        (guess, label_text) — where `guess` is a short machine-readable string
        like "ai" / "human" / "unsure", and `label_text` is the full sentence
        shown to a person.

    ⚠️ Write the label text for someone who has never heard the word
    "threshold".

        ✗ "human, 0.81 confidence"
        ✓ "We think this was probably written by a person."

    All three labels have to be **reachable**. If no score can produce one of
    them, your ranges have a gap — and Milestone 5 asks you to submit text that
    produces each one, which is how you'd find out.

    The hardest one to write is "unsure". It has to admit uncertainty without
    sounding like an accusation, because the person reading it may well have
    written every word themselves. Your breakout asks your group what they'd
    think if they got it on their own work. That question is the whole
    milestone.
    """
    # TODO: replace this — thresholds are in config.py
    if score >= config.AI_THRESHOLD:
        return "ai", "PLACEHOLDER — write the high-confidence AI label."
    if score <= config.HUMAN_THRESHOLD:
        return "human", "PLACEHOLDER — write the high-confidence human label."
    return "unsure", "PLACEHOLDER — write the unsure label."


def label_ranges() -> list[tuple[str, str]]:
    """
    The score range each label covers. Your README needs these beside the
    label text — given to you so the numbers can't drift apart from config.py.
    """
    return [
        ("high-confidence human", f"0.00 – {config.HUMAN_THRESHOLD:.2f}"),
        ("unsure", f"{config.HUMAN_THRESHOLD:.2f} – {config.AI_THRESHOLD:.2f}"),
        ("high-confidence AI", f"{config.AI_THRESHOLD:.2f} – 1.00"),
    ]
