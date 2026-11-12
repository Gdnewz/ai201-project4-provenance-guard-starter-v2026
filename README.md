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

Run: `python run_attacks.py --set attack_set --label before`, written to `results/attack_run_2026-11-12_0912_before.md`. 56 attacks, nothing fixed before this run.

| ID | Family | What it was going for | Status | Guess | Held or broke |
|---|---|---|---|---|---|
| EV01 | evasion | typos raise word variety (signal two) | 200 | human | BROKE |
| EV02 | evasion | broken-up sentences raise length spread | 200 | unsure | BROKE |
| EV03 | evasion | a pasted quotation changes the shape | 200 | unsure | BROKE |
| EV04 | evasion | unusual words raise perplexity (signal one) | 200 | unsure | BROKE |
| EV05 | evasion | heavy human editing pass (both signals) | 200 | human | BROKE |
| EV06 | evasion | one very long and one very short sentence | 200 | unsure | BROKE |
| EV07 | evasion | padding with punctuation | 200 | unsure | BROKE |
| EV08 | evasion | text below the token window | 200 | human | BROKE |
| EV09 | evasion | human opening paragraph bolted on | 200 | unsure | BROKE |
| EV10 | evasion | repeated stanza structure | 200 | ai | HELD |
| FP01 | false_positive | plain, clear human writing | 200 | unsure | HELD (not accused) |
| FP02 | false_positive | human writing in a formal register | 200 | ai | BROKE |
| FP03 | false_positive | non-native English speaker writing carefully | 200 | ai | BROKE |
| FP04 | false_positive | student essay written to a rubric | 200 | ai | BROKE |
| FP05 | false_positive | technical documentation by a person | 200 | ai | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | ai | BROKE |
| FP07 | false_positive | human writing that repeats a phrase | 200 | ai | BROKE |
| FP08 | false_positive | very short genuine human submission | 200 | unsure | HELD (not accused) |
| PI01 | prompt_injection | instruction to ignore the check | 200 | unsure | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | human | BROKE |
| PI03 | prompt_injection | instruction in the writer's voice | 200 | unsure | HELD |
| PI04 | prompt_injection | hostile markup in the label text | 200 | unsure | HELD |
| PI05 | prompt_injection | injection into the audit log | 200 | unsure | HELD (log entry intact) |
| PI06 | prompt_injection | instruction plus real human text | 200 | unsure | HELD |
| MF01 | malformed | text is only whitespace | 400 | none | HELD |
| MF02 | malformed | text is a single character | 400 | none | HELD |
| MF03 | malformed | text is control characters | 200 | human | BROKE |
| MF04 | malformed | text is only punctuation | 200 | human | BROKE |
| MF05 | malformed | text is a very long single word | 200 | ai | BROKE |
| MF06 | malformed | text is emoji only | 200 | ai | BROKE |
| MF07 | malformed | text is right-to-left script (Arabic) | 200 | ai | BROKE |
| MF08 | malformed | text is 60,000 characters | 200 | ai | BROKE |
| RQ01 | malformed | no text field at all | 400 | none | HELD |
| RQ02 | malformed | no creator_id (caller recorded as `unknown`) | 200 | unsure | HELD |
| RQ03 | malformed | (check input) | 400 | none | HELD |
| RQ04 | malformed | (check input) | 400 | none | HELD |
| RQ05 | malformed | (check input) | 400 | none | HELD |
| RQ06 | malformed | creator_id is an object | 200 | human | BROKE |
| RQ07 | malformed | JSON body that is a list, not an object | 500 | none | BROKE |
| RQ08 | malformed | body is unparseable JSON (re-run alone) | 400 | none | HELD (misleading message) |
| RQ09 | malformed | body is empty (re-run alone) | 400 | none | HELD |
| RQ10 | malformed | body is form-encoded, not JSON (re-run alone) | 400 | none | HELD (misleading message) |
| RQ11 | malformed | JSON claiming to be plain text (re-run alone) | 400 | none | HELD (misleading message) |
| RQ12 | malformed | deeply nested JSON, text is an object | 400 | none | HELD (misleading reason) |
| FL01_01 | flood_same_creator | one creator_id sending 12 in a row | 200 | human | HELD |
| FL01_02 | flood_same_creator | one creator_id sending 12 in a row | 200 | human | HELD |
| FL01_03 | flood_same_creator | one creator_id sending 12 in a row | 200 | human | HELD |
| FL01_04 | flood_same_creator | one creator_id sending 12 in a row | 429 | none | HELD |
| FL01_05 | flood_same_creator | one creator_id sending 12 in a row | 429 | none | HELD |
| FL01_06 | flood_same_creator | one creator_id sending 12 in a row | 429 | none | HELD |
| FL01_07 | flood_same_creator | one creator_id sending 12 in a row | 429 | none | HELD |
| FL01_08 | flood_same_creator | one creator_id sending 12 in a row | 429 | none | HELD |
| FL01_09 | flood_same_creator | one creator_id sending 12 in a row | 429 | none | HELD |
| FL01_10 | flood_same_creator | one creator_id sending 12 in a row | 429 | none | HELD |
| FL01_11 | flood_same_creator | one creator_id sending 12 in a row | 429 | none | HELD |
| FL01_12 | flood_same_creator | one creator_id sending 12 in a row | 429 | none | HELD |

