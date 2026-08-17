# A Pulp Of Man

A shelf of scrolls. Each scroll is one handwritten page. Tap one and it lifts off the
shelf and unrolls. Anything written today wears a small blue feather.

Publishing a new entry from your phone is one action: **upload the photo into the
`entries` folder.** There is no CMS, no build step, no database. The site reads the
folder itself.

---

## One-time setup (about ten minutes, on a computer)

**1. Make the repository.**
Go to github.com → **New repository**. Name it `a-pulp-of-man`. Make it **Public**
(GitHub Pages needs public on the free plan). Create it.

**2. Upload these files.**
On the new repo's page: **Add file → Upload files**, then drag in everything from
this folder — `index.html`, `entries.json`, the `assets` folder, and the `entries`
folder. Commit.

**3. Tell the site where it lives.**
Open `index.html` in GitHub (click it, then the pencil icon) and edit the four lines
near the top:

```js
const SOURCE = {
  user:   "your-github-username",
  repo:   "a-pulp-of-man",
  branch: "main",
  dir:    "entries"
};
```

Commit the change.

**4. Turn on the site.**
Repo **Settings → Pages**. Under *Source* choose **Deploy from a branch**, branch
`main`, folder `/ (root)`. Save. A minute later your site is live at:

```
https://your-github-username.github.io/a-pulp-of-man/
```

Add that to your phone's home screen and it behaves like an app.

**5. Delete the samples.**
The five `*-sample.jpg` files in `entries/` are placeholders. Delete them whenever
you like — the shelf will simply hold your own pages.

---

## Publishing from your phone

1. Photograph the page. Straight on, good light. Crop to the paper.
2. Open your repo in the GitHub app or in mobile Safari/Chrome.
3. Go into the **`entries`** folder → **Add file → Upload files** → choose the photo.
4. **Rename it so it starts with the date**, then commit.

```
2026-08-17.jpg
2026-08-17-morning.jpg      ← anything after the date is ignored
2026-08-17-2.jpg            ← a second entry the same day
```

The shelf updates within a minute. A page dated today gets the blue feather
automatically — nothing to switch on.

### The one rule

**The filename must begin with `YYYY-MM-DD`.** That is where the date on the scroll
comes from, and how the shelf sorts itself (newest at the top left). A file without a
date still appears, just without a date on it.

### A note on formats

Upload **JPG, PNG or WEBP**. iPhones sometimes hand over `.HEIC`, which Safari can
display but Chrome and Android cannot. In iOS: **Settings → Camera → Formats → Most
Compatible** makes the phone shoot JPEG from then on. Photos shared out of the Photos
app are usually converted to JPEG anyway.

Around 1–2 MB per photo is plenty — the scroll shows the page about 560 pixels wide
and lets you tap to zoom in.

---

## Reading it

- **Tap a scroll** — it lifts off the shelf and unrolls.
- **Tap the page** — zooms in, for handwriting that's gone small.
- **Tap the dark surround, either roll, or press Esc** — it rolls back up.

There is deliberately nothing else on screen. No menu, no buttons, no footer.

---

## How it finds your entries

The page asks the GitHub API for a listing of the `entries` folder and builds a scroll
per image. That call is anonymous, so GitHub allows about 60 per hour from a given
network — far more than one person reading a blog. If it ever fails, the site falls
back to `entries.json`, a plain list of filenames. You don't have to maintain that
file; it exists only as a safety net for the samples.

Nothing is tracked. There are no cookies, no analytics, no third-party scripts beyond
the two fonts.

---

## The look, if you ever want to change it

Everything visual is procedural — the cobblestone wall, the stone shelf and the eight
scroll variants are all rendered by one Python script rather than downloaded from
anywhere.

```bash
pip install numpy pillow
python3 tools/render_assets.py
```

That regenerates everything in `assets/`. Change `seed=7` in `cobblestone()` for a
different wall; the palette, mortar width and lamp direction are all named constants
near the top of each function. `tools/make_samples.py` regenerates the placeholder
handwriting.

The layout knobs live in the `:root` block at the top of `index.html`:

| variable | what it does |
|---|---|
| `--rowH` | vertical space one shelf occupies |
| `--base` | gap under a scroll's foot: slab front plus its shadow |
| `--sink` | how far onto the slab's top surface the scrolls stand |
| `--ink` | the colour of the date written on each roll |

---

## Files

```
index.html          the whole site
entries/            your photographs — this is the only folder you touch
entries.json        fallback listing, only used if the GitHub API is unreachable
assets/             rendered wall, shelf, scrolls, rolls, paper
tools/              the Python that renders assets/ and the sample pages
```
