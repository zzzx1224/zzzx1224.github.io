# CLAUDE.md — Homepage repo

This repo is Zehao Xiao's academic homepage, served at https://zzzx1224.github.io/
as **static files via GitHub Pages**. It is now a lightweight, build-it-yourself
site — NO Hugo, NO Wowchemy, no toolchain. You (Claude Code) own the loop.

## How it works
- Content lives in two data files: `profile.json` (identity, bio, news, links,
  contact) and `publications.json` (the publication list).
- `python3 build.py` regenerates `index.html` from those two files. Stdlib only.
- Existing assets (`authors/`, `publication_zehao/`, `media/`, `css/` leftovers)
  remain in the repo; images are referenced by **relative** paths (e.g.
  `publication_zehao/foo.png`), so they work both locally and on the live site.

## The loop you run
1. Edit `profile.json` and/or `publications.json`.
2. `python3 build.py`  -> regenerates `index.html`.
3. `git add -A && git commit && git push`  -> GitHub Pages serves the update.
4. Show the diff + live link **after** pushing. (Auto-push approved by Zehao,
   2026-06 — no pre-approval needed; the No-fabrication rule below still applies.)

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
- **Public-site safety.** Auto-push is approved (Zehao, 2026-06): push without
  waiting for pre-approval, but ALWAYS show the diff + live link afterward, and
  NEVER auto-push fabricated/unverified content (see No fabrication).
- **Affiliation:** current role is Postdoctoral Researcher, Huawei Noah's Ark
  Lab, Paris (set 2026-06); contact is email-only (stale UvA address removed).
  Do NOT publish a guessed affiliation — confirm with Zehao first.

## Conventions
- Keep `news` newest-first. Use real venue names and years.
- Author strings: write Zehao's name in full as "Zehao Xiao" (build.py bolds it).
  Keep "*" equal-contribution marks where they apply.
- A publication with no `image` renders cleanly without a thumbnail.
