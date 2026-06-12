#!/usr/bin/env python3
"""
build.py - regenerate index.html from profile.json + publications.json.

Zero dependencies (Python stdlib only). cc owns this loop:
  edit profile.json / publications.json  ->  python3 build.py  ->  git commit/push

Deploy: pushing index.html (+ assets) to the zzzx1224.github.io repo is the
deploy; GitHub Pages serves the static files directly. No build server needed.
"""

import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as f:
        return json.load(f)


def bold_me(authors, me="Zehao Xiao"):
    # authors strings may contain raw <a>; only bold the candidate's name
    return authors.replace(me, f"<strong>{me}</strong>")


def render_links(links):
    if not links:
        return ""
    btns = "".join(
        f'<a class="btn" href="{html.escape(u)}" target="_blank" rel="noopener">{html.escape(l)}</a>'
        for l, u in links.items()
    )
    return f'<div class="pub-links">{btns}</div>'


def render_pub(p):
    img = p.get("image")
    thumb = (
        f'<div class="pub-thumb"><img loading="lazy" src="{html.escape(img)}" alt=""></div>'
        if img else '<div class="pub-thumb pub-thumb--empty"></div>'
    )
    title = html.escape(p["title"])
    paper_url = p.get("links", {}).get("Paper")
    title_html = (
        f'<a href="{html.escape(paper_url)}" target="_blank" rel="noopener">{title}</a>'
        if paper_url else title
    )
    venue = html.escape(p.get("venue", ""))
    year = html.escape(str(p.get("year", "")))
    venue_html = f'<span class="pub-venue"><em>{venue}</em>{", " + year if year else ""}</span>' if venue else ""
    authors = bold_me(p.get("authors", ""))
    tldr = f'<p class="pub-tldr">{html.escape(p["tldr"])}</p>' if p.get("tldr") else ""
    links = render_links(p.get("links", {}))
    return f"""    <article class="pub">
      {thumb}
      <div class="pub-body">
        <h3 class="pub-title">{title_html}</h3>
        <p class="pub-authors">{authors}</p>
        {venue_html}
        {tldr}
        {links}
      </div>
    </article>"""


def render_social(links):
    return "".join(
        f'<a class="social" href="{html.escape(u)}" target="_blank" rel="noopener">{html.escape(l)}</a>'
        for l, u in links.items()
    )


