# A Pulp Of Man

A shelf of scrolls at **pulpofman.com**. Each scroll is one handwritten entry. Tap one
and it lifts off the shelf and unrolls. Anything dated today wears a small blue
feather.

Entries are photographs or PDFs sitting in the **`entries/` folder of this repo** —
`AidenAfshar/PulpOfMan`, branch `master`. When you publish one, the handwriting is read
into text and that text is what the scroll shows, set in a handwriting face. The scan is
kept alongside it.

To publish, you don't go anywhere: **tap the title five times** and a door opens.

---

## The hidden door

Tap **A PULP OF MAN** five times quickly. A panel appears on parchment. The first time,
it asks for your GitHub token. After that it goes **straight to the form** — no
password, ever again on that browser. Pick a file, confirm the date, hit Publish. The
scroll appears on the shelf a moment later.

Nothing about this is visible to anyone else. The public site has no menu, no login
link, no hint that the panel exists — five taps on a title is not something a visitor
does by accident.

### How the key is kept

Your token is **kept in that browser's storage and nowhere else**. It is never written
into `index.html`, so nothing secret is published — anyone can read every byte of this
repo and find no way in.

Since there's no password, the honest position is this: **whoever is using that browser
can post.** That's the trade you asked for, and it's a reasonable one, because the token
is scoped to `PulpOfMan` with only Contents access. The worst anyone could do with it is
add or remove entries on this one blog. It cannot touch your other repositories or your
account.

So: set it up on your own devices only. If you lend a laptop, or a phone goes missing,
open the panel and tap **forget this device** — or revoke the token on GitHub, which
kills it everywhere at once.

Two smaller things:

- Each device needs setting up once. Phone and laptop each get their own copy.
- Clearing your browser data forgets it. Set it up again; nothing on the shelf is lost.

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
6. On the site, tap the title five times, paste it in, save. That's the last time
   you'll be asked for anything.

A fine-grained token scoped this way can do precisely one thing: read and write files
in `PulpOfMan`. It cannot touch your other repositories, your account, or anything
else.

---

## Publishing

Tap the title five times, and then:

| field | what it does |
|---|---|
| The page | Choose a photograph or a PDF. On a phone this offers your camera roll and Files. Choosing it starts the reading straight away. |
| Dated | Defaults to today. This is the date inked down the scroll and what sorts the shelf. |
| A word | Optional. `morning` becomes `2026-08-17-morning.jpg`. Spaces and punctuation are tidied automatically. |
| Transcript | What the model read. **Fix it here before publishing** — this is the version people see. *read it again* re-runs it. |

Publish two things on the same date and the second quietly becomes `-2`. Nothing
overwrites anything.

### Reading the handwriting

Two engines, tried in that order, so a busy server can never stop you publishing.

**1. Google, if you've given it a key.** The best reader by a distance. The reader
prefers the more accurate Pro models, preserves more detail from the page, and learns
from the last single-page transcript you corrected and published. That one reference
page and its correction stay in this browser and are sent with the next page only as
an example of your letter shapes. When Google comes
back *overloaded* — which it does, often — the site now waits and tries again, and
switches to a different model each time rather than hammering the same busy one. Four
attempts across about ten seconds.

**2. This device, always.** If Google is still refusing, or you never gave a key, the
page reads the handwriting itself with Tesseract, which lives in `assets/tesseract/`.
No key, no network, no queue, nothing that can be overloaded or rationed. About eight
seconds a page.

The status line tells you which one read it.

**Be honest with yourself about the second one.** Tesseract was built for print, not
cursive fountain pen. To give it the best chance the page is enlarged, turned grey, and
thresholded against a *local* average rather than one number for the whole sheet —
which is what copes with a shadow across the paper or ink that fades along a line. It
will still make a mess of a flowing hand. Treat it as a first draft that saves you the
typing, not as a transcription.

Either way **you correct the text before publishing** — that box is the point, and it's
the version people read.

Other things worth knowing:

- **The model is asked to be faithful, not tidy.** It keeps your line breaks, spelling,
  punctuation and mistakes, drops crossings-out, and writes `[?]` where a word defeats
  it rather than inventing one.
- **Up to 15 pages** are read in one go. A longer PDF publishes fine; the panel says so.
- **Cost.** Google's free tier would likely cover a daily journal. On this device it's
  free forever.
