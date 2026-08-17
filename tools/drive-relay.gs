/**
 * A PULP OF MAN — Google Drive relay
 * ────────────────────────────────────────────────────────────────────────────
 * A static web page can't hold a Google password, so this little script stands
 * between the two. It does exactly two things:
 *
 *    /exec              → lists the photographs and PDFs in one Drive folder
 *    /exec?file=FILE_ID → hands back one PDF, so the site can draw its pages
 *
 * It cannot write, cannot delete, and refuses to serve any file that isn't
 * inside the folder you name below — so a stray file ID gets you nothing.
 *
 * SETUP — about ten clicks, once
 *
 *  1. Open the Drive folder your handwriting photos live in. The address bar
 *     reads .../folders/1a2B3c4D5e6F7g8H — that tail is the folder ID.
 *
 *  2. Go to script.google.com → New project. Delete whatever is in the editor
 *     and paste this whole file in. Name the project "Pulp Of Man".
 *
 *  3. Put your folder ID in the line just below.
 *
 *  4. Deploy ▸ New deployment ▸ (gear) Web app.
 *        Execute as:      Me
 *        Who has access:  Anyone            ← must be "Anyone", not "Anyone with a Google account"
 *     Deploy. Google will ask you to authorise it; the "unverified app" warning
 *     is expected for your own scripts — Advanced ▸ Go to Pulp Of Man (unsafe).
 *
 *  5. Copy the Web app URL. It ends in /exec. Paste it into index.html as
 *     SOURCE.drive.
 *
 *  6. In Drive, share the folder: Anyone with the link ▸ Viewer. The browser
 *     needs that to actually display the photographs.
 *
 * IF YOU EVER EDIT THIS FILE: changes don't go live until you deploy again —
 * Deploy ▸ Manage deployments ▸ (pencil) ▸ Version: New version ▸ Deploy.
 * Editing and forgetting to redeploy is the usual reason nothing changes.
 */

const FOLDER_ID = '1d_As0zvsNq__SeGWA-Ml7C3dMispg7vt';

/** Biggest PDF we'll hand over. Apps Script has its own ceiling; this one is
 *  friendlier, and a scanned page well under this is plenty. */
const MAX_PDF_MB = 12;

function doGet(e) {
  const id = e && e.parameter && e.parameter.file;
  return id ? sendFile(id) : sendList();
}

// ── the listing ────────────────────────────────────────────────────────────
function sendList() {
  const cache = CacheService.getScriptCache();
  const cached = cache.get('pulp-list');
  if (cached) return reply(cached);

  let body;
  try {
    const it = DriveApp.getFolderById(FOLDER_ID).getFiles();
    const entries = [];
    while (it.hasNext()) {
      const f = it.next();
      const mime = f.getMimeType();
      const isImage = mime.indexOf('image/') === 0;
      const isPdf = mime === 'application/pdf';
      if (!isImage && !isPdf) continue;              // ignore everything else
      entries.push({
        id: f.getId(),
        name: f.getName(),
        kind: isPdf ? 'pdf' : 'image',
        created: f.getDateCreated().toISOString()
      });
    }
    body = JSON.stringify({ ok: true, count: entries.length, entries: entries });
    cache.put('pulp-list', body, 60);        // be kind to the quota; 60s is plenty
  } catch (err) {
    body = JSON.stringify({ ok: false, error: String(err) });
  }
  return reply(body);
}

// ── one PDF, as base64 ─────────────────────────────────────────────────────
function sendFile(id) {
  try {
    const file = DriveApp.getFileById(id);

    // The guard: only ever serve something that lives in YOUR folder.
    if (!isInFolder(file)) {
      return reply(JSON.stringify({ ok: false, error: 'Not in the folder.' }));
    }
    if (file.getMimeType() !== 'application/pdf') {
      return reply(JSON.stringify({ ok: false, error: 'Not a PDF.' }));
    }

    const bytes = file.getBlob().getBytes();
    const mb = bytes.length / 1048576;
    if (mb > MAX_PDF_MB) {
      return reply(JSON.stringify({
        ok: false,
        error: 'Too large: ' + mb.toFixed(1) + ' MB. Scan at a lower resolution.'
      }));
    }
    return reply(JSON.stringify({
      ok: true, name: file.getName(), b64: Utilities.base64Encode(bytes)
    }));
  } catch (err) {
    return reply(JSON.stringify({ ok: false, error: String(err) }));
  }
}

function isInFolder(file) {
  const parents = file.getParents();
  while (parents.hasNext()) {
    if (parents.next().getId() === FOLDER_ID) return true;
  }
  return false;
}

function reply(body) {
  return ContentService.createTextOutput(body)
    .setMimeType(ContentService.MimeType.JSON);
}

/**
 * Run this once from the editor (choose `test` in the function dropdown, press
 * Run) to check the folder ID before deploying. The Execution log should show
 * ok:true and a sensible count.
 */
function test() {
  Logger.log(sendList().getContent().slice(0, 800));
}
