#!/usr/bin/env python3
"""
Static site generator for the Shawn Wang photography portfolio.

Structure (3 tiers):
  index.html            Photography overview — three category hero sections
  <category>.html       Portraits / Travel / Misc — grid of project covers
  <project>.html        Individual project — full-bleed hero + photo grid + lightbox

Everything is plain static HTML/CSS/JS; this script just keeps the 13 pages
consistent. Edit the data below and re-run:  python3 generate.py

Image order in each project's `images` list == display order in the grid and
lightbox. Reorder to re-sequence a project.
"""
import html

BRAND = "Shawn Wang"

# ---- category order + overview hero shots -------------------------------
CATEGORIES = [
    {"slug": "portraits", "name": "Portraits", "hero": "dunes-05",   "pos": "50% 50%"},
    {"slug": "travel",    "name": "Travel",    "hero": "iceland-11", "pos": "50% 50%"},
    {"slug": "misc",      "name": "Misc",      "hero": "home-09",    "pos": "50% 45%"},
]

# ---- projects (curated sequence lives in `images`) ----------------------
PROJECTS = [
    # Portraits
    {"slug": "kristin-paint", "title": "Kristin · Paint", "category": "portraits",
     "year": "2023", "hero": "paint-01", "hero_pos": "50% 30%", "cover": "paint-01",
     "images": ["paint-02", "paint-05", "paint-03", "paint-04", "paint-01"]},
    {"slug": "claire-beach", "title": "Claire · Beach", "category": "portraits",
     "year": "2024", "hero": "claire-02", "hero_pos": "50% 40%", "cover": "claire-05",
     "images": ["claire-02", "claire-05", "claire-07", "claire-03", "claire-01",
                "claire-09", "claire-04", "claire-06", "claire-08"]},
    {"slug": "kristin-dunes", "title": "Kristin · Dunes", "category": "portraits",
     "year": "2024", "hero": "dunes-05", "hero_pos": "50% 50%", "cover": "dunes-14",
     "images": ["dunes-02", "dunes-14", "dunes-05", "dunes-10", "dunes-07", "dunes-06",
                "dunes-01", "dunes-13", "dunes-17", "dunes-03", "dunes-15", "dunes-08",
                "dunes-11", "dunes-09", "dunes-12", "dunes-04", "dunes-16"]},
    {"slug": "kristin-palos-verdes", "title": "Kristin · Palos Verdes", "category": "portraits",
     "year": "2024", "hero": "palos-05", "hero_pos": "50% 45%", "cover": "palos-04",
     "images": ["palos-04", "palos-02", "palos-03", "palos-01", "palos-05",
                "palos-06", "palos-07", "palos-08", "palos-09"]},
    # Travel
    {"slug": "asia", "title": "Asia", "category": "travel",
     "year": "2024", "hero": "asia-09", "hero_pos": "50% 45%", "cover": "asia-09",
     "images": ["asia-02", "asia-01", "asia-06", "asia-09", "asia-03", "asia-12",
                "asia-04", "asia-10", "asia-07", "asia-08", "asia-11", "asia-05"]},
    {"slug": "iceland", "title": "Iceland", "category": "travel",
     "year": "", "hero": "iceland-11", "hero_pos": "50% 55%", "cover": "iceland-16",
     "images": ["iceland-01", "iceland-06", "iceland-05", "iceland-02", "iceland-16",
                "iceland-07", "iceland-13", "iceland-03", "iceland-11", "iceland-12",
                "iceland-08", "iceland-19", "iceland-04", "iceland-18", "iceland-09",
                "iceland-14", "iceland-10", "iceland-17", "iceland-15", "iceland-20"]},
    {"slug": "xinjiang", "title": "Xinjiang", "category": "travel",
     "year": "", "hero": "xinjiang-01", "hero_pos": "50% 46%", "cover": "xinjiang-01",
     "images": [f"xinjiang-{i:02d}" for i in range(1, 20)]},
    # Misc
    {"slug": "home", "title": "Home", "category": "misc",
     "year": "2022", "hero": "home-09", "hero_pos": "50% 45%", "cover": "home-08",
     "images": ["home-01", "home-03", "home-02", "home-05", "home-07", "home-09",
                "home-04", "home-06", "home-10", "home-08", "home-11", "home-12", "home-13"]},
    {"slug": "lighthouse-bell-works", "title": "Lighthouse & Bell Works", "category": "misc",
     "year": "2025", "hero": "lighthouse-09", "hero_pos": "50% 50%", "cover": "lighthouse-09",
     "images": ["lighthouse-01", "lighthouse-03", "lighthouse-05", "lighthouse-02",
                "lighthouse-04", "lighthouse-06", "lighthouse-08", "lighthouse-07",
                "lighthouse-09", "lighthouse-10"]},
]

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'"
           "%3E%3Crect width='32' height='32' fill='%231c1a17'/%3E%3Ccircle cx='16' cy='16' r='8'"
           " fill='none' stroke='%23f6f3ee' stroke-width='1.5'/%3E%3Cline x1='16' y1='8' x2='16'"
           " y2='24' stroke='%23f6f3ee' stroke-width='1.5'/%3E%3Cline x1='8' y1='16' x2='24' y2='16'"
           " stroke='%23f6f3ee' stroke-width='1.5' transform='rotate(45 16 16)'/%3E%3C/svg%3E")