RQ08 to RQ11 first came back 429 (the limiter answered before the request reached my route, because they have no usable `creator_id` and count against my network address), so I re-ran them alone, 25 seconds apart, with `rerun_rq.py`. `CHECK` means the mark depends on an input I have not read yet.

**Ten audit log entries from the run**

```json
{"timestamp": "2026-11-12T14:12:40+00:00", "content_id": "6939d252-9c89-4705-b47c-d2ae7cd66917", "creator_id": "attacker_EV01", "guess": "human", "model_score": 0.1635, "style_score": 0.4594, "combined_score": 0.25227, "label": "We think this was probably written by a person.", "status": "decided", "ai_threshold": 0.65, "human_threshold": 0.35, "weight_model": 0.7, "weight_style": 0.3}
{"timestamp": "2026-11-12T14:12:41+00:00", "content_id": "baad685f-27cd-46da-b1f4-764b3e5d8a10", "creator_id": "attacker_EV05", "guess": "human", "model_score": 0.3212, "style_score": 0.1988, "combined_score": 0.28447999999999996, "label": "We think this was probably written by a person.", "status": "decided", "ai_threshold": 0.65, "human_threshold": 0.35, "weight_model": 0.7, "weight_style": 0.3}
{"timestamp": "2026-11-12T14:12:41+00:00", "content_id": "4bf10640-fc8c-46aa-89b8-18e085359955", "creator_id": "attacker_EV08", "guess": "human", "model_score": 0.2452, "style_score": 0.532, "combined_score": 0.33124, "label": "We think this was probably written by a person.", "status": "decided", "ai_threshold": 0.65, "human_threshold": 0.35, "weight_model": 0.7, "weight_style": 0.3}
{"timestamp": "2026-11-12T14:12:42+00:00", "content_id": "74b1d59f-a143-4b3f-bd55-cfbd6f521811", "creator_id": "attacker_FP02", "guess": "ai", "model_score": 0.7387, "style_score": 0.6706, "combined_score": 0.71827, "label": "We think this may have been written with AI. We can be wrong, so if you wrote it yourself, you can appeal and a person will take a look.", "status": "decided", "ai_threshold": 0.65, "human_threshold": 0.35, "weight_model": 0.7, "weight_style": 0.3}
{"timestamp": "2026-11-12T14:12:42+00:00", "content_id": "df572eb4-56b3-4eca-8ec7-73e932494960", "creator_id": "attacker_FP03", "guess": "ai", "model_score": 0.8051, "style_score": 0.6516, "combined_score": 0.75905, "label": "We think this may have been written with AI. We can be wrong, so if you wrote it yourself, you can appeal and a person will take a look.", "status": "decided", "ai_threshold": 0.65, "human_threshold": 0.35, "weight_model": 0.7, "weight_style": 0.3}
{"timestamp": "2026-11-12T14:12:43+00:00", "content_id": "61c7cfa3-b334-44cc-b686-529a8b31f561", "creator_id": "attacker_PI02", "guess": "human", "model_score": 0.2044, "style_score": 0.2328, "combined_score": 0.21292, "label": "We think this was probably written by a person.", "status": "decided", "ai_threshold": 0.65, "human_threshold": 0.35, "weight_model": 0.7, "weight_style": 0.3}
{"timestamp": "2026-11-12T14:12:43+00:00", "content_id": "aa103748-d28a-449b-9384-d31a38ef11aa", "creator_id": "attacker_PI05", "guess": "unsure", "model_score": 0.6401, "style_score": 0.1089, "combined_score": 0.48073999999999995, "label": "We can't tell whether this was written by a person or by AI. This isn't a judgment against you, and you can ask for a review if you'd like one.", "status": "decided", "ai_threshold": 0.65, "human_threshold": 0.35, "weight_model": 0.7, "weight_style": 0.3}
{"timestamp": "2026-11-12T14:12:44+00:00", "content_id": "2419dfc9-67c0-4243-9e39-770f4a5f5629", "creator_id": "attacker_MF05", "guess": "ai", "model_score": 0.9976, "style_score": 0.6667, "combined_score": 0.89833, "label": "We think this may have been written with AI. We can be wrong, so if you wrote it yourself, you can appeal and a person will take a look.", "status": "decided", "ai_threshold": 0.65, "human_threshold": 0.35, "weight_model": 0.7, "weight_style": 0.3}
{"timestamp": "2026-11-12T14:12:46+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "3 per 1 minute"}
{"timestamp": "2026-11-12T14:12:46+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "3 per 1 minute"}
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

FP03, a non-native English speaker writing carefully about their first month in a new country. My service told them "We think this may have been written with AI" (combined score 0.759, model 0.8051, style 0.6516). It is genuine human writing, flagged because it is plain and uses common words, which is exactly how a careful second-language writer writes. Of the eight false-positive inputs, six were labelled `ai` and two `unsure`; none came back `human`.

---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My own writing (10 essays) | At most 1 of 10 labelled `ai` | 1 of 10 (essay 1, 0.6638) | 1 of 10 (essay 1, 0.6638) | 1 of 10 (essay 1, 0.6638) | **Pass, at the limit** |
| 2. AI paragraphs (10 paragraphs) | At least 8 of 10 labelled `ai` | 6 of 10 (4 `unsure`) | 6 of 10 (4 `unsure`) | 6 of 10 (4 `unsure`) | **Miss** |
| 3. Bad requests (5) | All 5 return 400 with the service message, none 500 | 5 of 5 returned 400 | 5 of 5 returned 400 | 5 of 5 returned 400 | **Pass** (status codes) |
| 4. Appeals (10) | All 10 return `under_review` and `/log` agrees | 10 of 10, log agrees | 10 of 10, log agrees | 10 of 10, log agrees | **Pass** |
| 5. Unknown ids (5) | All 5 return 404 and the log does not change | 5 of 5, log 237 to 237 | 5 of 5, log 257 to 257 | 5 of 5, log 277 to 277 | **Pass** |

Run file: `results/run_2026-11-12_1201_before.md`, produced by `run_eval.py --label before`. Scenarios are in `scenarios.py`. `run_eval.py` only sent texts and bad bodies on its own, so I added `appeal_rows` to it, which submits the 10 essays, appeals each returned `content_id`, and then sends 5 appeals for ids that do not exist. Criteria 4 and 5 are tested by that function.

**Notes on the runs.** All three trials came back identical to four decimal places, so the model signal is deterministic on my machine and the three trials are three copies of one result, not three independent samples. Criterion 1 passes only just: essay 1 scored 0.6638 against the 0.65 threshold, and four other essays (2, 5, 7 and 8) landed in `unsure`. Criterion 3 is judged on status codes only, because `run_eval.py` records the status and not the error message text. Criterion 2 is a miss and stays a miss. I did not change the target.

**Real output from one trial** (trial 1 of `results/run_2026-11-12_1201_before.md`), pasted as text, naming the file and function that produced it:

**Criterion 1, my own writing.** Produced by `app.py::submit`, scored by `detector.py::model_signal`, `stylometry.py::style_signal` and `scoring.py::combine_signals`, labelled by `scoring.py::score_to_label`. Essay 1 (labelled `ai`) and essay 3 (labelled `human`):

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.6638,
    "model_score": 0.6774,
    "style_score": 0.632,
    "label": "We think this may have been written with AI. We can be wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "Working at a job can be draining but we all do it for the same reason,"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.31,
    "model_score": 0.2564,
    "style_score": 0.4352,
    "label": "We think this was probably written by a person.",
    "sent": "Having a relationship, especially long distant relationships can be a "
  }
]
```

