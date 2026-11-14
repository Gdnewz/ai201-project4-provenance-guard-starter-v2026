"""Capstone criteria 3 and 5: cold start and the failure case, automated.

For ONE trial this script does 4 restarts of the server, by itself:
  3 restarts where the first request is a normal paragraph   (criterion 3)
  1 restart  where the first request is "a"                  (criterion 5)
Each time it starts "python app.py", waits for /health, sends the one request,
reads the new line from logs/audit.jsonl, then stops the server again.

Before you run it: STOP your own running server (Ctrl+C), the script needs
port 5000 free. Run it from the repo folder with the same Python you use for
the project (the activated virtual environment):

    python check_cold.py --trial 1

Writes results/cold_trial<N>_<UTC stamp>.txt
"""
import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone

import requests

LOG_PATH = os.path.join("logs", "audit.jsonl")
PARAGRAPH = (
    "I went to the store yesterday. It was crowded, so I waited in line for a "
    "long time. When I got home, I made dinner and watched a show."
)
C3_LIMIT_MS = 8500.0   # criterion 3: every one of the 3 at most 8.5 seconds
C5_LIMIT_MS = 3000.0   # criterion 5: at most 3 seconds


def server_up(base):
    try:
        return requests.get(base + "/health", timeout=2).status_code == 200
    except requests.RequestException:
        return False


def start_server(base):
    proc = subprocess.Popen(
        [sys.executable, "app.py"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    deadline = time.time() + 120
    while time.time() < deadline:
        if server_up(base):
            return proc
        if proc.poll() is not None:
            raise RuntimeError("app.py exited before it answered /health")
        time.sleep(0.5)
    stop_server(proc)
    raise RuntimeError("server did not answer /health within 120 seconds")


def stop_server(proc):
    # taskkill /T also stops the child process that Flask debug mode starts
    if os.name == "nt":
        subprocess.run(
            ["taskkill", "/F", "/T", "/PID", str(proc.pid)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    else:
        proc.terminate()
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()


def wait_until_down(base):
    deadline = time.time() + 30
    while time.time() < deadline:
        if not server_up(base):
            return True
        time.sleep(0.5)
    return False


def log_line_count():
    if not os.path.exists(LOG_PATH):
        return 0
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        return len(f.read().splitlines())


def one_restart(base, text, label):
    """Restart, send one request, return (status, entry dict or None)."""
    proc = start_server(base)
    try:
        before = log_line_count()
        creator = f"cold-{label}-{int(time.time() * 1000)}"
        r = requests.post(
            base + "/submit",
            json={"creator_id": creator, "text": text},
            timeout=180,
        )
        time.sleep(1.0)
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            new = f.read().splitlines()[before:]
        entry = None
        for raw in new:
            try:
                e = json.loads(raw)
            except ValueError:
                continue
            if e.get("event") in (None, "rejected") and "duration_ms" in e:
                entry = e
        return r.status_code, entry
    finally:
        stop_server(proc)
        wait_until_down(base)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="http://127.0.0.1:5000")
    parser.add_argument("--trial", default="1")
    args = parser.parse_args()

    if server_up(args.base):
        sys.exit("A server is already answering on " + args.base +
                 ". Stop it with Ctrl+C first, then run this again.")

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    out = [f"Cold trial {args.trial}, started {stamp} UTC", ""]

    out.append("Criterion 3: first request after each of 3 restarts (normal paragraph)")
    c3 = []
    for i in range(1, 4):
        status, e = one_restart(args.base, PARAGRAPH, f"c3-{i}")
        if e is None:
            out.append(f"  restart {i}: status {status}, NO TIMED LOG ENTRY FOUND")
            c3.append(None)
            continue
        ms = e.get("duration_ms")
        out.append(
            f"  restart {i}: status {status}, duration_ms={ms}, "
            f"model_warm={e.get('model_warm')}"
        )
        c3.append(ms)
    c3_ok = all(m is not None and m <= C3_LIMIT_MS for m in c3)
    out.append(f"  limit {C3_LIMIT_MS:.0f} ms for every one of the 3")
    out.append("  CRITERION 3 VERDICT: " + ("MET" if c3_ok else "MISSED"))
    out.append("")

    out.append('Criterion 5: first request after a restart is "a"')
    status, e = one_restart(args.base, "a", "c5")
    if e is None:
        out.append(f"  status {status}, NO TIMED LOG ENTRY FOUND")
        c5_ok = False
    else:
        ms = e.get("duration_ms")
        out.append(
            f"  status {status}, duration_ms={ms}, model_warm={e.get('model_warm')}, "
            f"reason={e.get('reason')}"
        )
        c5_ok = ms is not None and ms <= C5_LIMIT_MS
    out.append(f"  limit {C5_LIMIT_MS:.0f} ms")
    out.append("  CRITERION 5 VERDICT: " + ("MET" if c5_ok else "MISSED"))

    os.makedirs("results", exist_ok=True)
    path = os.path.join("results", f"cold_trial{args.trial}_{stamp}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    out.append("")
    out.append("written to " + path)
    print("\n".join(out))


if __name__ == "__main__":
    main()