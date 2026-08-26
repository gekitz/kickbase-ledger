# Kickbase Decision Ledger — rendered view

Static page for the two-hourly Kickbase briefing (Bundesliga 26/27).

- `index.html` — the UI. **Fixed.** Scheduled runs must never regenerate this file; that is the whole point of the split.
- `data/briefing.json` — the data. Overwritten by each run. Schema version in `schema`.

The page fetches the JSON at load, renders it, and shows a red staleness banner
when `run` is more than 3 hours old, so a pipeline that has stopped announces itself.

## How a run publishes

    KICKBASE_GH_PAT=<pat> python3 scripts/publish.py data/briefing.json

The PAT needs **Contents: read and write** on this repo only. Store it as an
environment variable on the cloud environment the scheduled task uses.

## Enabling Pages

Settings → Pages → Source: *Deploy from a branch* → `main` / `/ (root)`.
