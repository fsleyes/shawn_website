#!/usr/bin/env python3
"""
Static site generator for the Shawn Wang photography portfolio.

Structure (2 tiers, organized by theme rather than by shoot):
  index.html          Photography overview — one full-width hero tile per theme
  <theme>.html        One theme — full-bleed hero + photo grid + lightbox

Everything is plain static HTML/CSS/JS; this script just keeps the 9 pages
consistent. Edit the data below and re-run:  python3 generate.py

Image order in each theme's `images` list == display order in the grid and
lightbox. Reorder to re-sequence a theme. Every photo on the site belongs to
exactly one theme (checked at generation time).
"""
import html
import os
import sys

BRAND = "Shawn Wang"

# ---- themes: overview order, hero image, and curated sequence ------------
# `hero` is both the overview tile and the full-bleed image atop the theme page.
# `label: "low"` bottom-aligns the overview title (use when the hero's subject is centred).
THEMES = [
    # people in colour and landscape, medium to full-length — red/blue desert opener,
    # paint and meadow pages in the middle, ends on the cream-backdrop frame
    {"slug": "figures", "name": "Figures", "hero": "dunes-10", "hero_pos": "50% 42%",
     "images": ["dunes-10", "paint-02", "salton-07", "palos-04", "dunes-13", "poppies-01",
                "paint-05", "idaho-02", "dunes-17", "dunes-03", "palos-08", "salton-04",
                "poppies-04", "paint-03", "lighthouse-06", "palos-03", "dunes-04", "salton-01",
                "dunes-09", "poppies-05", "paint-04", "palos-06", "dunes-11", "dunes-02",
                "palos-07", "paint-01"]},
    # built geometry — slats and spires, colour-blocked facades; closes on the black church
    {"slug": "structure", "name": "Structure", "hero": "lighthouse-09", "hero_pos": "50% 50%",
     "images": ["lighthouse-09", "iceland-16", "xinjiang-04", "asia-09", "seattle-04", "iceland-18",
                "asia-12", "lighthouse-02", "xinjiang-02", "iceland-05", "asia-10", "lighthouse-07",
                "iceland-19", "xinjiang-06", "asia-03", "lighthouse-04", "iceland-14", "seattle-05",
                "asia-08", "lighthouse-10", "xinjiang-19", "iceland-10", "asia-11", "lighthouse-03",
                "lighthouse-08", "iceland-20"]},
    # close, direct-address portraits — warm opener, hard white tile in the middle,
    # closes on the quiet black-and-white frame
    {"slug": "faces", "name": "Faces", "hero": "studio-01", "hero_pos": "50% 53%", "label": "low",
     "images": ["studio-01", "dunes-14", "poppies-03", "palos-02", "bathroom-06", "studio-03",
                "dunes-01", "idaho-03", "palos-01", "salton-06", "dunes-07", "studio-02",
                "poppies-06", "bathroom-07", "dunes-15", "bathroom-05", "studio-04"]},
    # open places and the wires that cross them — glacier to suburban dusk, 31 photos
    {"slug": "land", "name": "Land", "hero": "iceland-11", "hero_pos": "50% 55%",
     "images": ["iceland-06", "home-02", "boise-01", "iceland-08", "seattle-06", "iceland-03",
                "home-05", "xinjiang-09", "iceland-12", "boise-07", "home-04", "iceland-15",
                "lighthouse-01", "iceland-07", "boise-03", "home-10", "iceland-02", "xinjiang-17",
                "seattle-07", "iceland-09", "boise-02", "home-01", "iceland-11", "xinjiang-13",
                "boise-04", "iceland-01", "home-12", "iceland-04", "home-13", "iceland-17",
                "home-09"]},
    # dark rooms, gel light, long exposure — interleaved so no one series runs long;
    # closes on the clearest of the blur frames
    {"slug": "after-dark", "name": "After Dark", "hero": "blur-06", "hero_pos": "55% 47%", "label": "low",
     "images": ["claire-02", "claire-05", "bathroom-04", "blur-01", "claire-07", "bathroom-01",
                "claire-03", "blur-02", "idaho-04", "claire-01", "bathroom-02", "blur-03",
                "claire-09", "seattle-02", "claire-04", "bathroom-03", "blur-04", "claire-06",
                "blur-05", "claire-08", "blur-06"]},
    # people observed in transit, at work, at rest
    {"slug": "street", "name": "Street", "hero": "asia-01", "hero_pos": "50% 45%",
     "images": ["asia-06", "xinjiang-03", "asia-01", "xinjiang-05", "boise-06", "xinjiang-08",
                "asia-07", "xinjiang-07", "seattle-01", "xinjiang-14", "asia-04", "xinjiang-16",
                "boise-05", "xinjiang-11", "xinjiang-01", "xinjiang-15"]},
    # tiny figures in big space — the portraits and the travel work meeting in scale
    {"slug": "distance", "name": "Distance", "hero": "dunes-05", "hero_pos": "50% 62%",
     "images": ["dunes-05", "xinjiang-18", "asia-02", "salton-05", "poppies-02", "lighthouse-05",
                "dunes-08", "palos-09", "idaho-01", "xinjiang-10", "dunes-12", "seattle-03",
                "salton-03", "asia-05", "dunes-06", "xinjiang-12", "dunes-16", "palos-05"]},
    # family and the rooms they live in
    {"slug": "home", "name": "Home", "hero": "orangetree-01", "hero_pos": "50% 60%",
     "images": ["orangetree-01", "home-03", "orangetree-04", "home-07", "home-08", "orangetree-02",
                "iceland-13", "home-06", "orangetree-05", "home-11", "orangetree-03",
                "orangetree-06"]},
]

