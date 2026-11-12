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

1. **A request arrives** at `POST /submit` with `text` and `creator_id`. If the caller has gone over the rate limit, the service answers 429 before anything else runs, and the rejection is written to the audit log.
2. **Input check.** If `text` is missing, empty or only spaces, the service rejects it with a 400 and the message "did you mean to send an empty message?". The rejection is written to the audit log with the reason and the `creator_id`. A rejected request never gets a `content_id`, so its entry shows only the reason and the caller.
3. **Signal one (the model signal).** `detector.model_signal(text)` runs the text through a local gpt2 model and returns a number from 0 to 1 (higher = more likely AI). Text too short to score is rejected with a 400 and logged.
4. **Signal two (the style signal).** `stylometry.style_signal(text)` measures the shape of the text and returns a number from 0 to 1 (higher = more likely AI).
5. **Combine.** `scoring.combine_signals(...)` merges the two into one score with a weighted average (0.7 model, 0.3 style).
6. **Label.** `scoring.score_to_label(...)` turns the score into a guess (`ai`, `unsure` or `human`) and the sentence the writer reads.
7. **Log and answer.** `audit.log_decision(...)` records the `content_id`, `creator_id`, both signal scores, the combined score, the guess, the label, the status `decided`, and the settings that produced the decision: `ai_threshold`, `human_threshold`, `weight_model` and `weight_style`. Recording them means a decision can be rebuilt from its log line alone, even after the settings change. The writer gets `content_id`, `guess`, `confidence`, `label`, `model_score` and `style_score` as JSON.

If the writer disagrees, they send `POST /appeal` with the `content_id` and their `reasoning`. The service checks the id exists (404 if not), records the appeal in the log, and the item becomes `under_review`. Nothing is re-checked automatically. A person looks at it.

---

## Signals and Scoring

### Signal one — the model signal

**What it measures:** How predictable the text is to a language model (gpt2, running on my own machine). The perplexity is turned into a 0 to 1 score, where higher means more likely AI.

**Why that might differ between human and AI writing:** A language model picks likely next words, so text a model wrote tends to be easy for another model to predict. Human writing is more surprising.

**What it can't see:** Who actually wrote it. Predictability isn't authorship. Plain writing with common words and short sentences (a second-language writer, a younger writer, anyone writing plainly on purpose) scores as machine-like, while ornate prose with rare words scores as human. In my own tests, a plain essay I wrote scored 0.886 and an ornate paragraph scored 0.22, and both were written by people. It also refuses text shorter than a few sentences.

### Signal two — the style signal

**What it measures:** The shape of the text without reading it. Three measures, averaged equally: sentence-length spread (standard deviation divided by the mean), vocabulary variety (unique words over total words, on the first 100 words), and punctuation density (commas, semicolons, colons, dashes and brackets per word). Each is flipped and scaled into a 0 to 1 AI-ness score.

**Why that might differ between human and AI writing:** Generated prose tends toward even, mid-length sentences and a narrower band of vocabulary. Human writing is lumpier, with short sentences next to long ones.

**What it can't see:** What the text says. Typos, broken-up sentences or a pasted quotation shift the score without changing the substance, and that is cheap to do on purpose. It is also noisy on short texts: my ornate two-sentence paragraph has two sentences of the same length, so its spread measure read it as even-paced and the style score leaned AI (0.42) even though a person wrote it. The cutoff numbers inside `style_signal` are starting guesses and are not tuned yet.

### The combining rule

**The rule:** A weighted average of the two signals, weighted toward the model signal: `combined = 0.7 × model_score + 0.3 × style_score`. When the two disagree, the result lands between them, closer to the model signal.

**The numbers:** 0.7 model, 0.3 style (set in `config.py`). Thresholds: below 0.35 is "human", 0.35 to 0.65 is "unsure", above 0.65 is "AI". I trust the model signal more because it measures predictability, which is closer to what I'm trying to detect, and the style signal is easy to fool. The cost is that the model signal's blind spot (plain writing) counts for more in the final score.

**Where it lives:** `scoring.py::combine_signals`

**A case where my two signals split, and what my rule does with it:**

I submitted a plain 134-character essay I wrote myself ("I went to the store yesterday..."). The model signal scored it 0.886 (AI) and the style signal scored it 0.3167 (human). My rule combined them to 0.7152, which is above the 0.65 threshold, so the writer is told the text may have been written with AI. The style signal pulled the score down by about 0.17, but not enough to cross the threshold. That's the false positive this project is about, and it's why the appeal path exists. The opposite split was the ornate paragraph: model 0.22 (human), style 0.4216 (leaning AI), combined 0.2805, labelled human.