**Criterion 2, AI paragraphs.** Same producers. The first paragraph (time management) is a miss at 0.579, the second (regular exercise) is labelled `ai`:

```json
[
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.579,
    "model_score": 0.7135,
    "style_score": 0.2653,
    "label": "We can't tell whether this was written by a person or by AI. This isn't a judgment against you, and you can ask for a review if you'd like one.",
    "sent": "Time management is an essential skill that can significantly improve b"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.6916,
    "model_score": 0.8745,
    "style_score": 0.2648,
    "label": "We think this may have been written with AI. We can be wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "Regular exercise offers numerous benefits for both physical and mental"
  }
]
```

**Criterion 3, bad requests.** Produced by `app.py::submit`, which returns the 400 before any signal runs. The five bodies sent were empty text, no `text` field, `text: null`, `text: 12345` and whitespace only:

```json
[
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "(empty text)"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "{\"creator_id\": \"eval_bad_missing\"}"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "{\"text\": null, \"creator_id\": \"eval_bad_null\"}"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "{\"text\": 12345, \"creator_id\": \"eval_bad_number\"}"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "   "
  }
]
```

**Criterion 4, appeals.** Produced by `app.py::appeal`, which calls `audit.py::log_appeal`. The `log_status` is read back from `GET /log` (`app.py::get_log`):

