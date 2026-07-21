# Portfolio Site

A minimal photography portfolio. Plain static HTML/CSS/JS — no build tooling to
deploy, no dependencies. Type is Helvetica, headers bold (Off-White style);
photos run caption-free and stand on their own.

## Structure (3 tiers)

```
index.html               Photography overview — 3 category hero sections
portraits.html           Category — grid of project covers
travel.html              Category
misc.html                Category
<project>.html           Individual project — hero + staggered photo grid + lightbox
styles.css               all styling (warm gallery theme, Helvetica)
script.js                lightbox, scroll reveal, footer year
generate.py              regenerates every HTML page from the data at its top
assets/full/             web-optimized images for hero + lightbox
assets/thumb/            smaller images for the grids
photos/<category>/<shoot>/   your original full-res files (not served)
```

Navigation: one **Photography** nav item → the overview. Each overview section is
a clickable hero shot → its category page → a project → the gallery. Every page
carries a Contact section and footer; project pages show a breadcrumb.

Projects by category:
- **Portraits** — Kristin · Paint, Claire · Beach, Kristin · Dunes, Kristin · Palos Verdes
- **Travel** — Asia, Iceland, Xinjiang
- **Misc** — Home, Lighthouse & Bell Works

## Run it

Open `index.html` in a browser, or serve locally:

```bash
python3 -m http.server 8000   # then visit http://localhost:8000
```

## The generator

The 13 pages are generated so they stay consistent. Edit the data at the top of
`generate.py` (categories, projects, and each project's ordered `images` list),
then run:

```bash
python3 generate.py
```

`images` order == display order in the grid and lightbox — reorder that list to
re-sequence a project. `cover` is the tile shown on the category page; `hero` is
the full-bleed image at the top of the project page.

## Adding a shoot

1. Drop originals in `photos/<category>/<shoot>/`.
2. Optimize into `assets/full` and `assets/thumb`, naming them `<prefix>-01.jpg`, …
   in capture order (see the `optimize_project` pattern used previously):
   ```bash
   sips --resampleHeightWidthMax 2000 -s format jpeg -s formatOptions 82 in.jpg --out assets/full/prefix-01.jpg
   sips --resampleHeightWidthMax 1100 -s format jpeg -s formatOptions 72 in.jpg --out assets/thumb/prefix-01.jpg
   ```
3. Add a project dict to `PROJECTS` in `generate.py` (slug, title, category, cover,
   hero, and the curated `images` order), then run `python3 generate.py`.

## Notes

- **Branding:** the nav wordmark and contact email are set in `generate.py`
  (currently Shawn Wang / shawn.wang.1667@gmail.com) — edit there, then regenerate.
- **Grid crop:** grid thumbnails are a uniform 4:5 crop for a consistent wall;
  the lightbox always shows the full frame. Landscape shots (a few in Iceland /
  Dunes) are center-cropped in the grid only.
- Colors and fonts are CSS variables at the top of `styles.css`.

## Deploy

Fully static — drop the folder on Netlify, Vercel, GitHub Pages, or any host.
`generate.py`, `photos/`, and `README.md` aren't required at runtime.
