# Homepage (lightweight rebuild)

Drop these files into your `zzzx1224.github.io` repo. No Hugo, no install.

## Files
- `profile.json` — identity, bio, news, social links, contact
- `publications.json` — CANONICAL publication list (also drives the CV)
- `build.py` — `python3 build.py` regenerates `index.html`
- `gen_cv_pubs.py` — `python3 gen_cv_pubs.py` prints the LaTeX pubs block for your CV
- `CLAUDE.md` — instructions + guardrails for Claude Code
- `index.html` — generated output (sample included; rebuilt by build.py)

## Setup (one time, in local cc)
1. Copy these files into the homepage repo root (keep your existing `authors/`,
   `publication_zehao/`, `media/` asset folders — images reference them).
2. `python3 build.py` and open `index.html` to check it.
3. When happy: `git add -A && git commit -m "rebuild homepage" && git push`.
   GitHub Pages serves the new static files. Done.

## Editing later
Edit the JSON -> `python3 build.py` -> review diff -> commit/push. That's it.

## Before going live — confirm these (flagged with <CONFIRM> in the JSON)
- Current role / affiliation (PhD is done; add your current position)
- Contact address (the old UvA one is stale)
- The merged 2026 news line (split into dated items if you like)
