"""Capstone criterion 1: clean-clone setup, automated.

One trial does, in a brand-new temporary folder:
  1. git clone of the GitHub repo (what is actually pushed)
  2. python -m venv, then pip install -r requirements-pinned.txt
  3. python test.py          -> expects 9 of 9 passed
  4. python detector.py      -> expects model_signal between 0.866 and 0.906
  5. python app.py, GET /health -> expects "ok": true and "detector_model": "gpt2"
Then it deletes the temporary folder.

Before you run it: STOP your own running server (Ctrl+C), port 5000 must be
free. Run it from your repo folder with the python you normally use:

    python check_clone.py --trial 1

It can take several minutes because pip installs the pinned packages.
Writes results/clone_trial<N>_<UTC stamp>.txt in your repo folder.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone

import requests

REPO_URL = "https://github.com/Gdnewz/ai201-project4-provenance-guard-starter-v2026.git"
LOW, HIGH = 0.866, 0.906


def venv_python(venv_dir):
    sub = "Scripts" if os.name == "nt" else "bin"
    exe = "python.exe" if os.name == "nt" else "python"
    return os.path.join(venv_dir, sub, exe)


def run(cmd, cwd, timeout):
    p = subprocess.run(
        cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout,
        encoding="utf-8", errors="replace",
    )
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def tail(text, n=12):
    lines = [l for l in text.splitlines() if l.strip()]
    return "\n".join("    " + l[:160] for l in lines[-n:])


def server_up(base):
    try:
        return requests.get(base + "/health", timeout=2).status_code == 200
    except requests.RequestException:
        return False


def stop(proc):
    if os.name == "nt":
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        proc.terminate()
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="http://127.0.0.1:5000")
    ap.add_argument("--trial", default="1")
    ap.add_argument("--repo", default=REPO_URL)
    ap.add_argument("--requirements", default="requirements-pinned.txt")
    args = ap.parse_args()

    if server_up(args.base):
        sys.exit("A server is already answering on " + args.base +
                 ". Stop it with Ctrl+C first, then run this again.")

    origin_cwd = os.getcwd()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    work = tempfile.mkdtemp(prefix=f"pg_clone_t{args.trial}_")
    out = [f"Clone trial {args.trial}, started {stamp} UTC",
           f"repo: {args.repo}", f"temporary folder: {work}", ""]
    repo_dir = os.path.join(work, "repo")
    venv_dir = os.path.join(work, "venv")
    ok_tests = ok_signal = ok_health = False

    try:
        code, text = run(["git", "clone", args.repo, repo_dir], work, 600)
        out.append(f"git clone: exit code {code}")
        if code != 0:
            out.append(tail(text))
            raise RuntimeError("clone failed")

        code, text = run([sys.executable, "-m", "venv", venv_dir], work, 600)
        out.append(f"python -m venv: exit code {code}")
        if code != 0:
            out.append(tail(text))
            raise RuntimeError("venv failed")
        py = venv_python(venv_dir)

        t0 = time.time()
        code, text = run([py, "-m", "pip", "install", "-r", args.requirements,
                          "--disable-pip-version-check"], repo_dir, 3600)
        out.append(f"pip install -r {args.requirements}: exit code {code} "
                   f"({time.time() - t0:.0f} s)")
        if code != 0:
            out.append(tail(text))
            raise RuntimeError("pip install failed")

        # check 1: tests
        code, text = run([py, "test.py"], repo_dir, 1800)
        # test.py prints e.g. "9 passed, 0 failed, 0 to look at, 0 skipped"
        m = re.search(r"\b(\d+)\s+passed,\s*(\d+)\s+failed", text)
        n_pass = int(m.group(1)) if m else None
        n_fail = int(m.group(2)) if m else None
        passed = n_pass == 9 and n_fail == 0
        ok_tests = passed and code == 0
        out.append(f"python test.py: exit code {code}, passed={n_pass}, "
                   f"failed={n_fail}, 9 passed and 0 failed: {passed}")
        out.append(tail(text, 6))

        # check 2: detector signal
        code, text = run([py, "detector.py"], repo_dir, 1800)
        m = re.search(r"model_signal\D{0,12}(\d*\.\d+)", text)
        val = float(m.group(1)) if m else None
        ok_signal = val is not None and LOW <= val <= HIGH
        out.append(f"python detector.py: exit code {code}, "
                   f"model_signal = {val}, window {LOW} to {HIGH}")
        if val is None:
            out.append(tail(text, 8))

        # check 3: server and /health
        proc = subprocess.Popen([py, "app.py"], cwd=repo_dir,
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)
        try:
            deadline = time.time() + 180
            while time.time() < deadline and not server_up(args.base):
                if proc.poll() is not None:
                    break
                time.sleep(0.5)
            if server_up(args.base):
                body = requests.get(args.base + "/health", timeout=10).json()
                ok_health = (body.get("ok") is True
                             and body.get("detector_model") == "gpt2")
                out.append("GET /health: " + json.dumps(body)[:200])
            else:
                out.append("GET /health: server never answered")
        finally:
            stop(proc)
    except Exception as e:  # report, do not hide
        out.append(f"STOPPED EARLY: {e}")
    finally:
        os.chdir(origin_cwd)
        shutil.rmtree(work, ignore_errors=True)

    out.append("")
    out.append(f"check 1, test.py 9 of 9:          {'PASS' if ok_tests else 'FAIL'}")
    out.append(f"check 2, model_signal in window:  {'PASS' if ok_signal else 'FAIL'}")
    out.append(f"check 3, /health ok and gpt2:     {'PASS' if ok_health else 'FAIL'}")
    all_ok = ok_tests and ok_signal and ok_health
    out.append("VERDICT: " + ("MET" if all_ok else "MISSED (read the lines above)"))

    os.makedirs("results", exist_ok=True)
    path = os.path.join("results", f"clone_trial{args.trial}_{stamp}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    out.append("")
    out.append("written to " + path)
    print("\n".join(out))


if __name__ == "__main__":
    main()