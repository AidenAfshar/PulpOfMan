# A Pulp Of Man

A shelf of scrolls at **pulpofman.com**. Each scroll is one handwritten page. Tap one
and it lifts off the shelf and unrolls. Anything dated today wears a small blue
feather.

Entries live in a **Google Drive folder**. Publishing is: photograph the page, put it
in the folder, name it with the date. No CMS, no build step, no database.

---

## Setup

Four parts. Do them in this order — the Drive half is the fiddly bit, so it's first,
while you still have patience.

### Part 1 — Google Drive

A static web page can't hold a Google password, so a tiny script stands between them.
It lists one folder and hands the site a plain list of filenames. It can't write,
delete, or see anything outside that folder.

**1. Make the folder.**
In Drive, create a folder — call it `Pulp Of Man`. Open it. The address bar reads
`.../folders/1a2B3c4D5e6F7g8H`. **That tail is the folder ID.** Copy it.

**2. Share it.**
Right-click the folder → **Share** → under *General access* choose
**Anyone with the link**, role **Viewer**. This is what lets the browser actually
display the photographs. The folder stays unlisted and unsearchable — only reachable
by someone holding an exact file ID.

**3. Make the relay.**
Go to **script.google.com** → **New project**. Delete everything in the editor and
paste in the whole of `tools/drive-relay.gs` from this folder. Name the project
`Pulp Of Man`. Put your folder ID into the `FOLDER_ID` line near the top. Save.

**4. Check it before deploying.**
In the toolbar, pick `test` from the function dropdown and press **Run**. Approve the
permissions when asked — the "Google hasn't verified this app" screen is expected for
a script you wrote yourself: **Advanced → Go to Pulp Of Man (unsafe)**. The Execution
log should print `"ok":true` and a count. If it says `ok:false`, the folder ID is
wrong.

**5. Deploy it.**
**Deploy → New deployment →** click the gear → **Web app**.

| field | value |
|---|---|
| Execute as | **Me** |
| Who has access | **Anyone** |

That second one must be plain **Anyone**, *not* "Anyone with a Google account" —
otherwise visitors get a login screen instead of your writing. Deploy, then copy the
**Web app URL**. It ends in `/exec`.

**6. Paste it into the site.**
Near the top of `index.html`:

```js
const SOURCE = {
  drive: "https://script.google.com/macros/s/AKfy…/exec",
  ...
};
```

### Part 2 — hosting

The page itself still needs somewhere to live. GitHub Pages is free and fine.

1. github.com → **New repository**, named `a-pulp-of-man`, **Public**.
2. **Add file → Upload files**, drag in everything from this folder, commit.
3. **Settings → Pages** → Source: **Deploy from a branch**, branch `main`, folder
   `/ (root)`. Save.

### Part 3 — pulpofman.com

At your registrar's DNS settings, add:

| Type | Name | Value |
|---|---|---|
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |
| CNAME | `www` | `your-github-username.github.io` |

Optionally add these four as `AAAA` records on `@` for IPv6:
`2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`,
`2606:50c0:8003::153`.

Then **Settings → Pages → Custom domain** should already read `pulpofman.com` — the
`CNAME` file in this folder sets it. Wait until the **Enforce HTTPS** checkbox becomes
available and tick it; that's what puts the padlock in the address bar. GitHub needs
to see your DNS resolve first, usually minutes.

**On Cloudflare:** keep both records **DNS only** (grey cloud) until the certificate
has issued. The orange proxy during setup is the usual reason certificates never
appear.

**Expect a broken window.** Because `CNAME` ships in this folder, the old
`username.github.io/a-pulp-of-man` address redirects to `pulpofman.com` from the
moment you upload — so between uploading and DNS propagating, the site looks dead.
That's normal.

### Part 4 — your home screen

Open `https://pulpofman.com` on your phone → Share → **Add to Home Screen**. It gets a
proper icon and opens without browser chrome.

---

## Publishing from your phone

1. Photograph the page. Straight on, good light, cropped to the paper.
2. Open the **Google Drive** app → your `Pulp Of Man` folder → **+** → **Upload** →
   pick the photo.
