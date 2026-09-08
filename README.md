# A Pulp Of Man

A shelf of scrolls at **pulpofman.com**. Each scroll is one entry. Tap one and it lifts
off the shelf and unrolls. Anything dated today wears a small blue feather.

Entries are plain text files sitting in the **`entries/` folder of this repo** —
`AidenAfshar/PulpOfMan`, branch `master`. One file, named `YYYY-MM-DD-anything.txt`, is
one scroll. The words in it are what the scroll shows, set in a handwriting face.

To publish, you don't go anywhere: **tap the title five times** and a door opens.

---

## The hidden door

Tap **A PULP OF MAN** five times quickly. A panel appears on parchment. The first time,
it asks for your GitHub token. After that it goes **straight to the form** — no
password, ever again on that browser. Write the entry, confirm the date, hit Publish.
The scroll appears on the shelf a moment later.

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
| Dated | Defaults to today. This is the date inked down the scroll and what sorts the shelf. |
| A word | Optional. `morning` becomes `2026-08-17-morning.txt`. Spaces and punctuation are tidied automatically. |
| The entry | The words themselves, on a miniature unrolled scroll with the same paper, handwriting face, size, spacing and padding as the published view. What you see here is what people see. |

Publish two things on the same date and the second quietly becomes `-2`. Nothing
overwrites anything.

There is no upload, no file picker, no reading step and no second service to depend on.
The panel writes one text file and that is the entry.

### Editing an old post

On a browser that remembers the GitHub token, open any scroll normally. An **Edit**
button appears directly on the opened scroll. The scroll itself becomes the writing
surface, with Save and Cancel controls at its top. Saving creates a normal Git commit,
so simultaneous changes are rejected instead of silently overwritten. Visitors and
browsers without the saved token never see the editing controls.

The latest Git commit timestamp appears as **Last edited** at the bottom of that scroll.
Entries are read from the immutable Git blob for their exact file SHA, so raw-file
caches cannot resurrect an older version after reloading or opening the site on another
device.

### The naming rule, if you ever add files by hand

**The filename must carry `YYYY-MM-DD` and end in `.txt`.** The panel does this for you,
but if you drag files into `entries/` on GitHub or on your Mac, that's the rule. A file
without a date still appears — bare, at the very end of the shelf. Nothing disappears
silently; an unlabelled scroll is a filename asking to be fixed.

Because an entry is a text file, writing one by hand is a perfectly good way to post:
add `entries/2026-09-01-whatever.txt` in the GitHub web editor and it is on the shelf.

---

## Reading it

- **Tap a scroll** — it lifts off the shelf and unrolls, as far as the words go and no
  further. It opens large enough to read without doing anything else, and the text can
  be selected, copied, and found with the browser's own search.
- **Unread scrolls nudge gently.** Reading is remembered only in that browser. The
  animation stops as soon as the scroll is opened and is disabled when reduced motion
  is requested.
- **Phones fit more scrolls per shelf.** The closed scrolls, shelf spacing, dates, and
  feathers scale down below 640px; opened entries remain full reading size.
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
| A file is in `entries/` but no scroll appears | It doesn't end in `.txt`. Only text files become scrolls now. |
| Five taps do nothing | Try again a little faster — all five need to land inside two and a half seconds. |
| It asks for the token again | The browser's storage was cleared, or you're in a private window. Paste it in again. |
| Publish says `Resource not accessible` | The token lacks **Contents: Read and write**, or wasn't scoped to `PulpOfMan`. |
| Publish says `Bad credentials` | The token expired or was pasted with a stray space. Tap *forget this device* and set it up again. |
| Scrolls appear but are blank | The repo is private. Make it public. |
| Everything is in the wrong font | `assets/fonts/` didn't get uploaded. |
| An entry is wrong | Edit it on the scroll itself, or edit `entries/<name>.txt` directly on GitHub. It's a plain text file; the scroll follows it. |

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

Change `seed=7` in `cobblestone()` for a different wall. `social.py` re-renders the
share card and home-screen icons.

Layout knobs are in the `:root` block at the top of `index.html`:

| variable | what it does |
|---|---|
| `--rowH` | vertical space one shelf occupies |
| `--base` | gap under a scroll's foot: slab front plus its shadow |
| `--sink` | how far onto the slab's top surface the scrolls stand |
| `--ink` | the colour of the date written on each roll |

There are exactly as many shelves as it takes to hold the scrolls — one more appears
when a row fills up. Two more knobs sit in the script: `textSize()` sets how big the
writing is (smaller on a desktop so more fits, larger on a phone), and the
`Math.min(760, vw * 0.92)` in `openScroll` sets how wide a scroll opens.

---

## Files

```
index.html            the whole site, including the hidden door
CNAME                 pulpofman.com
site.webmanifest      name and icons for Add to Home Screen
entries/              your entries: one .txt per scroll
archive-scans/        the original PDFs from before the site went text-only
assets/               rendered wall, shelf, scrolls, rolls, paper, icons, share card
assets/fonts/         Cormorant Garamond, Caveat, Architects Daughter (OFL)
entries.json          last-ditch fallback listing; unused in normal operation
tools/                the Python that renders assets/, plus the old Drive relay
```
