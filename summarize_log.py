"""
Summarize the Provenance Guard audit log.

    python summarize_log.py                          reads logs/audit.jsonl
    python summarize_log.py path/to/log              reads another file
    python summarize_log.py --since 2026-11-13T15:00 only entries at or after that
                                                     time (the log uses UTC)

Prints request counts, rejections by reason, and p50 / p95 of duration_ms,
split into warm requests (model already loaded) and cold ones (the first
request after the service starts, which pays for loading gpt2).

It only reads the log. It never changes or deletes anything in it.
"""

import json
import statistics
import sys
from collections import Counter

DEFAULT_LOG = "logs/audit.jsonl"


def read_log(path):
    """Return (entries, unreadable_count). Bad lines are counted, not deleted."""
    entries = []
    unreadable = 0
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                unreadable += 1
                continue
            if isinstance(entry, dict):
                entries.append(entry)
            else:
                unreadable += 1
    return entries, unreadable


def has_duration(entry):
    value = entry.get("duration_ms")
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def describe(label, values):
    """Print one latency line: count, p50, p95 and the slowest request."""
    if not values:
        print(f"    {label}: none")
        return
    if len(values) < 2:
        print(f"    {label}: n=1, {values[0]:.2f} ms (too few for percentiles)")
        return
    cuts = statistics.quantiles(values, n=100, method="inclusive")
    p50, p95 = cuts[49], cuts[94]
    print(f"    {label}: n={len(values)}  p50={p50:.2f} ms  "
          f"p95={p95:.2f} ms  max={max(values):.2f} ms")


def parse_args(argv):
    """Return (path, since). `since` is an ISO time string like 2026-11-13T15:00 or None."""
    path = DEFAULT_LOG
    since = None
    i = 0
    while i < len(argv):
        if argv[i] == "--since" and i + 1 < len(argv):
            since = argv[i + 1]
            i += 2
        else:
            path = argv[i]
            i += 1
    return path, since


def main():
    path, since = parse_args(sys.argv[1:])

    try:
        entries, unreadable = read_log(path)
    except FileNotFoundError:
        print(f"No log file at {path}")
        return 1

    total_read = len(entries)
    if since:
        # Timestamps are ISO strings in UTC, so comparing them as text is correct.
        entries = [e for e in entries if str(e.get("timestamp", "")) >= since]

    print(f"Provenance Guard log summary: {path}")
    print(f"  entries read: {total_read}   unreadable lines skipped: {unreadable}")
    if since:
        print(f"  only entries at or after {since} (UTC): {len(entries)} kept")
    if not entries:
        print("  the log is empty, nothing to summarize")
        return 0

    appeals = [e for e in entries if e.get("event") == "appeal"]
    rejections = [e for e in entries if e.get("event") == "rejected"]
    decisions = [e for e in entries if e.get("event") not in ("appeal", "rejected")]
    submissions = decisions + rejections

    print(f"  submissions: {len(submissions)}  "
          f"(decided {len(decisions)}, rejected {len(rejections)})")
    print(f"  appeals: {len(appeals)} (not timed, counted separately)")

    if rejections:
        print("  rejections by reason:")
        by_reason = Counter(e.get("reason", "unknown") for e in rejections)
        for reason, count in by_reason.most_common():
            print(f"    {reason}: {count}")

    timed = [e for e in submissions if has_duration(e)]
    untimed = len(submissions) - len(timed)
    print(f"  timed submissions: {len(timed)}   without duration_ms: {untimed} "
          "(logged before timing existed, or rate limited before the route ran)")

    if not timed:
        print("  no timed submissions yet")
        return 0

    warm = [e["duration_ms"] for e in timed if e.get("model_warm") is True]
    cold = [e["duration_ms"] for e in timed if e.get("model_warm") is False]
    unknown = [e["duration_ms"] for e in timed if "model_warm" not in e]

    print("  latency (duration_ms, from the start of /submit to just before the log write):")
    describe("all timed", [e["duration_ms"] for e in timed])
    describe("warm (model already loaded)", warm)
    describe("cold (first request, model loading)", cold)
    if unknown:
        describe("model_warm not recorded", unknown)
    return 0


if __name__ == "__main__":
    sys.exit(main())