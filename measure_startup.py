"""How long does the service take to start answering /health?

Starts "python app.py" three times, times each start until GET /health answers,
stops it again, and writes results/startup_<label>_<UTC stamp>.txt.

Use it once BEFORE changing app.py and detector.py (label "before") and once
AFTER (label "after"), so the cost of preparing the tokenizer at start is
reported. Stop your own server first (Ctrl+C): port 5000 must be free.

    python measure_startup.py --label before
"""
import argparse
import os
import statistics
import subprocess
import sys
import time
from datetime import datetime, timezone

import requests

from check_cold import server_up, stop_server, wait_until_down


def one_start(base):
    t0 = time.perf_counter()
    proc = subprocess.Popen(
        [sys.executable, "app.py"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        deadline = time.time() + 180
        while time.time() < deadline:
            if server_up(base):
                return time.perf_counter() - t0
            if proc.poll() is not None:
                raise RuntimeError("app.py exited before it answered /health")
            time.sleep(0.1)
        raise RuntimeError("no answer from /health within 180 seconds")
    finally:
        stop_server(proc)
        wait_until_down(base)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="http://127.0.0.1:5000")
    ap.add_argument("--label", default="before")
    args = ap.parse_args()

    if server_up(args.base):
        sys.exit("A server is already answering on " + args.base +
                 ". Stop it with Ctrl+C first, then run this again.")

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    out = [f"Startup time ({args.label}), started {stamp} UTC",
           "seconds from launching python app.py until GET /health answers", ""]
    times = []
    for i in range(1, 4):
        sec = one_start(args.base)
        times.append(sec)
        out.append(f"  start {i}: {sec:.2f} s")
    out.append(f"  median {statistics.median(times):.2f} s, "
               f"min {min(times):.2f} s, max {max(times):.2f} s")

    os.makedirs("results", exist_ok=True)
    path = os.path.join("results", f"startup_{args.label}_{stamp}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    out.append("")
    out.append("written to " + path)
    print("\n".join(out))


if __name__ == "__main__":
    main()