3. Long-press it → **Rename** → give it the date:

```
2026-08-17.jpg
2026-08-17-morning.jpg      ← anything after the date is ignored
2026-08-17-2.jpg            ← a second entry the same day
```

The shelf catches up within a minute or two — the relay holds its answer for sixty
seconds, and browsers cache a little beyond that.

### The one rule

**The filename must carry `YYYY-MM-DD`.** That's the date inked down the scroll, and
it's what sorts the shelf — newest at the top left. A photo dated today grows the
feather on its own.

A file with no date, or a nonsense one like `2026-13-99`, still appears — bare, at the
very end of the shelf. Nothing ever disappears silently; if you see an unlabelled
scroll, that's a filename asking to be fixed.

### HEIC

Upload whatever your phone shoots. Google renders HEIC as JPEG on the way out, so
iPhone photos generally work with no conversion — which they didn't in the GitHub
version. If a page ever refuses to appear, that's the first thing to suspect.

Around 1–2 MB per photo is plenty. The scroll shows the page about 560 pixels wide and
lets you tap to zoom.

---

## Reading it

- **Tap a scroll** — it lifts off the shelf and unrolls.
- **Tap the page** — zooms in, for handwriting that's gone small.
- **Tap the dark surround, either roll, or press Esc** — it rolls back up.

Nothing else on screen. No menu, no buttons, no footer.

---

## When something doesn't show up

Open the site, then your browser's console (on a desktop: right-click → Inspect →
Console). Anything the site couldn't do is logged there, prefixed `[pulp]`.

| what you see | what it means |
|---|---|
| Shelf is empty, console says `fromDrive → relay 401/403` | The deployment's access isn't **Anyone**. Deploy → Manage deployments → edit → fix it. |
| Console says `fromDrive → Exception: … getFolderById` | Wrong `FOLDER_ID` in the script. |
| You edited the script but nothing changed | Apps Script serves the *deployed* version. Deploy → Manage deployments → pencil → **Version: New version** → Deploy. This catches everyone once. |
| Scrolls appear but pages are blank when opened | The folder isn't shared **Anyone with the link → Viewer**. |
| Console says `no address served` | Same cause — Google refused the image. Check sharing. |
| A scroll has no date on it | Its filename has no `YYYY-MM-DD`. Rename it in Drive. |

### The fallbacks

If Drive can't be reached at all, the site quietly tries the GitHub `entries/` folder,
then `entries.json`. That's why the five sample scribbles are still in this folder —
they're a safety net, not content. Delete `entries/`, `entries.json` and the GitHub
lines in `SOURCE` once Drive is working, or leave them as a spare tyre.

Nothing is tracked. No cookies, no analytics, no third-party scripts beyond the two
fonts.

---

## The look, if you ever want to change it

The cobblestone wall, the stone shelf and the eight scroll variants are rendered by
one Python script rather than downloaded from anywhere.

```bash
pip install numpy pillow
python3 tools/render_assets.py
```

Change `seed=7` in `cobblestone()` for a different wall; palette, mortar width and
lamp direction are named constants near the top of each function. `make_samples.py`
regenerates the placeholder handwriting; `social.py` re-renders the share card and
home-screen icons from the live page.

Layout knobs live in the `:root` block at the top of `index.html`:

| variable | what it does |
|---|---|
| `--rowH` | vertical space one shelf occupies |
| `--base` | gap under a scroll's foot: slab front plus its shadow |
| `--sink` | how far onto the slab's top surface the scrolls stand |
| `--ink` | the colour of the date written on each roll |

Moving to a different address means changing it in three places: the `CNAME` file, the
`og:`/`canonical` tags at the top of `index.html`, and the Pages setting.

---

## Files

```
index.html            the whole site
tools/drive-relay.gs  paste this into script.google.com — the Drive half
CNAME                 pulpofman.com — this is what claims the domain
site.webmanifest      name and icons for Add to Home Screen
assets/               rendered wall, shelf, scrolls, rolls, paper, icons, share card
entries/              fallback samples, only used if Drive is unreachable
entries.json          last-ditch fallback listing
tools/                the Python that renders assets/ and the sample pages
```