# ------------------------------------------------------------------ helpers
def cat_by_slug(slug):
    return next(c for c in CATEGORIES if c["slug"] == slug)

def projects_in(cat_slug):
    return [p for p in PROJECTS if p["category"] == cat_slug]

def meta_line(p):
    n = len(p["images"])
    frames = f"{n} photographs"
    return f"{p['year']} &middot; {frames}" if p["year"] else frames

def head(title, desc):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(desc)}" />
  <link rel="icon" href="{FAVICON}" />
  <link rel="stylesheet" href="styles.css" />
</head>
<body>"""

def header():
    return f"""
  <header class="site-header" id="top">
    <a class="wordmark" href="index.html" aria-label="{BRAND} — home">
      Shawn<span class="wordmark__thin">Wang</span>
    </a>
    <nav class="nav" aria-label="Primary">
      <a href="index.html">Photography</a>
      <a href="#contact">Contact</a>
    </nav>
  </header>"""

def contact():
    return """
    <section class="contact" id="contact">
      <div class="contact__inner reveal">
        <p class="eyebrow">Contact</p>
        <a class="contact__email" href="mailto:shawn.wang.1667@gmail.com">shawn.wang.1667@gmail.com</a>
      </div>
    </section>"""

def footer():
    return f"""
  <footer class="site-footer">
    <span>&copy; <span id="year"></span> {BRAND}</span>
    <a href="#top">Back to top &uarr;</a>
  </footer>"""

def lightbox():
    return """
  <div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Image viewer" hidden>
    <button class="lightbox__close" id="lb-close" aria-label="Close">&times;</button>
    <button class="lightbox__nav lightbox__nav--prev" id="lb-prev" aria-label="Previous image">&#8249;</button>
    <figure class="lightbox__stage">
      <img class="lightbox__img" id="lb-img" src="" alt="" />
      <figcaption class="lightbox__caption"><span id="lb-count"></span></figcaption>
    </figure>
    <button class="lightbox__nav lightbox__nav--next" id="lb-next" aria-label="Next image">&#8250;</button>
  </div>

  <script src="script.js"></script>
