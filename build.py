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
    title = html.escape(p["title"])
    paper_url = p.get("links", {}).get("Paper")
    title_html = (
        f'<a href="{html.escape(paper_url, quote=True)}" target="_blank" rel="noopener">{title}</a>'
        if paper_url else title
    )
    image = p.get("image")
    if image:
        image_html = (
            f'<img loading="lazy" src="{html.escape(image, quote=True)}" '
            f'alt="Figure for {title}">'
        )
        if paper_url:
            image_html = (
                f'<a class="pub-image-link" href="{html.escape(paper_url, quote=True)}" '
                f'target="_blank" rel="noopener">{image_html}</a>'
            )
    else:
        image_html = ""
    venue = html.escape(p.get("venue", ""))
    authors = bold_me(html.escape(p.get("authors", "")))
    links = render_links(p.get("links", {}))
    return f"""      <article class="pub">
        <div class="pub-side">
          <div class="pub-venue">{venue}</div>
          {image_html}
        </div>
        <div class="pub-body">
          <h4 class="pub-title">{title_html}</h4>
          <p class="pub-authors">{authors}</p>
          {links}
        </div>
      </article>"""


def render_publications(pubs, scholar_url):
    groups = {}
    for pub in pubs:
        groups.setdefault(pub["year"], []).append(pub)
    scholar = html.escape(scholar_url, quote=True)
    intro = (
        '<p class="pub-intro">Selected publications. For the full list, see my '
        f'<a href="{scholar}" target="_blank" rel="noopener">Google Scholar profile</a>.</p>'
    )
    years = []
    for year in sorted(groups, reverse=True):
        rows = "\n".join(render_pub(pub) for pub in groups[year])
        years.append(f'    <div class="pub-year-group">\n      <h3 class="pub-year">{year}</h3>\n{rows}\n    </div>')
    return intro + "\n" + "\n".join(years)


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
#publications {{ font-family:Georgia,"Times New Roman",serif; }}
#publications > h2 {{ border:0; padding:0; font-size:2rem; line-height:1.2; letter-spacing:-.02em; }}
.pub-intro {{ max-width:42rem; margin:.9rem 0 2.2rem 176px; color:#4b5563; font-size:1rem; line-height:1.55; }}
.pub-year-group {{ margin:0 0 2.3rem; }}
.pub-year {{ color:#740082; font-size:1.45rem; font-weight:500; margin:0 0 .8rem; }}
.pub {{ display:grid; grid-template-columns:150px minmax(0,1fr); gap:1.6rem; margin:0 0 2rem; align-items:start; }}
.pub-side {{ min-width:0; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif; }}
.pub-venue {{ font-size:.78rem; font-weight:600; color:#20253b; line-height:1.35; margin:.1rem 0 .6rem; }}
.pub-image-link {{ display:block; width:140px; }}
.pub-side img {{ display:block; width:140px; height:110px; object-fit:contain; background:#fff; border:1px solid #e1dfeb; border-radius:3px; box-shadow:0 3px 9px rgba(31,41,55,.09); }}
.pub-body {{ min-width:0; }}
.pub-title {{ margin:0 0 .25rem; font-size:1.08rem; line-height:1.35; }}
.pub-title a {{ color:#1d1830; }}
.pub-title a:hover {{ color:#740082; }}
.pub-authors {{ margin:.15rem 0 .25rem; color:#606071; font-size:.94rem; line-height:1.45; }}
.pub-authors strong {{ color:#222039; }}
.pub-links {{ display:flex; gap:1rem; flex-wrap:wrap; font-size:.87rem; }}
.pub-links .btn {{ color:#740082; text-decoration:underline; text-underline-offset:2px; }}
.pub-links .btn:hover {{ color:#4c0057; }}
.contact {{ list-style:none; padding:0; margin:0; color:var(--muted); }}
footer {{ text-align:center; color:var(--muted); font-size:.82rem; padding:1.6rem 0; }}
@media (max-width:560px) {{
  .pub-intro {{ margin-left:0; }}
  .pub {{ grid-template-columns:92px minmax(0,1fr); gap:1rem; margin-bottom:1.8rem; }}
  .pub-side img,.pub-image-link {{ width:92px; }}
  .pub-side img {{ height:82px; }}
  .pub-title {{ font-size:1rem; }}
  .pub-authors {{ font-size:.87rem; }}
}}
@media (max-width:360px) {{ .pub {{ grid-template-columns:1fr; }} .pub-side img,.pub-image-link {{ width:140px; }} }}
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
        pubs=render_publications(pubs, prof.get("social", {}).get("Google Scholar", "")),
        contact=contact,
    )
    with open(os.path.join(HERE, "index.html"), "w", encoding="utf-8") as f:
        f.write(out)
    print(f"Wrote index.html ({len(out)} bytes, {len(pubs)} publications)")


if __name__ == "__main__":
    main()