```json
[
  {
    "submit_status": 200,
    "content_id": "39080d2b-3610-4e93-94ef-0828dc81b388",
    "appeal_status": 200,
    "appeal_body": {
      "content_id": "39080d2b-3610-4e93-94ef-0828dc81b388",
      "message": "Thanks. Your appeal has been recorded and a person will review it.",
      "status": "under_review"
    },
    "log_status": "under_review"
  }
]
```

**Criterion 5, unknown ids.** Produced by `app.py::appeal`, which checks `audit.entries_for` before logging anything. The last object is the log entry count before and after the five appeals:

```json
[
  {
    "status": 404,
    "body": {
      "error": "not_found",
      "message": "we couldn't find that content_id, please check it and try again"
    }
  },
  {
    "log_entries_before": 237,
    "log_entries_after": 237
  }
]
```

**Diagnoses**

Five problems explain the broken attacks. Each group below names the stage and the mechanism, with numbers from the audit log.

### 1. Genuine human writing labelled `ai` (FP02 to FP07)

**FP03** (a non-native English speaker writing carefully), labelled `ai` at 0.759. The stage at fault is signal one, the model signal (`detector.py::model_signal`). gpt2 finds plain, careful writing with common words easy to predict, so it scored 0.8051. My combining rule gives the model signal 0.7 of the weight, so it contributes 0.5636 by itself and leaves only about 0.086 for the style signal before the score crosses the 0.65 threshold. The style signal (0.6516) leaned AI too, so nothing pulled the score back. The model signal would only have had to drop by about 0.16 to change the outcome, and the style signal would have had to drop by about 0.36. Plain writing is the model signal's blind spot, which I named in Signals and Scoring under "Signal one", and FP03 is that blind spot in the attack set.

