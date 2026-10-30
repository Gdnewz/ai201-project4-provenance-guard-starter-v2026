# Milestone 1: Trace a submission

## 1. The path

Example: a writer sends `POST /submit` with `text` and `creator_id`.

1. **Request arrives** at `/submit`. In: JSON with `text`, `creator_id`.
2. **Input check.** If `text` is missing or empty, reject with **400** and the message "did you mean to send an empty message?". The path ends here.
3. **Signal 1:** `detector.model_signal(text)`. In: text. Out: number 0 to 1 (higher = more likely AI).
4. **Signal 2:** `stylometry.style_signal(text)`. In: text. Out: number 0 to 1.
5. **Combine:** `scoring.combine_signals(...)`. In: the two signal numbers. Out: one score, a weighted average: 0.7 model + 0.3 style. One number is needed because a label comes from comparing a single score against cutoffs.
6. **Label:** `scoring.score_to_label(...)`. In: the combined score. Out: a label. Below 0.35 = likely human, 0.35 to 0.65 = unsure, above 0.65 = likely AI.
7. **Log:** `audit.log_decision(...)`. Records `content_id`, both signal scores, the combined score and the label.
8. **Response:** returns JSON to the writer.

## 2. The two signals

**Model signal (`detector.py`)**
- Measures: how predictable the text is to a language model. Easier to predict means more likely AI.
- Can't see: who wrote it. Plain writing with common words and short sentences scores as machine-like, so second-language and younger writers get wrongly flagged.

**Style signal (`stylometry.py`)**
- Measures: the shape of the text (sentence-length variety, word variety, punctuation).
- Can't see: what the text says, because it can't read. Typos, broken-up sentences or a pasted quotation shift it without changing the meaning, and that is cheap to do on purpose.

**Why two:** where one signal is blind, the other may still see.

**Weights:** model 0.7, style 0.3. I trust the model signal more because it measures predictability, which is closer to what I'm detecting, and the style signal is easy to fool. The cost: the model signal's blind spot (plain writing) matters more in the final score.

## 3. The false positive

- **Writer:** someone writing in a second language. They use common words and short, plain sentences.
- **Score:** high, about 0.7, above the 0.65 threshold.
- **Label the writer sees:** "Likely AI". It says "likely", not "is", so it is not stated as fact.
- **What they do next:** send `POST /appeal` with `content_id` and `reasoning`. The service checks the id exists, records the appeal, and the item becomes `under_review`. Nothing is re-checked automatically. A human looks at it later.
- **Why they have the least room to argue back:** the people most likely to be wrongly flagged are the ones with the fewest words to defend themselves with, so the appeal path has to exist.

## 4. Endpoint shapes

**`POST /submit`**
- In: `text` (string, required), `creator_id` (string, required)
- Out: `content_id`, `guess`, `confidence`, `label`, `model_score`, `style_score`
- Empty or missing `text`: 400, "did you mean to send an empty message?"

**`POST /appeal`**
- In: `content_id` (string, required), `reasoning` (string, required)
- Steps: check the id exists (`audit.entries_for`), record it (`audit.log_appeal`), confirm to the writer
- Out: `content_id`, `status: "under_review"`, a confirmation message
- Unknown `content_id`: 404 with a clear message, so a typo never fails silently