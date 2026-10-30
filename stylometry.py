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


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


def _clamp(x: float) -> float:
    """Keep a number between 0 and 1."""
    return max(0.0, min(1.0, x))


# ── The three measures ───────────────────────────────────────────────────────

def sentence_length_spread(text: str) -> float:
    """
    Standard deviation of sentence length (in words) divided by the mean.

    Scale: 0 upward, usually 0 to about 1. HIGHER = more varied = more human.
    Fewer than 2 sentences returns 0.0 (no spread to measure), which leans AI.
    """
    lengths = [len(words(s)) for s in sentences(text)]
    lengths = [n for n in lengths if n > 0]
    if len(lengths) < 2:
        return 0.0
    return statistics.stdev(lengths) / statistics.mean(lengths)


def type_token_ratio(text: str) -> float:
    """
    Unique words over total words, measured on the FIRST 100 WORDS only.

    Scale: 0 to 1. HIGHER = more varied vocabulary = more human.
    The 100-word window is there because the ratio falls as text gets longer,
    so without it a long text would look machine-like just for being long.
    """
    w = words(text)[:100]
    if not w:
        return 0.0
    return len(set(w)) / len(w)


def punctuation_density(text: str) -> float:
    """
    Commas, semicolons, colons, dashes and brackets per word.
    Full stops are ignored (every text has them).

    Scale: 0 upward, usually 0 to about 0.2. HIGHER = more punctuation
    variety = more human.
    """
    w = words(text)
    if not w:
        return 0.0
    marks = re.findall(r"[,;:()\u2014\u2013-]", text)
    return len(marks) / len(w)


# ── Combining them ───────────────────────────────────────────────────────────

def style_signal(text: str) -> float:
    """
    The style signal as a 0–1 score. **Higher means more likely AI.**

    Each measure points toward "human" when it is HIGH, so each is flipped
    into an AI-ness score and scaled to 0–1 before averaging:

        spread       0.7 or more -> 0 (human);  0 -> 1 (AI)
        vocabulary   0.85 or more -> 0 (human); 0.55 or less -> 1 (AI)
        punctuation  0.12 or more -> 0 (human); 0 -> 1 (AI)

    The three are averaged equally. The cut-off numbers (0.7, 0.55/0.85, 0.12)
    are starting guesses, not facts. Tune them against the four calibration
    inputs from Milestone 4.
    """
    spread_ai = 1 - _clamp(sentence_length_spread(text) / 0.7)
    vocab_ai = _clamp((0.85 - type_token_ratio(text)) / 0.30)
    punct_ai = 1 - _clamp(punctuation_density(text) / 0.12)
    return round((spread_ai + vocab_ai + punct_ai) / 3, 4)


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
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")