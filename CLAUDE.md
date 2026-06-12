# CLAUDE.md — Homepage repo

This repo is Zehao Xiao's academic homepage, served at https://zzzx1224.github.io/
as **static files via GitHub Pages**. It is now a lightweight, build-it-yourself
site — NO Hugo, NO Wowchemy, no toolchain. You (Claude Code) own the loop.

## How it works
- Content lives in two data files: `profile.json` (identity, bio, news, links,
  contact) and `publications.json` (the publication list).
- `python3 build.py` regenerates `index.html` from those two files. Stdlib only.
- Existing assets (`authors/`, `publication_zehao/`, `media/`, `css/` leftovers)
  remain in the repo; images are referenced by absolute URL to this same site,
  so they keep working. (Switch to relative paths if you ever move the domain.)

## The loop you run
1. Edit `profile.json` and/or `publications.json`.
2. `python3 build.py`  -> regenerates `index.html`.
3. Show the diff. **Get explicit approval before pushing** (this is a public site).
4. `git add -A && git commit && git push`  -> GitHub Pages serves the update.

## Source-of-truth (anti-drift)
- `publications.json` is the CANONICAL publication list. It also drives the CV:
  run `python3 gen_cv_pubs.py` to emit the LaTeX `cventries` block for
  `master-resume.tex`. **Edit `publications.json` once; never maintain the
  homepage list and the CV list separately.**
- The job-search vault keeps a human-readable mirror at
  `profile/publications.md`; this JSON is the machine source. Keep them aligned.

## Hard guardrails
- **No fabrication.** Never invent or upgrade publications, venues, dates,
  authors, or claims. Everything here must be true and verifiable.
- **Public-site safety.** Never push without showing a diff and getting an
  explicit yes. Work on a branch if making larger changes.
- **Stale content to fix (flagged in the data files):** current role/affiliation
  (PhD is completed; add current position), contact address (the UvA one is old).
  Do NOT publish a guessed affiliation — confirm with Zehao first.

## Conventions
- Keep `news` newest-first. Use real venue names and years.
- Author strings: write Zehao's name in full as "Zehao Xiao" (build.py bolds it).
  Keep "*" equal-contribution marks where they apply.
- A publication with no `image` renders cleanly without a thumbnail.