- **The model name isn't hardcoded.** On first use the site asks your key which models
  it can run, keeps the best four, and works down the list when one is busy.

Your Google key is stored in this browser next to the GitHub token, and — like it — is
never written into the site.

#### Getting the key

**aistudio.google.com** → **Get API key** → **Create API key**. Paste it into the second
field of the setup panel. Skip it entirely if you'd rather not: everything still works.

### PDFs

Once an entry has a transcript, the scroll shows the words and never touches the PDF —
which makes it far quicker to open. The pages are still there in the repo.

For an entry with **no** transcript — anything published before this, or where you
cleared the box — the scan is shown instead: **every page drawn**, stacked end to end,
with a faint fold where one page meets the next.

Page one is drawn before the scroll unrolls, and the rest are drawn quietly behind it
one at a time, so a long entry opens as fast as a short one and scrolling never
stutters. Opening the same entry again is instant — the last three documents you
looked at stay drawn. A PDF also begins downloading the moment your finger or cursor
lands on its scroll, before you've even tapped.

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

- **Tap a scroll** — it lifts off the shelf and unrolls, as far as the words go and no
  further. It opens large enough to read without doing anything else, and the text can
  be selected, copied, and found with the browser's own search.
- **Tap anywhere** — steps closer: normal → half again → two and a bit, then back to
  normal. It zooms around the spot you tapped, so you can walk across a page by
  tapping the bit you want. When you're in close, the page pans in both directions.
- **Pinch as much as you like.** A two-finger gesture is left alone, and won't be
  mistaken for a tap when you let go.
- **The X in the top right, or Esc** — closes it. Only those two. Tapping the dark
  surround does nothing, so you can't lose your place by mis-aiming.

Nothing else on screen, and nothing at all until you open a scroll.

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
| Five taps do nothing | Try again a little faster — all five need to land inside two and a half seconds. |
| It asks for the token again | The browser's storage was cleared, or you're in a private window. Paste it in again. |
| Publish says `Resource not accessible` | The token lacks **Contents: Read and write**, or wasn't scoped to `PulpOfMan`. |
| Publish says `Bad credentials` | The token expired or was pasted with a stray space. Tap *forget this device* and set it up again. |
| Scrolls appear but pages are blank | The repo is private. Make it public. |
| PDFs hang, photos are fine | `assets/pdfjs/` didn't get uploaded — 1.5 MB, easy to miss. |
| Reading always says "read by this device" | Google is refusing every time. Check the key, or just live with it — the local reader needs no one's permission. |
| Reading says `the on-device reader would not load` | `assets/tesseract/` didn't get uploaded. It's 15 MB across eight files. |
| Everything is in the wrong font | `assets/fonts/` didn't get uploaded. |
| Reading says `API key not valid` | The Google key was mistyped, or the Generative Language API isn't enabled on that project. Make a fresh one at aistudio.google.com. |
| Reading says `quota` or `429` | You've gone past the free tier for now. Wait, or publish without the transcript and add it later by hand. |
| A transcript is wrong | Edit `entries/<name>.txt` directly on GitHub. It's a plain text file; the scroll follows it. |
| You want the scan back for one entry | Delete its `.txt`. The scroll reverts to showing the pages. |

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

There are exactly as many shelves as it takes to hold the scrolls — one more appears
when a row fills up. Three more knobs sit in the script: `ZOOMS` near `setZoom` sets the
magnification steps, `textSize()` sets how big transcribed writing is (smaller on a
desktop so more fits, larger on a phone), and the `Math.min(760, vw * 0.92)` in
`openScroll` sets how wide a scroll opens.

---

## Files

```
index.html            the whole site, including the hidden door
CNAME                 pulpofman.com
site.webmanifest      name and icons for Add to Home Screen
entries/              your entries, and a .txt of each one's words — the panel writes both
assets/               rendered wall, shelf, scrolls, rolls, paper, icons, share card
assets/pdfjs/         Mozilla's pdf.js, for drawing PDF pages (Apache 2.0)
assets/fonts/         Cormorant Garamond, Caveat, Architects Daughter (OFL)
assets/tesseract/     the on-device reader, for when Google is busy (Apache 2.0)
entries.json          last-ditch fallback listing; unused in normal operation
tools/                the Python that renders assets/, plus the old Drive relay
```