</body>
</html>
"""

# ------------------------------------------------------------------ pages
def render_home():
    parts = [head(f"{BRAND} — Photography",
                  f"Photography by {BRAND} — portraits, travel, and more."),
             f'<h1 class="sr-only">{BRAND} — Photography</h1>',
             header(), '\n  <main class="overview">']
    for c in CATEGORIES:
        n = len(projects_in(c["slug"]))
        parts.append(f"""
    <a class="cat-hero reveal" href="{c['slug']}.html" aria-label="{c['name']} — view series">
      <img class="cat-hero__img" src="assets/full/{c['hero']}.jpg" alt="" style="object-position:{c['pos']}" />
      <span class="cat-hero__scrim" aria-hidden="true"></span>
      <span class="cat-hero__content">
        <span class="cat-hero__title">{c['name']}</span>
        <span class="cat-hero__meta">{n} series</span>
        <span class="cat-hero__cta">View</span>
      </span>
    </a>""")
    parts.append("\n" + contact() + "\n  </main>")
    parts.append(footer())
    # home has no gallery, but keep script for footer year (lightbox markup omitted)
    parts.append('\n  <script src="script.js"></script>\n</body>\n</html>\n')
    return "".join(parts)

def render_category(c):
    parts = [head(f"{c['name']} — {BRAND}",
                  f"{c['name']} photography by {BRAND}."),
             header(),
             f"""
  <main>
    <div class="page-head reveal">
      <p class="eyebrow">Photography</p>
      <h1 class="page-head__title">{c['name']}</h1>
    </div>
    <div class="projects">"""]
    for p in projects_in(c["slug"]):
        parts.append(f"""
      <a class="project reveal" href="{p['slug']}.html">
        <span class="project__frame">
          <img class="project__img" src="assets/thumb/{p['cover']}.jpg" loading="lazy"
               width="800" height="1000" alt="{html.escape(p['title'])} — cover" />
        </span>
        <span class="project__label">
          <span class="project__title">{html.escape(p['title'])}</span>
          <span class="project__meta">{meta_line(p)}</span>
        </span>
      </a>""")
    parts.append("\n    </div>")
    parts.append(contact() + "\n  </main>")
    parts.append(footer())
    parts.append("\n  <script src=\"script.js\"></script>\n</body>\n</html>\n")
    return "".join(parts)

def render_project(p):
    c = cat_by_slug(p["category"])
    figs = []
    for i, img in enumerate(p["images"]):
        figs.append(f"""
        <figure class="shot reveal" data-full="assets/full/{img}.jpg" data-index="{i}">
          <img src="assets/thumb/{img}.jpg" loading="lazy" width="800" height="1000"
               alt="{html.escape(p['title'])} — {i + 1}" />
        </figure>""")
    parts = [head(f"{p['title']} — {BRAND}",
                  f"{p['title']} — photography by {BRAND}."),
             header(),
             f"""
  <h1 class="sr-only">{html.escape(p['title'])} — {c['name']} — {BRAND}</h1>
  <section class="hero" aria-label="{html.escape(p['title'])}">
    <img class="hero__img" src="assets/full/{p['hero']}.jpg" alt="{html.escape(p['title'])}"
         style="object-position:{p['hero_pos']}" />
    <div class="hero__scrim" aria-hidden="true"></div>
    <a class="hero__scroll" href="#work" aria-label="Scroll to photographs">
      <span>Scroll</span>
      <span class="hero__scroll-line" aria-hidden="true"></span>
    </a>
  </section>

  <main>
    <p class="breadcrumb">
      <a href="index.html">Photography</a><span>/</span><a href="{c['slug']}.html">{c['name']}</a><span>/</span>{html.escape(p['title'])}
    </p>
    <section class="work" id="work">
      <div class="gallery" id="gallery">{''.join(figs)}
      </div>
    </section>""",
             contact() + "\n  </main>",
             footer(),
             lightbox()]
    return "".join(parts)

def main():
    written = []
    with open("index.html", "w") as f:
        f.write(render_home())
    written.append("index.html")
    for c in CATEGORIES:
        fn = f"{c['slug']}.html"
        with open(fn, "w") as f:
            f.write(render_category(c))
        written.append(fn)
    for p in PROJECTS:
        fn = f"{p['slug']}.html"
        with open(fn, "w") as f:
            f.write(render_project(p))
        written.append(fn)
    print(f"Generated {len(written)} pages:")
    for w in written:
        print("  " + w)

if __name__ == "__main__":
    main()