def render_news(news):
    items = "".join(
        f'<li><span class="news-date">{html.escape(n["date"])}</span> {n["html"]}</li>'
        for n in news
    )
    return f'<ul class="news">{items}</ul>'


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{name}</title>
<meta name="description" content="{tagline}">
<style>
:root {{ --accent:{accent}; --ink:#1f2937; --muted:#6b7280; --line:#e5e7eb; --bg:#ffffff; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  color:var(--ink); background:var(--bg); line-height:1.6; }}
a {{ color:var(--accent); text-decoration:none; }}
a:hover {{ text-decoration:underline; }}
header.nav {{ position:sticky; top:0; background:rgba(255,255,255,.92); backdrop-filter:blur(6px);
  border-bottom:1px solid var(--line); z-index:10; }}
.nav-inner {{ max-width:880px; margin:0 auto; padding:.7rem 1.2rem; display:flex; gap:1.4rem; align-items:center; }}
.nav-inner .brand {{ font-weight:700; margin-right:auto; }}
.nav-inner a {{ color:var(--ink); font-size:.95rem; }}
main {{ max-width:880px; margin:0 auto; padding:0 1.2rem; }}
section {{ padding:2.4rem 0; border-bottom:1px solid var(--line); }}
section h2 {{ font-size:1.35rem; margin:0 0 1.1rem; color:var(--ink);
  border-left:4px solid var(--accent); padding-left:.6rem; }}
.hero {{ display:flex; gap:1.6rem; align-items:center; flex-wrap:wrap; padding-top:2.6rem; }}
.hero img {{ width:150px; height:150px; border-radius:50%; object-fit:cover; border:3px solid var(--line); }}
.hero h1 {{ margin:0 0 .2rem; font-size:1.8rem; }}
.hero .roles {{ color:var(--muted); margin:.1rem 0; }}
.hero .roles strong {{ color:var(--ink); font-weight:600; }}
.socials {{ margin-top:.7rem; display:flex; gap:.5rem; flex-wrap:wrap; }}
.social {{ font-size:.82rem; padding:.25rem .6rem; border:1px solid var(--line); border-radius:999px; color:var(--ink); }}
.social:hover {{ border-color:var(--accent); color:var(--accent); text-decoration:none; }}
.news {{ list-style:none; padding:0; margin:0; }}
.news li {{ padding:.28rem 0; color:var(--ink); }}
.news-date {{ display:inline-block; min-width:7.5rem; color:var(--muted); font-size:.88rem; }}
.pub {{ display:flex; gap:1.1rem; padding:1.1rem 0; border-top:1px solid var(--line); }}
.pub:first-of-type {{ border-top:none; }}
.pub-thumb {{ flex:0 0 150px; }}
.pub-thumb img {{ width:150px; height:96px; object-fit:cover; border-radius:6px; border:1px solid var(--line); }}
.pub-thumb--empty {{ width:150px; height:96px; border:1px dashed var(--line); border-radius:6px; }}
.pub-title {{ margin:0 0 .25rem; font-size:1.04rem; }}
.pub-authors {{ margin:.1rem 0; font-size:.92rem; color:var(--ink); }}
.pub-venue {{ font-size:.9rem; color:var(--muted); }}
.pub-tldr {{ margin:.45rem 0 .2rem; font-size:.9rem; color:var(--muted); }}
.pub-links {{ margin-top:.5rem; display:flex; gap:.45rem; flex-wrap:wrap; }}
.btn {{ font-size:.8rem; padding:.18rem .55rem; border:1px solid var(--accent); border-radius:5px; color:var(--accent); }}
.btn:hover {{ background:var(--accent); color:#fff; text-decoration:none; }}
.contact {{ list-style:none; padding:0; margin:0; color:var(--muted); }}
footer {{ text-align:center; color:var(--muted); font-size:.82rem; padding:1.6rem 0; }}
@media (max-width:560px) {{ .pub {{ flex-direction:column; }} .pub-thumb img,.pub-thumb--empty {{ width:100%; height:140px; }} }}
</style>
</head>
<body>
<header class="nav"><div class="nav-inner">
  <span class="brand">{name}</span>
  <a href="#about">Home</a><a href="#publications">Publications</a><a href="#contact">Contact</a>
</div></header>
<main>
  <section class="hero" id="about">
    <img src="{photo}" alt="{name}">
    <div>
      <h1>{name}</h1>
      {roles}
      <div class="socials">{socials}</div>
    </div>
  </section>
  <section id="bio">
    <h2>About</h2>
    {bio}
    <h3 style="margin-top:1.4rem;font-size:1.05rem;">News</h3>
    {news}
  </section>
  <section id="publications">
    <h2>Publications</h2>
{pubs}
  </section>
  <section id="contact">
    <h2>Contact</h2>
    <ul class="contact">{contact}</ul>
  </section>
</main>
<footer>Built from profile.json + publications.json &middot; updated by Claude Code</footer>
</body>
</html>
"""


def main():
    prof = load("profile.json")
    pubs = load("publications.json")
    roles = "".join(f'<div class="roles">{r}</div>' for r in prof.get("roles", []))
    bio = "".join(f"<p>{para}</p>" for para in prof.get("bio", []))
    contact = "".join(f"<li>{c}</li>" for c in prof.get("contact", []))
    out = TEMPLATE.format(
        name=html.escape(prof["name"]),
        tagline=html.escape(prof.get("tagline", "")),
        accent=prof.get("accent", "#1565c0"),
        photo=html.escape(prof["photo"]),
        roles=roles,
        socials=render_social(prof.get("social", {})),
        bio=bio,
        news=render_news(prof.get("news", [])),
        pubs="\n".join(render_pub(p) for p in pubs),
        contact=contact,
    )
    with open(os.path.join(HERE, "index.html"), "w", encoding="utf-8") as f:
        f.write(out)
    print(f"Wrote index.html ({len(out)} bytes, {len(pubs)} publications)")


if __name__ == "__main__":
    main()
