#!/usr/bin/env python3
"""Push data/briefing.json to the GH Pages repo via the Contents API.

Env:
  KICKBASE_GH_PAT   fine-grained PAT, Contents: read+write on the target repo
  KICKBASE_GH_REPO  "owner/repo"        (default: gekitz/kickbase-ledger)
  KICKBASE_GH_BRANCH                    (default: main)
Usage: python3 scripts/publish.py [path-to-briefing.json]
"""
import base64, json, os, sys, urllib.request, urllib.error

REPO   = os.environ.get("KICKBASE_GH_REPO", "gekitz/kickbase-ledger")
BRANCH = os.environ.get("KICKBASE_GH_BRANCH", "main")
TOKEN  = os.environ.get("KICKBASE_GH_PAT")
SRC    = sys.argv[1] if len(sys.argv) > 1 else "data/briefing.json"
DEST   = "data/briefing.json"
API    = f"https://api.github.com/repos/{REPO}/contents/{DEST}"

def req(url, method="GET", body=None):
    r = urllib.request.Request(url, method=method,
        data=json.dumps(body).encode() if body else None,
        headers={"Authorization": f"Bearer {TOKEN}",
                 "Accept": "application/vnd.github+json",
                 "X-GitHub-Api-Version": "2022-11-28",
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(r, timeout=30) as resp:
        return json.loads(resp.read() or b"{}")

if not TOKEN:
    sys.exit("KICKBASE_GH_PAT is not set — add it to the cloud environment's variables.")

payload = open(SRC, "rb").read()
run = json.loads(payload).get("run", "unknown")

sha = None
try:
    sha = req(f"{API}?ref={BRANCH}").get("sha")
except urllib.error.HTTPError as e:
    if e.code != 404:
        sys.exit(f"read failed: HTTP {e.code} {e.read()[:300].decode(errors='replace')}")

body = {"message": f"briefing {run}", "content": base64.b64encode(payload).decode(),
        "branch": BRANCH}
if sha:
    body["sha"] = sha

try:
    out = req(API, "PUT", body)
except urllib.error.HTTPError as e:
    sys.exit(f"write failed: HTTP {e.code} {e.read()[:300].decode(errors='replace')}")

print(f"published {run} -> {REPO}@{BRANCH} commit {out['commit']['sha'][:7]}")
