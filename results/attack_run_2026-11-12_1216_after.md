# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-12 12:16
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `abcfc534-4ad8-44f1-b298-286afa833bac` | human | 0.252 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `b04a25f0-e3af-4bf9-bb87-12fe319efe6d` | unsure | 0.488 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `e0685b76-e88e-4e28-8eb3-e200aaafe805` | unsure | 0.564 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `e4346c81-2b18-400b-bee5-638d5723efba` | unsure | 0.555 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `e78665eb-1da2-4bef-986a-f87bd3b402e5` | human | 0.284 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `503154fe-2d60-4240-96f4-f82caeb38d2b` | unsure | 0.507 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `a7849ded-f039-40c4-993b-222e2ecf2033` | unsure | 0.536 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `61a84643-0a58-4253-93d7-5a8b3deb6896` | human | 0.331 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `0e33a746-cd17-4104-abdc-ae345f56c977` | unsure | 0.581 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `2db85c9f-c29e-429b-a19d-df834c6305d9` | ai | 0.929 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `7fa1dd78-6823-436a-bc9d-2eaf398c6983` | unsure | 0.601 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `c503b675-4676-4242-ba63-16bc5d20eb98` | ai | 0.718 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `6bbbacc8-6b3a-4670-8f04-cca1cf544946` | ai | 0.759 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `89c4095b-c8fc-4480-8625-1050819366fd` | ai | 0.732 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `445c43d5-2be8-4750-848e-5d0fb5f45a63` | ai | 0.785 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `dad89937-cc43-4fac-b571-8f42aec9a583` | ai | 0.768 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `b9ca8b61-04cb-4d10-8aab-cd58ecd37114` | ai | 0.789 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `34f4ffbb-114c-49f6-99ad-f6f9796fd87f` | unsure | 0.364 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `4d1628bd-433e-4124-a66b-268b05d79815` | unsure | 0.429 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `40475450-04c9-4c73-adb7-6a3052158543` | human | 0.213 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `e3f1fcf8-48ef-464d-ab17-d5c334648534` | unsure | 0.521 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `4cd4c161-d822-4771-a80c-64e4ccdb4932` | unsure | 0.428 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `1233b829-d775-451d-870e-38d28c22c47f` | unsure | 0.481 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `ccba2ec9-9250-4837-9366-cee38719c078` | unsure | 0.552 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `f5d4af20-3950-49f5-b6fd-ca1b54eb64ba` | human | 0.200 |  |
| MF04 | malformed | text is only punctuation | 400 | `—` | — | — |  |
| MF05 | malformed | text is a very long single word | 200 | `da3890e8-2553-45bc-9999-b6b73357b24a` | ai | 0.898 |  |
| MF06 | malformed | text is emoji only | 400 | `—` | — | — |  |
| MF07 | malformed | text is right-to-left script | 200 | `38d035e0-df32-4a73-a986-3e03bc74f86a` | ai | 0.934 |  |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 200 | `f91dd372-460e-428b-a84b-1dfbfbbfd301` | unsure | 0.368 |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 429 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 429 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `e8e1fe2f-0530-4a59-9f7d-d35c5b2141a1` | human | 0.220 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c74fa353-45d3-44cf-a5ea-34a8d7bcc0c5` | human | 0.220 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `948fe082-2b80-4746-9b7e-d8283a683f05` | human | 0.220 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
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
| `malformed` | 20 | 0 | 20 |
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
  "content_id": "abcfc534-4ad8-44f1-b298-286afa833bac",
  "creator_id": "attacker_EV01",
  "guess": "human",
  "confidence": 0.2523,
  "model_score": 0.1635,
  "style_score": 0.4594,
  "label": "We think this was probably written by a person.",
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
  "content_id": "b04a25f0-e3af-4bf9-bb87-12fe319efe6d",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.488,
  "model_score": 0.5943,
  "style_score": 0.2399,
  "label": "We can't tell whether this was written by a person or by AI. This isn't a judgment against you, and you can ask for a review if you'd like one.",
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
  "content_id": "e0685b76-e88e-4e28-8eb3-e200aaafe805",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5637,
  "model_score": 0.6662,
  "style_score": 0.3245,
  "label": "We can't tell whether this was written by a person or by AI. This isn't a judgment against you, and you can ask for a review if you'd like one.",
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
  "content_id": "e4346c81-2b18-400b-bee5-638d5723efba",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.5547,
  "model_score": 0.6114,
  "style_score": 0.4223,
  "label": "We can't tell whether this was written by a person or by AI. This isn't a judgment against you, and you can ask for a review if you'd like one.",
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
  "content_id": "e78665eb-1da2-4bef-986a-f87bd3b402e5",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.2845,
  "model_score": 0.3212,
  "style_score": 0.1988,
  "label": "We think this was probably written by a person.",
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
  "content_id": "503154fe-2d60-4240-96f4-f82caeb38d2b",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.5071,
  "model_score": 0.5727,
  "style_score": 0.3539,
  "label": "We can't tell whether this was written by a person or by AI. This isn't a judgment against you, and you can ask for a review if you'd like one.",
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
  "content_id": "a7849ded-f039-40c4-993b-222e2ecf2033",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.536,
  "model_score": 0.5862,
  "style_score": 0.4187,
  "label": "We can't tell whether this was written by a person or by AI. This isn't a judgment against you, and you can ask for a review if you'd like one.",
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
  "content_id": "61a84643-0a58-4253-93d7-5a8b3deb6896",
  "creator_id": "attacker_EV08",
  "guess": "human",
  "confidence": 0.3312,
  "model_score": 0.2452,
  "style_score": 0.532,
  "label": "We think this was probably written by a person.",
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
  "content_id": "0e33a746-cd17-4104-abdc-ae345f56c977",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.5811,
  "model_score": 0.7042,
  "style_score": 0.2939,
  "label": "We can't tell whether this was written by a person or by AI. This isn't a judgment against you, and you can ask for a review if you'd like one.",
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
  "content_id": "2db85c9f-c29e-429b-a19d-df834c6305d9",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.9292,
  "model_score": 0.9792,
  "style_score": 0.8124,
  "label": "We think this may have been written with AI. We can be wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
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
  "content_id": "7fa1dd78-6823-436a-bc9d-2eaf398c6983",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.6007,
  "model_score": 0.6175,
  "style_score": 0.5615,
  "label": "We can't tell whether this was written by a person or by AI. This isn't a judgment against you, and you can ask for a review if you'd like one.",
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
  "content_id": "c503b675-4676-4242-ba63-16bc5d20eb98",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.7183,
  "model_score": 0.7387,
  "style_score": 0.6706,
  "label": "We think this may have been written with AI. We can be wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
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
  "content_id": "6bbbacc8-6b3a-4670-8f04-cca1cf544946",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.7591,
  "model_score": 0.8051,
  "style_score": 0.6516,
  "label": "We think this may have been written with AI. We can be wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
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
  "content_id": "89c4095b-c8fc-4480-8625-1050819366fd",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.7321,
  "model_score": 0.8329,
  "style_score": 0.497,
  "label": "We think this may have been written with AI. We can be wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
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
  "content_id": "445c43d5-2be8-4750-848e-5d0fb5f45a63",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.7851,
  "model_score": 0.8005,
  "style_score": 0.7491,
  "label": "We think this may have been written with AI. We can be wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
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
  "content_id": "dad89937-cc43-4fac-b571-8f42aec9a583",
  "creator_id": "attacker_FP06",
  "guess": "ai",
  "confidence": 0.7683,
  "model_score": 0.8814,
  "style_score": 0.5045,
  "label": "We think this may have been written with AI. We can be wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
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
  "content_id": "b9ca8b61-04cb-4d10-8aab-cd58ecd37114",
  "creator_id": "attacker_FP07",
  "guess": "ai",
  "confidence": 0.7889,
  "model_score": 0.8816,
  "style_score": 0.5725,
  "label": "We think this may have been written with AI. We can be wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
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
  "content_id": "34f4ffbb-114c-49f6-99ad-f6f9796fd87f",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.3638,
  "model_score": 0.3223,
  "style_score": 0.4605,
  "label": "We can't tell whether this was written by a person or by AI. This isn't a judgment against you, and you can ask for a review if you'd like one.",
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
  "content_id": "4d1628bd-433e-4124-a66b-268b05d79815",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.4291,
  "model_score": 0.4625,
  "style_score": 0.3511,
  "label": "We can't tell whether this was written by a person or by AI. This isn't a judgment against you, and you can ask for a review if you'd like one.",
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
  "content_id": "40475450-04c9-4c73-adb7-6a3052158543",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.2129,
  "model_score": 0.2044,
  "style_score": 0.2328,
  "label": "We think this was probably written by a person.",
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
  "content_id": "e3f1fcf8-48ef-464d-ab17-d5c334648534",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5215,
  "model_score": 0.5943,
  "style_score": 0.3518,
  "label": "We can't tell whether this was written by a person or by AI. This isn't a judgment against you, and you can ask for a review if you'd like one.",
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
  "content_id": "4cd4c161-d822-4771-a80c-64e4ccdb4932",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.4278,
  "model_score": 0.4998,
  "style_score": 0.2599,
  "label": "We can't tell whether this was written by a person or by AI. This isn't a judgment against you, and you can ask for a review if you'd like one.",
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
  "content_id": "1233b829-d775-451d-870e-38d28c22c47f",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.4807,
  "model_score": 0.6401,
  "style_score": 0.1089,
  "label": "We can't tell whether this was written by a person or by AI. This isn't a judgment against you, and you can ask for a review if you'd like one.",
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
  "content_id": "ccba2ec9-9250-4837-9366-cee38719c078",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5524,
  "model_score": 0.5583,
  "style_score": 0.5387,
  "label": "We can't tell whether this was written by a person or by AI. This isn't a judgment against you, and you can ask for a review if you'd like one.",
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
  "content_id": "f5d4af20-3950-49f5-b6fd-ca1b54eb64ba",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.2,
  "model_score": 0.0,
  "style_score": 0.6667,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
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
  "content_id": "da3890e8-2553-45bc-9999-b6b73357b24a",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.8983,
  "model_score": 0.9976,
  "style_score": 0.6667,
  "label": "We think this may have been written with AI. We can be wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF06",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
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
  "content_id": "38d035e0-df32-4a73-a986-3e03bc74f86a",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.9345,
  "model_score": 0.9064,
  "style_score": 1.0,
  "label": "We think this may have been written with AI. We can be wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
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
  "content_id": "f91dd372-460e-428b-a84b-1dfbfbbfd301",
  "creator_id": null,
  "guess": "unsure",
  "confidence": 0.3677,
  "model_score": 0.2395,
  "style_score": 0.6667,
  "label": "We can't tell whether this was written by a person or by AI. This isn't a judgment against you, and you can ask for a review if you'd like one.",
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
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
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

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
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

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
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
  "content_id": "e8e1fe2f-0530-4a59-9f7d-d35c5b2141a1",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2201,
  "model_score": 0.0287,
  "style_score": 0.6667,
  "label": "We think this was probably written by a person.",
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
  "content_id": "c74fa353-45d3-44cf-a5ea-34a8d7bcc0c5",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2201,
  "model_score": 0.0287,
  "style_score": 0.6667,
  "label": "We think this was probably written by a person.",
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
  "content_id": "948fe082-2b80-4746-9b7e-d8283a683f05",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2201,
  "model_score": 0.0287,
  "style_score": 0.6667,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
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

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
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
