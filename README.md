# A Pulp Of Man

A shelf of scrolls at **pulpofman.com**. Each scroll is one handwritten entry. Tap one
and it lifts off the shelf and unrolls. Anything dated today wears a small blue
feather.

Entries are photographs or PDFs sitting in the **`entries/` folder of this repo** —
`AidenAfshar/PulpOfMan`, branch `master`. No second service, no sharing settings, no
relay. If the site loads, the entries load.

To publish, you don't go anywhere: **tap the title five times** and a door opens.

---

## The hidden door

Tap **A PULP OF MAN** five times quickly. A panel appears on parchment. The first time,
it asks for a GitHub token and a PIN of your choosing; after that, just the PIN. Then
you pick a file, confirm the date, and hit Publish. The scroll appears on the shelf a
moment later.

Nothing about this is visible to anyone else. The public site has no menu, no login
link, no hint that the panel exists — five taps on a title is not something a visitor
does by accident.

### How the key is kept

Your token is **encrypted with your PIN and stored only in that browser**
(AES-GCM, key stretched from the PIN with 250,000 rounds of PBKDF2). It is never
written into `index.html`, so nothing secret is ever published — anyone can read every
byte of this repo and find no way in.

The practical consequences:

- Each device you want to post from needs setting up once. Phone and laptop each get
  their own copy.
- Clearing your browser data forgets it. Set it up again; nothing is lost.
- Someone who steals your unlocked phone could post to your blog. Nothing worse — the
  token below is scoped to this one repository.
- It needs **https**. On `pulpofman.com` that's automatic. Opening `index.html` by
  double-clicking it on your Mac will not work, because browsers withhold the crypto
  API from `file://` pages.

### Making the token

1. github.com → your avatar → **Settings** → **Developer settings** (very bottom of
   the left column) → **Personal access tokens** → **Fine-grained tokens** →
   **Generate new token**.
2. Name it `Pulp Of Man`. Expiry: your call — a year is reasonable, and the site will
   simply say GitHub refused when it lapses.
3. **Repository access** → *Only select repositories* → **PulpOfMan**.
4. **Permissions** → *Repository permissions* → **Contents** → **Read and write**.
   That is the only one. Leave everything else alone.
5. Generate, and copy the token. GitHub shows it exactly once.
6. On the site, tap the title five times, paste it in, choose a PIN, save.

A fine-grained token scoped this way can do precisely one thing: read and write files
in `PulpOfMan`. It cannot touch your other repositories, your account, or anything
else.

---

## Publishing

Tap the title five times → PIN → then:

| field | what it does |
|---|---|
| The page | Choose a photograph or a PDF. On a phone this offers your camera roll and Files. |
| Dated | Defaults to today. This is the date inked down the scroll and what sorts the shelf. |
| A word | Optional. `morning` becomes `2026-08-17-morning.jpg`. Spaces and punctuation are tidied automatically. |

Publish two things on the same date and the second quietly becomes `-2`. Nothing
overwrites anything.

### PDFs

A PDF behaves like everything else, except that **every page is drawn**, stacked end to
end, so a four-page entry becomes a genuinely long scroll. There's a faint fold where
one page meets the next.

Keep them under about 25 MB. Tap the page when it's open to zoom in — that works on
PDF pages too.

### HEIC

Your iPhone's default format is `.heic`, which Safari shows but Chrome and Android do
not. Either set **Settings → Camera → Formats → Most Compatible** so the phone shoots
JPEG, or share the photo out of the Photos app rather than picking the original file —
that converts it on the way.

### The naming rule, if you ever add files by hand

**The filename must carry `YYYY-MM-DD`.** The panel does this for you, but if you drag
files into `entries/` on GitHub or on your Mac, that's the rule. A file without a date
still appears — bare, at the very end of the shelf. Nothing disappears silently; an
unlabelled scroll is a filename asking to be fixed.

---

## Reading it

- **Tap a scroll** — it lifts off the shelf and unrolls.
- **Tap the page** — zooms in, for handwriting that's gone small.
- **Tap the dark surround, either roll, or press Esc** — it rolls back up.

Nothing else on screen.

---

## Hosting

1. The repo must be **Public**. GitHub Pages needs that on the free plan, and so does
   reading `entries/` without a login.
2. **Settings → Pages** → Source: **Deploy from a branch** → branch **`master`** →
   folder `/ (root)`.
3. **Settings → Pages → Custom domain** should read `pulpofman.com`; the `CNAME` file
   sets it. Tick **Enforce HTTPS** once the checkbox becomes available — the hidden
   door won't work without it.

DNS at your registrar:

| Type | Name | Value |
|---|---|---|
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |
| CNAME | `www` | `aidenafshar.github.io` |

On Cloudflare, keep those **DNS only** (grey cloud) until the certificate has issued.

---

## When something doesn't show up

Open the site, then the browser console (desktop: right-click → Inspect → Console).
Anything that failed is logged there, prefixed `[pulp]`.

| what you see | what it means |
|---|---|
| Shelf empty, console says `fromGitHub → github 404` | Wrong `user`/`repo`/`branch` in `SOURCE` at the top of `index.html`, or there's no `entries/` folder yet. |
| Shelf empty, console says `github 403` | You've made more than 60 anonymous requests in an hour from this network. Unlock the panel — once you do, the site uses your token and the ceiling rises to 5,000. |
| Five taps do nothing | You're on `file://` or plain `http`. The panel needs https. |
| Publish says `Resource not accessible` | The token lacks **Contents: Read and write**, or wasn't scoped to `PulpOfMan`. |
| Publish says `Bad credentials` | The token expired or was pasted with a stray space. Tap *forget this device* and set it up again. |
| Scrolls appear but pages are blank | The repo is private. Make it public. |
| PDFs hang, photos are fine | `assets/pdfjs/` didn't get uploaded — 1.5 MB, easy to miss. |

---

## About Google Drive

The site can still read from a Drive folder if you ever want it to: put an Apps Script
`/exec` URL in `SOURCE.drive` and it takes priority over the repo. `tools/drive-relay.gs`
is still here for that.

It isn't used now, and the reason is worth recording: Drive needed a public sharing
toggle, a deployed script that goes stale unless you redeploy after every edit, and an
access setting with two confusingly similar options. Three things that could quietly
break, none of which you could see from the site. Publishing into the repo has none of
those moving parts.

---

## The look, if you ever want to change it

The cobblestone wall, the stone shelf and the eight scroll variants are rendered by one
Python script rather than downloaded from anywhere.

```bash
pip install numpy pillow
python3 tools/render_assets.py
```

Change `seed=7` in `cobblestone()` for a different wall. `make_samples.py` regenerates
placeholder handwriting; `social.py` re-renders the share card and home-screen icons.

Layout knobs are in the `:root` block at the top of `index.html`:

| variable | what it does |
|---|---|
| `--rowH` | vertical space one shelf occupies |
| `--base` | gap under a scroll's foot: slab front plus its shadow |
| `--sink` | how far onto the slab's top surface the scrolls stand |
| `--ink` | the colour of the date written on each roll |

---

## Files

```
index.html            the whole site, including the hidden door
CNAME                 pulpofman.com
site.webmanifest      name and icons for Add to Home Screen
entries/              your entries — the panel writes here
assets/               rendered wall, shelf, scrolls, rolls, paper, icons, share card
assets/pdfjs/         Mozilla's pdf.js, for drawing PDF pages (Apache 2.0)
entries.json          last-ditch fallback listing; unused in normal operation
tools/                the Python that renders assets/, plus the old Drive relay
```