---

## Label Variants

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.35 | We think this was probably written by a person. |
| unsure | 0.35 – 0.65 | We can't tell whether this was written by a person or by AI. This isn't a judgment against you, and you can ask for a review if you'd like one. |
| high-confidence AI | 0.65 – 1.00 | We think this may have been written with AI. We can be wrong, so if you wrote it yourself, you can appeal and a person will take a look. |

**Why I worded the "unsure" one this way:**

The person reading it may well have written every word themselves, so it admits the system can't tell without suggesting they did anything wrong. It says outright that it isn't a judgment against them, and it offers a review so they have somewhere to go.

---

## Sample Run

**A submission**

```bash
$ curl.exe -X POST http://127.0.0.1:5000/submit -H "Content-Type: application/json" -d '{"text": "I went to the store yesterday. It was crowded, so I waited in line for a long time. When I got home, I made dinner and watched a show.", "creator_id": "goody"}'
```

```json
{
  "confidence": 0.7152,
  "content_id": "90d94a4b-cbbf-4e34-9b19-afd4f3cc72a2",
  "creator_id": "goody",
  "guess": "ai",
  "label": "We think this may have been written with AI. We can be wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
  "model_score": 0.886,
  "style_score": 0.3167,
  "text_length": 134
}
```

**An appeal**

```bash
$ curl.exe -X POST http://127.0.0.1:5000/appeal -H "Content-Type: application/json" -d '{"content_id": "90d94a4b-cbbf-4e34-9b19-afd4f3cc72a2", "reasoning": "I wrote this myself."}'
```

```json
PASTE YOUR REAL APPEAL RESPONSE HERE
```

**What the log shows afterwards**

```bash
$ curl.exe "http://127.0.0.1:5000/log?limit=3"
```

```json
PASTE YOUR REAL LOG OUTPUT HERE
```

---

## How I Used AI

**Moment 1**

- *What I asked for:* A draft of my Milestone 1 trace: the path a submission takes, the two signals with their blind spots, the false-positive case, and the endpoint shapes.
- *What came back:* A full draft, but it guessed some details, including the file names, the 0.80 and 0.40 thresholds and the error codes.
- *What I changed:* I checked it against `running.md`, `app.py` and `config.py`, corrected the thresholds to 0.35 and 0.65, added `model_score` and `style_score` to the response shape, chose my own weights (0.7 and 0.3) and my own rule for empty text (reject with a 400), and wrote my five criteria in the form "given X, the system returns Y".

**Moment 2**

- *What I asked for:* The three style measures and `style_signal` in `stylometry.py`.
- *What came back:* Working code for sentence-length spread, vocabulary variety and punctuation density, with cutoff numbers (0.7, 0.55 to 0.85, 0.12) that were starting guesses.
- *What I changed:* I ran it on my own texts and checked that I got the same numbers (style_signal 0.3167 on my plain essay), then wired it into `/submit` and confirmed the combined score matched my hand calculation (0.7152). The cutoffs are still untuned. <!-- EDIT: add anything you change after tuning them -->

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 3 per minute, 40 per day

**Why those numbers and not others:**

I chose 3 submissions per minute and 40 per day. A real writer checks a piece, reads the result, and edits before sending the next one, so three a minute leaves room for normal use. The limit protects the scoring step from a script that sends text as fast as it can, which my flood test showed: 3 went through and 12 were blocked (`results/flood_2026-11-04_2123.md`). The cost is that a writer with several short pieces to check at once can be blocked for a minute, and a daily cap of 40 stops someone with a big batch. I accept that because a short wait costs a writer less than an open scoring endpoint costs the service. These numbers are my judgment, not measured, and I would change them if real users were blocked often.

**What a caller counts as:**

I count each `creator_id` as one caller, falling back to the network address when a request has none. This protects a shared network, like a school or household, from being blocked because one person on it sent too much, since each writer gets their own limit. The cost is that someone who wants to flood the service can send each request with a new `creator_id` and never reach the limit. I accept that for now because the limit still stops a simple script, and because `creator_id` is a stand-in for an account I don't check. A real deployment would tie it to a verified login or add a limit by network address as well.

**The run of status codes when I pushed past it:**

```
200 200 200 429 429 429 429 429 429 429 429 429 429 429 429
```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

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



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

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