**FP02, FP04, FP05, FP06, FP07** have the same cause as FP03: signal one, the model signal. Formal, rubric-style, technical and repetitive human writing uses predictable words in a predictable order, so gpt2 scored them 0.7387, 0.8329, 0.8005, 0.8814 and 0.8816. The style signal agreed (0.497 to 0.7491) because this writing also has even sentences and a narrow vocabulary, so the combined scores were 0.718 to 0.789, all above 0.65. The two signals did not disagree, so my combining rule had nothing to resolve. Even a style score of 0.0 would only have brought these down to between 0.517 and 0.617, which is `unsure`, not `human`, so the model signal carries these accusations. FP01 (0.6007) and FP08 (0.3638) landed in `unsure`, and FP01 was 0.05 from an accusation.

### 2. AI text labelled `human` (EV01, EV05, EV08, PI02)

**EV01, EV05, EV08 and PI02** all got through at the same stage: signal one, the model signal. Each one changed the text so that gpt2 found it harder to predict: EV01 has misspelled words it rarely sees, EV05 has an informal style with dashes and fragments, EV08 has only two short sentences, and PI02 has an odd "SYSTEM:" line at the start. The model score fell to 0.1635, 0.3212, 0.2452 and 0.2044, which read as human. My combining rule gives the model signal 0.7 of the weight, so each low score pulled the combined score down hard, to 0.25227, 0.28448, 0.33124 and 0.21292, all under the 0.35 threshold, so all four were labelled `human`. The style signal (0.4594, 0.1988, 0.532 and 0.2328) could not pull it back: the highest was EV08 at 0.532, and at a weight of 0.3 that adds only about 0.16 to the combined score. In PI02 the same AI paragraph scored 0.754 (`unsure`) without the instruction line and 0.2044 (`human`) with it.

### 3. AI text labelled `unsure` (EV02, EV03, EV04, EV06, EV07, EV09)

**EV02, EV03, EV04, EV06, EV07 and EV09** were not labelled `human`, but none reached `ai`. The model signal still leaned AI (0.5727 to 0.7042), but the style signal read all six as human (0.2399 to 0.4223), so the combined scores sat in the middle of the `unsure` band (0.488 to 0.581), below 0.65. Each attack reshapes what the style signal measures: broken-up sentences and one very long sentence change the sentence-length spread (EV02, EV06), a pasted quotation or a human paragraph adds variety (EV03, EV09), and extra semicolons raise punctuation density (EV07). EV04 changes words and so targets the model signal, and its model score was 0.6114. These attacks did not move the text across the line. The same AI paragraph with no attack scored 0.754 model and 0.3333 style, 0.6278 combined, `unsure`, in my PI02 baseline, a shortened version of it. So the style signal already read this AI-written text as human-leaning, and with a 0.7 weight on a model score of 0.754 the average still fell short of 0.65. The attacks pushed it further down.

### 4. Input the route mishandled (MF03, MF04, RQ06, RQ07, and the error messages)

**MF03** (text made of control characters) was scored as if it were writing: model 0.0, style 0.6667, combined 0.20001, labelled `human`. The stage at fault is the route. Its input check rejects empty or whitespace-only text and text too short to score, but control characters count as text, so they pass both checks and reach the model.

**MF04** (text made only of punctuation, "!!! ??? ...") also passed both checks and was scored: model 0.0112, style 1.0, combined 0.30784, labelled `human`. Same stage and same cause as MF03: the route only refuses empty or too-short text and never checks that the text contains words.

