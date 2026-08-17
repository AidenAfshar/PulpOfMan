/**
 * A PULP OF MAN — Google Drive relay
 * ────────────────────────────────────────────────────────────────────────────
 * A static web page can't hold a Google password, so this little script stands
 * between the two. It lists the image files in one Drive folder and hands the
 * site back a plain JSON list. Nothing else. It cannot write, delete or read
 * anything outside the folder you name below.
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

const FOLDER_ID = 'PASTE-YOUR-FOLDER-ID-HERE';

function doGet() {
  const cache = CacheService.getScriptCache();
  const cached = cache.get('pulp-list');
  if (cached) return reply(cached);

  let body;
  try {
    const folder = DriveApp.getFolderById(FOLDER_ID);
    const it = folder.getFiles();
    const entries = [];
    while (it.hasNext()) {
      const f = it.next();
      if (f.getMimeType().indexOf('image/') !== 0) continue;   // skip anything not a picture
      entries.push({
        id: f.getId(),
        name: f.getName(),
        created: f.getDateCreated().toISOString()
      });
    }
    body = JSON.stringify({ ok: true, count: entries.length, entries: entries });
    cache.put('pulp-list', body, 60);          // be kind to the quota; 60s is plenty
  } catch (err) {
    body = JSON.stringify({ ok: false, error: String(err) });
  }
  return reply(body);
}

function reply(body) {
  return ContentService.createTextOutput(body)
    .setMimeType(ContentService.MimeType.JSON);
}

/**
 * Run this once from the editor (choose `test` in the function dropdown, press
 * Run) to check the folder ID before deploying. The result appears in the
 * Execution log: it should say ok:true and a sensible count.
 */
function test() {
  Logger.log(doGet().getContent());
}
