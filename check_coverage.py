"""Capstone criterion 4: instrumentation coverage check.

Sends 10 requests to a running Provenance Guard server (8 normal, 2 rejected),
each under its own creator_id so the rate limiter cannot interfere, then reads
the lines the server appended to logs/audit.jsonl and checks that every timed
entry (decided or rejected, not rate limited, not appeals) carries both
duration_ms and model_warm.

Usage (server already running, from the repo folder):
    python check_coverage.py --trial 1

Writes results/criterion4_trial<N>_<UTC stamp>.txt with the raw log lines.
"""
import argparse
import json
import os
import time
from datetime import datetime, timezone

import requests

LOG_PATH = os.path.join("logs", "audit.jsonl")

NORMAL_TEXTS = [
    "I walked to the market this morning and bought some bread and apples. The baker was friendly, and we talked about the weather for a while.",
    "Last weekend my family drove to the lake. The water was cold, so we mostly sat on the dock and ate sandwiches while the kids skipped stones.",
    "My neighbor has a small garden with tomatoes and peppers. Every summer she leaves a bag on our porch, and we always say thank you with a pie.",
    "The bus was late again today, so I read a few chapters of my book. By the time it arrived, I was almost glad it had been delayed.",
    "We painted the kitchen yellow over two days. It took longer than planned because the old paint kept showing through the first coat.",
    "After work I usually go for a short run around the block. Some days it feels easy, and other days I only make it halfway before turning back.",
    "My sister called to say she got the new job. We were all very happy, and we planned a dinner for Friday to celebrate together.",
    "The library near my house has a quiet room upstairs. I go there on Saturdays to write letters and drink tea from a thermos.",
]

REJECTED_INPUTS = [
    ("empty text", ""),
    ("one character", "a"),
]


def classify(entry):
    """Return decided, rejected, rate_limited, appeal or other."""
    if entry.get("event") == "appeal":
        return "appeal"
    reason = str(entry.get("reason", "")).lower()
    if entry.get("event") == "rejected":
        if "rate" in reason or "limit" in reason:
            return "rate_limited"
        return "rejected"
    if "event" not in entry and entry.get("status") == "decided":
        return "decided"
    return "other"


def read_new_lines(start_count):
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    return lines[start_count:]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="http://127.0.0.1:5000")
    parser.add_argument("--trial", default="1")
    args = parser.parse_args()

    with open(LOG_PATH, "r", encoding="utf-8") as f:
        start_count = len(f.read().splitlines())

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    inputs = [("normal", t) for t in NORMAL_TEXTS] + REJECTED_INPUTS

    out = []
    out.append(f"Criterion 4 trial {args.trial}, started {stamp} UTC")
    out.append(f"requests sent: {len(inputs)}")
    out.append("")

    for i, (kind, text) in enumerate(inputs, start=1):
        creator = f"c4-t{args.trial}-{stamp}-{i:02d}"
        r = requests.post(
            args.base + "/submit",
            json={"creator_id": creator, "text": text},
            timeout=120,
        )
        out.append(f"request {i:02d} ({kind}): status {r.status_code}")

    time.sleep(1.0)
    new_lines = read_new_lines(start_count)

    counts = {}
    timed = 0
    covered = 0
    missing = []
    out.append("")
    out.append("log lines added by this trial:")
    for raw in new_lines:
        try:
            e = json.loads(raw)
        except ValueError:
            out.append("  UNREADABLE: " + raw[:120])
            continue
        kind = classify(e)
        counts[kind] = counts.get(kind, 0) + 1
        has_both = "duration_ms" in e and "model_warm" in e
        if kind in ("decided", "rejected"):
            timed += 1
            if has_both:
                covered += 1
            else:
                missing.append(raw)
        out.append(
            f"  {kind:<12} duration_ms={e.get('duration_ms')} "
            f"model_warm={e.get('model_warm')} reason={e.get('reason')}"
        )

    out.append("")
    out.append(f"entries by kind: {counts}")
    out.append(f"timed entries (decided + rejected, excluding rate limited): {timed}")
    out.append(f"timed entries with both duration_ms and model_warm: {covered}")
    out.append(f"rejected entries seen: {counts.get('rejected', 0)}")
    out.append(f"rate limited entries (excluded): {counts.get('rate_limited', 0)}")
    if missing:
        out.append("entries missing a field:")
        out.extend("  " + m[:200] for m in missing)

    pct = (100.0 * covered / timed) if timed else 0.0
    out.append(f"coverage: {pct:.0f} percent")

    ok = (
        timed == len(inputs)
        and covered == timed
        and counts.get("rejected", 0) >= 1
    )
    out.append("VERDICT: " + ("MET" if ok else "MISSED (read the lines above)"))

    os.makedirs("results", exist_ok=True)
    path = os.path.join("results", f"criterion4_trial{args.trial}_{stamp}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    out.append("")
    out.append("written to " + path)

    print("\n".join(out))


if __name__ == "__main__":
    main()