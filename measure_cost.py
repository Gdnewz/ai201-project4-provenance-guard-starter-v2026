"""
Measure what one run of Provenance Guard costs, in seconds of compute.

    python measure_cost.py                  10 requests
    python measure_cost.py --runs 11        11 requests (use this right after a
                                            fresh start: 1 cold + 10 warm)
    python measure_cost.py --url http://127.0.0.1:5000

One "run" is one POST to /submit with the same 134 character paragraph, each
under its own creator_id so the rate limit never blocks the measurement.

Two numbers per run:
  server_ms  duration_ms from the audit log: start of /submit to just before
             the log write. This is the compute the service spent.
  client_ms  wall time as the caller sees it, including building and sending
             the response.

The log says which requests were cold (the model was not loaded yet), so the
cold start is reported separately and left out of the warm average.
A summary is also written to results/cost_run_<UTC time>.md.
"""

import argparse
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

TEXT = (
    "I went to the store yesterday. It was crowded, so I waited in line for a "
    "long time. When I got home, I made dinner and watched a show."
)


def run_once(url, creator_id):
    start = time.perf_counter()
    response = requests.post(
        f"{url}/submit",
        json={"text": TEXT, "creator_id": creator_id},
        timeout=120,
    )
    client_ms = round((time.perf_counter() - start) * 1000, 2)
    content_id = None
    if response.headers.get("content-type", "").startswith("application/json"):
        content_id = response.json().get("content_id")
    return response.status_code, client_ms, content_id


def fetch_log(url, limit):
    response = requests.get(f"{url}/log", params={"limit": limit}, timeout=30)
    response.raise_for_status()
    return response.json()["entries"]


def describe(values):
    return (f"mean {statistics.mean(values):.2f}  median {statistics.median(values):.2f}  "
            f"min {min(values):.2f}  max {max(values):.2f}")


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--runs", type=int, default=10)
    parser.add_argument("--url", default="http://127.0.0.1:5000")
    args = parser.parse_args()

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    rows = []
    for i in range(1, args.runs + 1):
        status, client_ms, content_id = run_once(args.url, f"cost_{stamp}_{i}")
        rows.append({"run": i, "status": status, "client_ms": client_ms,
                     "content_id": content_id})
        print(f"run {i}: status {status}, client {client_ms} ms")

    entries = {e.get("content_id"): e for e in fetch_log(args.url, args.runs + 25)
               if e.get("content_id")}
    for row in rows:
        entry = entries.get(row["content_id"], {})
        row["server_ms"] = entry.get("duration_ms")
        row["model_warm"] = entry.get("model_warm")

    ok = [r for r in rows if r["status"] == 200 and r["server_ms"] is not None]
    warm = [r for r in ok if r["model_warm"] is True]
    cold = [r for r in ok if r["model_warm"] is False]
    failed = len(rows) - len(ok)

    lines = [
        f"# Cost run {stamp} (UTC)",
        "",
        f"{args.runs} requests to {args.url}/submit, one 134 character paragraph, "
        "each under its own creator_id.",
        "",
        "| Run | Status | model_warm | server_ms | client_ms |",
        "|---|---|---|---|---|",
    ]
    for r in rows:
        lines.append(f"| {r['run']} | {r['status']} | {r['model_warm']} | "
                     f"{r['server_ms']} | {r['client_ms']} |")
    lines.append("")
    if warm:
        lines.append(f"Warm runs (n={len(warm)}), server_ms: "
                     f"{describe([r['server_ms'] for r in warm])}")
        lines.append(f"Warm runs (n={len(warm)}), client_ms: "
                     f"{describe([r['client_ms'] for r in warm])}")
    else:
        lines.append("No warm runs recorded.")
    for r in cold:
        lines.append(f"Cold run {r['run']}: server_ms {r['server_ms']}, "
                     f"client_ms {r['client_ms']}")
    if failed:
        lines.append(f"{failed} run(s) failed or had no log entry; see the table.")

    report = "\n".join(lines)
    print()
    print(report)

    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    path = results_dir / f"cost_run_{stamp}.md"
    path.write_text(report + "\n", encoding="utf-8")
    print(f"\nwritten to {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())