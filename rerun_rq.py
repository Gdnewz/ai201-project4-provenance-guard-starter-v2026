import time
import urllib.request
import urllib.error

URL = "http://127.0.0.1:5000/submit"
rows = [
    ("RQ08", b'{"text": "unterminated', "application/json"),
    ("RQ09", b"", "application/json"),
    ("RQ10", b"text=hello&creator_id=attacker_RQ10", "application/x-www-form-urlencoded"),
    ("RQ11", b'{"text": "Real writing.", "creator_id": "attacker_RQ11"}', "text/plain"),
]

for i, (rid, body, ctype) in enumerate(rows):
    if i:
        time.sleep(25)  # stay under 3 per minute: these count against my address
    req = urllib.request.Request(URL, data=body, method="POST", headers={"Content-Type": ctype})
    try:
        with urllib.request.urlopen(req) as r:
            print(rid, r.status, r.read().decode())
    except urllib.error.HTTPError as e:
        print(rid, e.code, e.read().decode())