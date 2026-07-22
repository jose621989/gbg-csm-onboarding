import base64, json, urllib.request, os, sys

import os as _os
TOKEN = _os.environ.get("GITHUB_TOKEN", "").strip()
if not TOKEN:
    print("NO TOKEN IN ENV"); sys.exit(1)
API = "https://api.github.com/repos/jose621989/gbg-csm-onboarding/contents"
BRANCH = "main"

root = os.path.dirname(__file__)
targets = [
    ("assets/index-Buzv4xRN.js", "assets/index-Buzv4xRN.js"),
    ("index.html", "index.html"),
    ("assets/index-DDcnQbDe.css", "assets/index-DDcnQbDe.css"),
]

for local, ghpath in targets:
    local_path = os.path.join(root, local)
    if not os.path.exists(local_path):
        print(f"SKIP (missing) {ghpath}")
        continue
    b64 = base64.b64encode(open(local_path, "rb").read()).decode()
    payload = json.dumps({"message": "Add " + ghpath, "content": b64, "branch": BRANCH}).encode()
    url = API + "/" + ghpath
    req = urllib.request.Request(url, data=payload, method="PUT", headers={
        "Authorization": "Bearer " + TOKEN,
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
        "User-Agent": "hermes-deploy",
    })
    try:
        r = urllib.request.urlopen(req, timeout=60)
        print(f"OK   {ghpath} -> {r.status}")
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:300]
        print(f"FAIL {ghpath} -> {e.code} {body}")