# Grid thumbnails are cropped to 4:5; for wide frames where the subject sits off-centre,
# name the crop's focal point here (CSS object-position) so the subject isn't clipped.
GRID_FOCUS = {
    "dunes-08": "95% 50%",   # tiny figure on the ridge, right of centre
    "dunes-16": "85% 50%",
}

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'"
           "%3E%3Crect width='32' height='32' fill='%231c1a17'/%3E%3Ccircle cx='16' cy='16' r='8'"
           " fill='none' stroke='%23f6f3ee' stroke-width='1.5'/%3E%3Cline x1='16' y1='8' x2='16'"
           " y2='24' stroke='%23f6f3ee' stroke-width='1.5'/%3E%3Cline x1='8' y1='16' x2='24' y2='16'"
           " stroke='%23f6f3ee' stroke-width='1.5' transform='rotate(45 16 16)'/%3E%3C/svg%3E")

# ------------------------------------------------------------------ helpers
def check_themes():
    """Every image exists, and none is repeated within or across themes."""
    seen = {}
    problems = []
    for t in THEMES:
        for img in t["images"]:
            if img in seen:
                problems.append(f"{img} is in both '{seen[img]}' and '{t['slug']}'")
            seen[img] = t["slug"]
            for kind in ("full", "thumb"):
                if not os.path.exists(f"assets/{kind}/{img}.jpg"):
                    problems.append(f"missing assets/{kind}/{img}.jpg")
        if t["hero"] not in t["images"]:
            problems.append(f"hero {t['hero']} is not in theme '{t['slug']}'")
    on_disk = {f[:-4] for f in os.listdir("assets/full") if f.endswith(".jpg")}
    for img in sorted(on_disk - set(seen)):
        problems.append(f"assets/full/{img}.jpg is not in any theme")
    if problems:
        sys.exit("generate.py: " + "\n  ".join(["problems found:"] + problems))
    return len(seen)

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
                  f"Photography by {BRAND}."),
             f'<h1 class="sr-only">{BRAND} — Photography</h1>',
             header(), '\n  <main class="overview">']
    for t in THEMES:
        parts.append(f"""
    <a class="cat-hero{' cat-hero--low' if t.get('label') == 'low' else ''} reveal" href="{t['slug']}.html" aria-label="{t['name']} — view photographs">
      <img class="cat-hero__img" src="assets/full/{t['hero']}.jpg" alt="" style="object-position:{t['hero_pos']}" />
      <span class="cat-hero__scrim" aria-hidden="true"></span>
      <span class="cat-hero__content">
        <span class="cat-hero__title">{t['name']}</span>
        <span class="cat-hero__meta">{len(t['images'])} photographs</span>
        <span class="cat-hero__cta">View</span>
      </span>
    </a>""")
    parts.append("\n" + contact() + "\n  </main>")
    parts.append(footer())
    # overview has no gallery, but keep script for footer year (lightbox markup omitted)
    parts.append('\n  <script src="script.js"></script>\n</body>\n</html>\n')
    return "".join(parts)

def render_theme(t):
    name = html.escape(t["name"])
    figs = []
    for i, img in enumerate(t["images"]):
        focus = f' style="object-position:{GRID_FOCUS[img]}"' if img in GRID_FOCUS else ""
        figs.append(f"""
        <figure class="shot reveal" data-full="assets/full/{img}.jpg" data-index="{i}">
          <img src="assets/thumb/{img}.jpg" loading="lazy" width="800" height="1000"
               alt="{name} — {i + 1}"{focus} />
        </figure>""")
    parts = [head(f"{t['name']} — {BRAND}",
                  f"{t['name']} — photography by {BRAND}."),
             header(),
             f"""
  <h1 class="sr-only">{name} — {BRAND}</h1>
  <section class="hero" aria-label="{name}">
    <img class="hero__img" src="assets/full/{t['hero']}.jpg" alt="{name}"
         style="object-position:{t['hero_pos']}" />
    <div class="hero__scrim" aria-hidden="true"></div>
    <a class="hero__scroll" href="#work" aria-label="Scroll to photographs">
      <span>Scroll</span>
      <span class="hero__scroll-line" aria-hidden="true"></span>
    </a>
  </section>

  <main>
    <p class="breadcrumb">
      <a href="index.html">Photography</a><span>/</span>{name}
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
    total = check_themes()
    written = []
    with open("index.html", "w") as f:
        f.write(render_home())
    written.append("index.html")
    for t in THEMES:
        fn = f"{t['slug']}.html"
        with open(fn, "w") as f:
            f.write(render_theme(t))
        written.append(fn)
    print(f"Generated {len(written)} pages ({total} photographs in {len(THEMES)} themes):")
    for w in written:
        print("  " + w)

if __name__ == "__main__":
    main()
