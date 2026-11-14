"""
Signal one: the model signal.

This is the signal that "reads the text for meaning". It runs a language model
on your own machine and asks one question: **how predictable is this text?**

The idea is the one every AI-detection product is built on. A language model
writes by repeatedly picking a likely next word, so text a model produced tends
to be text a model finds easy to predict. Human writing wanders more — odd word
choices, abrupt turns, the specific rather than the typical.

The measure is called **perplexity**. Low perplexity means "I could have
guessed this"; high perplexity means "that surprised me". This module turns
that into a 0–1 score where **higher means more likely AI**.

    from detector import model_signal
    score = model_signal("some text")     # 0.0 human-ish … 1.0 AI-ish

Everything runs locally. No account, no key, no card.

⚠️ **The blind spot, which you have to name in Milestone 1.**

Predictability is not the same thing as authorship. What this signal actually
rewards is **common words in short, ordinary sentences** — and plenty of real
people write that way.

Someone writing in a second language, sticking to vocabulary they're sure of.
A younger writer. Anyone writing plainly on purpose. Measured against gpt2,
writing like that scores about as machine-like as machine writing does.

The reverse trips people up too: dense, ornate prose full of rare words often
scores as *human* on this signal, because rare words are exactly what a
language model fails to predict. Formality on its own doesn't decide it.

So the writers this signal is most likely to accuse are the ones with the
least room to argue back. That is structural rather than a bug you can fix,
and it is the person Milestone 1 asks you to follow through your service.

Don't take that on trust — it's a claim you can check. Milestone 4 has you run
four calibration inputs. Add a plainly-written human paragraph to them and see
for yourself where it lands.
"""

import math

import config

_model = None
_tokenizer = None


class DetectorUnavailable(RuntimeError):
    """The model couldn't be loaded — no download yet, or no disk."""


def _load_tokenizer():
    """
    Load only the tokenizer and keep it. It is small and quick, so input can be
    checked for length BEFORE the slow model load (capstone criterion 5).
    """
    global _tokenizer
    if _tokenizer is not None:
        return _tokenizer

    try:
        from transformers import AutoTokenizer
    except ImportError as exc:
        raise DetectorUnavailable(
            f"transformers isn't installed ({exc}).\n"
            f"Run: pip install -r requirements.txt"
        ) from exc

    try:
        _tokenizer = AutoTokenizer.from_pretrained(config.DETECTOR_MODEL)
    except Exception as exc:  # noqa: BLE001
        raise DetectorUnavailable(
            f"Couldn't load the tokenizer for '{config.DETECTOR_MODEL}': {exc}\n"
            f"The first run downloads about 550 MB — check your connection and "
            f"that you have disk space free."
        ) from exc

    return _tokenizer


def _load():
    """Load the model once and keep it. First call downloads ~550 MB."""
    global _model
    if _model is not None:
        return _model, _tokenizer

    try:
        import torch  # noqa: F401
        from transformers import AutoModelForCausalLM
    except ImportError as exc:
        raise DetectorUnavailable(
            f"transformers or torch isn't installed ({exc}).\n"
            f"Run: pip install -r requirements.txt"
        ) from exc

    tokenizer = _load_tokenizer()

    try:
        _model = AutoModelForCausalLM.from_pretrained(config.DETECTOR_MODEL)
        _model.eval()
    except Exception as exc:  # noqa: BLE001
        raise DetectorUnavailable(
            f"Couldn't load '{config.DETECTOR_MODEL}': {exc}\n"
            f"The first run downloads about 550 MB — check your connection and "
            f"that you have disk space free."
        ) from exc

    return _model, tokenizer


def perplexity(text: str) -> float:
    """
    How surprised the model is by this text. Lower means more predictable.

    Returns a positive number. Typical values land roughly between 10 and 200,
    but that range shifts with topic and length, which is one reason the raw
    number isn't what you score on.
    """
    # Tokenize first, with the tokenizer alone, so text that is too short is
    # refused BEFORE the model loads. Same rule as before, checked earlier.
    tokenizer = _load_tokenizer()
    ids = tokenizer(
        text,
        truncation=True,
        max_length=config.DETECTOR_MAX_TOKENS,
    )["input_ids"]

    # Two tokens is not enough to be surprised by anything.
    if len(ids) < 3:
        raise ValueError("Text is too short to score — a few sentences at least.")

    import torch

    model, _ = _load()
    input_ids = torch.tensor([ids])

    with torch.no_grad():
        output = model(input_ids, labels=input_ids)

    # The model's loss here IS mean negative log-likelihood per token.
    return float(math.exp(output.loss.item()))


def model_signal(text: str) -> float:
    """
    The signal, as a 0–1 score. **Higher means more likely AI.**

    Perplexity is unbounded and roughly log-distributed, so it gets squashed
    onto 0–1 rather than clipped. The midpoint below is the perplexity that
    maps to 0.5 — text this surprising is a coin flip.

    You may want to move that midpoint once you've run the four calibration
    inputs in Milestone 4 and seen what your own text actually scores. If you
    do, say so in your README: it's a scoring decision, not a detail.
    """
    ppl = perplexity(text)

    midpoint = 45.0    # perplexity that scores 0.5
    steepness = 1.6    # how sharply the score moves either side of it

    # Logistic on log-perplexity. Low perplexity -> high AI score.
    score = 1.0 / (1.0 + (ppl / midpoint) ** steepness)
    return round(min(max(score, 0.0), 1.0), 4)


def prepare() -> None:
    """
    Import transformers and load the tokenizer now, at server start, so the
    first request does not pay for them (about 6 s on my laptop). The model
    weights stay lazy, so model_warm still separates cold from warm.
    """
    _load_tokenizer()


def warm_up() -> str:
    """Load the model without scoring anything. Run this before class."""
    _load()
    return f"{config.DETECTOR_MODEL} loaded and ready."


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = (
            "The implementation of the proposed framework requires careful "
            "consideration of several key factors. First, it is important to "
            "note that the system must be able to handle a wide variety of "
            "different inputs. Additionally, the overall performance of the "
            "solution depends on a number of important variables."
        )
        print("(no text given — scoring a sample)\n")

    print(f"Loading {config.DETECTOR_MODEL} (first run downloads ~550 MB)…")
    print(f"perplexity     {perplexity(text):.1f}")
    print(f"model_signal   {model_signal(text):.4f}   (higher = more likely AI)")