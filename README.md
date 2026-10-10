# Portfolio Site

A minimal photography portfolio. Plain static HTML/CSS/JS — no build tooling to
deploy, no dependencies. Type is Helvetica, headers bold (Off-White style);
photos run caption-free and stand on their own.

## Structure (2 tiers, organized by theme)

```
index.html               Photography overview — one full-width hero tile per theme
<theme>.html             One theme — hero + staggered photo grid + lightbox
                         (figures, structure, faces, land, after-dark, street,
                          distance, home)
styles.css               all styling (warm gallery theme, Helvetica)
script.js                lightbox, scroll reveal, footer year
generate.py              regenerates every HTML page from the data at its top
assets/full/             web-optimized images for hero + lightbox
assets/thumb/            smaller images for the grids
photos/<category>/<shoot>/   your original full-res files (not served)
```

Navigation: one **Photography** nav item → the overview. Each overview tile is a
clickable hero shot → that theme's gallery. Every page carries a Contact section and
footer; theme pages show a breadcrumb.

The site used to be organized by shoot (Portraits / Travel / Misc → project pages).
It was regrouped by theme so photos from different shoots sit together. Every photo
belongs to exactly one theme, and `generate.py` refuses to run if a photo is in two
themes, missing, or on disk but unused.

| Theme | Photos | What it holds |
|---|---|---|
| Figures | 26 | people in colour and landscape, medium to full-length |
| Structure | 26 | built geometry: spires, slats, facades |
| Faces | 17 | close, direct-address portraits |
| Land | 31 | open places and the wires that cross them (kept as one theme on purpose) |
| After Dark | 21 | dark rooms, gel light, long exposure |
| Street | 16 | people observed in transit, at work, at rest |
| Distance | 18 | tiny figures in big space |
| Home | 12 | family and the rooms they live in |

Source shoots are noted in the file names (`dunes-`, `palos-`, `iceland-`, …) — the
prefix is the shoot, not the theme. Several shoots span themes (e.g. Dunes feeds
Faces, Figures and Distance); Beach, Blur, Paint, Studio and Orange Tree stay whole.
Site titles never contain subject names.

## Run it

Open `index.html` in a browser, or serve locally:

```bash
python3 -m http.server 8000   # then visit http://localhost:8000
```

## The generator

The 9 pages are generated so they stay consistent. Edit the data at the top of
`generate.py` (the `THEMES` list and each theme's ordered `images` list), then run:

```bash
python3 generate.py
```

`images` order == display order in the grid and lightbox — reorder that list to
re-sequence a theme. `hero` is both the overview tile and the full-bleed image at
the top of the theme page. Optional knobs:

- `label: "low"` on a theme bottom-aligns its overview title (use when the hero's
  subject is centred and the title would land on a face).
- `GRID_FOCUS` names a crop focal point for a wide photo whose subject would be
  clipped by the 4:5 grid crop (currently two Dunes frames).

## Adding photos

1. Drop originals in `photos/<category>/<shoot>/` (originals live outside this repo
   and are never committed).
2. Optimize into `assets/full` and `assets/thumb`, naming them `<prefix>-01.jpg`, …
   Use Pillow, not `sips` — it compresses ~35% smaller at the same visual quality
   and strips EXIF:
   ```python
   from PIL import Image, ImageOps
   for kind, px, q in (("full", 1500, 70), ("thumb", 850, 68)):
       im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")  # fix rotation, drop EXIF
       im.thumbnail((px, px), Image.LANCZOS)
       im.save(f"assets/{kind}/{name}.jpg", "JPEG",
               quality=q, optimize=True, progressive=True)
   ```
3. Add each new image id to the `images` list of the theme it belongs in (or add a
   new theme dict), then run `python3 generate.py`. It will tell you if an image
   on disk isn't in any theme.

## Notes

- **Branding:** the nav wordmark and contact email are set in `generate.py`
  (currently Shawn Wang / shawn.wang.1667@gmail.com) — edit there, then regenerate.
- **Titles** are single-word themes — no subject or place names.
- **Image weight:** keep `assets/` lean, it is the only heavy thing in the repo
  (~31 MB for 167 photos). Re-run the optimizer above rather than committing
  anything straight out of Lightroom.
- **Grid crop:** grid thumbnails are a uniform 4:5 crop for a consistent wall;
  the lightbox always shows the full frame. Landscape shots (a few in Iceland /
  Dunes) are center-cropped in the grid only.
- Colors and fonts are CSS variables at the top of `styles.css`.

## Deploy

Fully static — drop the folder on Netlify, Vercel, GitHub Pages, or any host.
`generate.py`, `photos/`, and `README.md` aren't required at runtime.
