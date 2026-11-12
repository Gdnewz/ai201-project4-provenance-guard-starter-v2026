# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-12 09:12
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
| EV01 | evasion | signal two: typos raise word variety | 200 | `6939d252-9c89-4705-b47c-d2ae7cd66917` | human | 0.252 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `cccb83db-cd27-4d87-ab65-c13dd18b3b26` | unsure | 0.488 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `60727376-87fd-4f69-a7a6-9096e3a77d6d` | unsure | 0.564 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `e5a8d494-f54d-424f-b7d2-c7ffd9842eb3` | unsure | 0.555 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `baad685f-27cd-46da-b1f4-764b3e5d8a10` | human | 0.284 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `14be7fb1-10f7-4db5-9c34-2ac34c7f3c17` | unsure | 0.507 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `20a51c61-6c46-4890-bbcb-dd2529cb1078` | unsure | 0.536 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `4bf10640-fc8c-46aa-89b8-18e085359955` | human | 0.331 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `ba62d716-aa25-46de-92c9-624b20b87654` | unsure | 0.581 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `80917858-f9a3-4609-a8a5-8d936f397d98` | ai | 0.929 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `a4d93ed2-f208-492e-8cdc-106c1782664c` | unsure | 0.601 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `74b1d59f-a143-4b3f-bd55-cfbd6f521811` | ai | 0.718 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `df572eb4-56b3-4eca-8ec7-73e932494960` | ai | 0.759 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `884f0e84-9d3e-4ff8-961a-dae6ee1abf82` | ai | 0.732 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `58be3733-6e45-43d0-a153-6aea67ef1036` | ai | 0.785 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `e014e09a-876d-4f5d-aaf5-14b0459d1537` | ai | 0.768 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `cf81ddde-e0d5-4c2f-9552-8878b774031f` | ai | 0.789 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `fd25cd22-f570-44e4-a625-2d23cfd0df74` | unsure | 0.364 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `9c06bc1d-d785-43be-9aa9-203030fe67ae` | unsure | 0.429 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `61c7cfa3-b334-44cc-b686-529a8b31f561` | human | 0.213 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `fd1d0658-6819-4e2c-a47d-086e5fb2cc61` | unsure | 0.521 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `4b15b5f1-2b58-462f-b891-78a9d91d1988` | unsure | 0.428 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `aa103748-d28a-449b-9384-d31a38ef11aa` | unsure | 0.481 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `9850a7fb-bea0-47de-a7e6-5915f623ba5b` | unsure | 0.552 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `cfee3c51-8acf-413d-afb8-5ae634b846d0` | human | 0.200 |  |
| MF04 | malformed | text is only punctuation | 200 | `54bbd696-6355-4373-a216-41ee885ed747` | human | 0.308 |  |
| MF05 | malformed | text is a very long single word | 200 | `2419dfc9-67c0-4243-9e39-770f4a5f5629` | ai | 0.898 |  |
| MF06 | malformed | text is emoji only | 200 | `f2c727bf-c25c-4ed5-872b-c3e8440d91bc` | ai | 0.998 |  |
| MF07 | malformed | text is right-to-left script | 200 | `5a6f0397-c3e9-4f77-960f-73fa492cd763` | ai | 0.934 |  |
| MF08 | malformed | text is 60,000 characters | 200 | `c3ad42fc-78d9-4327-98ce-7ff1ce3c706a` | ai | 0.864 |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 200 | `2b8b4ae9-add3-4bd4-b642-a109d4fde102` | unsure | 0.368 |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 200 | `7d22f6b4-e6c7-4db6-b854-42a74665fe5d` | human | 0.234 |  |
| RQ07 | malformed | body is a JSON array, not an object | 500 | `—` | — | — | BROKE |
| RQ08 | malformed | body is unparseable JSON | 429 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 429 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `1d72e054-d8d8-4b90-8e4a-d1fd296a4baa` | human | 0.220 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `8c5f721e-d840-4041-bb14-3c5937f4e138` | human | 0.220 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `f6086ebc-dbce-408b-9738-8b679a6e536b` | human | 0.220 |  |
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
  "content_id": "6939d252-9c89-4705-b47c-d2ae7cd66917",
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
  "content_id": "cccb83db-cd27-4d87-ab65-c13dd18b3b26",
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
  "content_id": "60727376-87fd-4f69-a7a6-9096e3a77d6d",
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
  "content_id": "e5a8d494-f54d-424f-b7d2-c7ffd9842eb3",
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
  "content_id": "baad685f-27cd-46da-b1f4-764b3e5d8a10",
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
  "content_id": "14be7fb1-10f7-4db5-9c34-2ac34c7f3c17",
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
  "content_id": "20a51c61-6c46-4890-bbcb-dd2529cb1078",
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
  "content_id": "4bf10640-fc8c-46aa-89b8-18e085359955",
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
  "content_id": "ba62d716-aa25-46de-92c9-624b20b87654",
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
  "content_id": "80917858-f9a3-4609-a8a5-8d936f397d98",
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
  "content_id": "a4d93ed2-f208-492e-8cdc-106c1782664c",
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
  "content_id": "74b1d59f-a143-4b3f-bd55-cfbd6f521811",
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
  "content_id": "df572eb4-56b3-4eca-8ec7-73e932494960",
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
  "content_id": "884f0e84-9d3e-4ff8-961a-dae6ee1abf82",
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
  "content_id": "58be3733-6e45-43d0-a153-6aea67ef1036",
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
  "content_id": "e014e09a-876d-4f5d-aaf5-14b0459d1537",
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
  "content_id": "cf81ddde-e0d5-4c2f-9552-8878b774031f",
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
  "content_id": "fd25cd22-f570-44e4-a625-2d23cfd0df74",
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
  "content_id": "9c06bc1d-d785-43be-9aa9-203030fe67ae",
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
  "content_id": "61c7cfa3-b334-44cc-b686-529a8b31f561",
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
  "content_id": "fd1d0658-6819-4e2c-a47d-086e5fb2cc61",
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
  "content_id": "4b15b5f1-2b58-462f-b891-78a9d91d1988",
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
  "content_id": "aa103748-d28a-449b-9384-d31a38ef11aa",
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
  "content_id": "9850a7fb-bea0-47de-a7e6-5915f623ba5b",
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
  "content_id": "cfee3c51-8acf-413d-afb8-5ae634b846d0",
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
  "status": 200,
  "content_id": "54bbd696-6355-4373-a216-41ee885ed747",
  "creator_id": "attacker_MF04",
  "guess": "human",
  "confidence": 0.3078,
  "model_score": 0.0112,
  "style_score": 1.0,
  "label": "We think this was probably written by a person.",
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
  "content_id": "2419dfc9-67c0-4243-9e39-770f4a5f5629",
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
  "status": 200,
  "content_id": "f2c727bf-c25c-4ed5-872b-c3e8440d91bc",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.9978,
  "model_score": 0.9969,
  "style_score": 1.0,
  "label": "We think this may have been written with AI. We can be wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
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
  "content_id": "5a6f0397-c3e9-4f77-960f-73fa492cd763",
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
  "status": 200,
  "content_id": "c3ad42fc-78d9-4327-98ce-7ff1ce3c706a",
  "creator_id": "attacker_MF08",
  "guess": "ai",
  "confidence": 0.864,
  "model_score": 0.9876,
  "style_score": 0.5755,
  "label": "We think this may have been written with AI. We can be wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
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
  "content_id": "2b8b4ae9-add3-4bd4-b642-a109d4fde102",
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
  "status": 200,
  "content_id": "7d22f6b4-e6c7-4db6-b854-42a74665fe5d",
  "creator_id": {
    "id": "x"
  },
  "guess": "human",
  "confidence": 0.2344,
  "model_score": 0.0492,
  "style_score": 0.6667,
  "label": "We think this was probably written by a person.",
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
  "content_id": "1d72e054-d8d8-4b90-8e4a-d1fd296a4baa",
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
  "content_id": "8c5f721e-d840-4041-bb14-3c5937f4e138",
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
  "content_id": "f6086ebc-dbce-408b-9738-8b679a6e536b",
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