**RQ06** (`creator_id` sent as an object, `{"id": "x"}`, with real text) returned 200 and was scored `human`. The stage at fault is the route (`app.py`, line 206): `creator_id = payload.get("creator_id") or "unknown"` accepts any value that is not empty, not only a string, so an object is passed on to `audit.log_decision` and written into the caller field of the audit log.

**RQ07** (a broken input that crashed the service). The stage at fault is the route (`app.py`, line 205, in `submit`). The service returned a 500 with `AttributeError: 'list' object has no attribute 'get'`. The request body was valid JSON, but a list and not an object. `.get` only exists on a dictionary-like object, so `submit` fell over before it checked anything. My rate limiter and 429 handler already check that the payload is a dictionary, but `/submit` didn't. This is still unfixed in the "before" run.

**RQ08, RQ10, RQ11 and RQ12** were all rejected with a 400, so the route held, but with the wrong explanation. They get the reason `empty_text` and the message "did you mean to send an empty message?" even though the body was cut-off JSON (RQ08), form data (RQ10), valid JSON sent as plain text (RQ11), or a text that was an object (RQ12). The stage is the route: `get_json(silent=True)` returns nothing for all of these, so my code cannot tell "empty" from "unreadable" or "wrong type", and a writer who sent valid JSON is told they sent nothing.

### 5. Input that is not ordinary English writing, labelled `ai` (MF05 to MF08)

**MF05** (one very long word, "aaaa..."), **MF06** (emoji only), **MF07** (Arabic) and **MF08** (the same human paragraph repeated to 60,000 characters) all returned 200 and were labelled `ai`, with combined scores from 0.864 to 0.998 (model 0.9064 to 0.9976, style 0.5755 to 1.0). The stage at fault is signal one, together with the route letting them in. gpt2 finds repetition easy to predict: the repeated letter, the repeating emoji pattern and the repeated paragraph. The paragraph in MF08 is the one from FP01, which scored 0.6007 (`unsure`) once and 0.864 (`ai`) repeated. I think MF07 has the same cause, because gpt2 breaks Arabic into many small pieces that are easy to guess, but I did not test that. The route has no check on what the text contains and no maximum length, so it accepted a 60,000 character request and scored it. A writer in Arabic would be told their work "may have been written with AI".

### 6. Criterion 2: AI paragraphs labelled `unsure` (my own run)

Four of my ten AI paragraphs stayed under the 0.65 line in every trial:

| Paragraph | model_score | style_score | combined | label |
|---|---|---|---|---|
| Time management | 0.7135 | 0.2653 | 0.5790 | unsure |
| Effective communication | 0.7662 | 0.3533 | 0.6423 | unsure |
| Travel | 0.7849 | 0.1598 | 0.5974 | unsure |
| Artificial intelligence | 0.6838 | 0.2312 | 0.5480 | unsure |

All ten paragraphs had a model score of 0.6838 or higher, and the highest style score across the ten was 0.4832.

**My diagnosis:** The miss happens at the combining step (`scoring.py::combine_signals`), and the style signal (`stylometry.py::style_signal`) is what pulls these four paragraphs under the line. The model signal got every AI paragraph right, with all ten at 0.6838 or higher, but the style signal scored all ten at 0.4832 or lower, so it read clean chatbot writing as human leaning. With a weight of 0.3, a style score of 0.1598 on the travel paragraph takes about 0.19 off the combined score compared with a style score equal to its model score of 0.7849, and that drops it from about 0.78 to 0.5974, which is `unsure`. I did not test which of the three style measures (sentence length spread, vocabulary variety, punctuation density) causes the low scores. Using the model signal alone would have labelled all ten paragraphs `ai`, but it would also make the false positives in group 1 worse, because the model signal is the one that scored plain human writing like FP03 as AI, so the fix is not as simple as removing the style signal.

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