/**
 * Greenlight Permits & Takeoffs - form backend (Google Apps Script)
 *
 * Receives the website's "Upload your plans" and "Contact us" forms.
 *  - Adds each request as a row in the Google Sheet this script is attached to
 *  - Saves uploaded plans into a Google Drive folder ("Greenlight - Client Plans")
 *  - Emails you a notification
 * Your email lives only here, inside your Google account. It never appears on the website.
 */

// ===== Settings =====
const NOTIFY_EMAIL = Session.getEffectiveUser().getEmail(); // emails the Google account that owns this script
const DRIVE_FOLDER_NAME = 'Greenlight - Client Plans';
const MAX_TOTAL_MB = 20;
// ====================

const COLUMNS = ['Received', 'Type', 'Service', 'Name', 'Company', 'Phone', 'Email', 'Job address',
  'License #', 'Needed by', 'Price shown', 'Notes', 'OK to text', 'Language', 'Plans folder', 'Status'];

function doPost(e) {
  try {
    const d = JSON.parse(e.postData.contents);
    if (d['bot-field']) return json_({ ok: true });                 // spam
    if (!d.name || !(d.email || d.phone)) return json_({ ok: false, error: 'missing fields' });

    const files = Array.isArray(d.files) ? d.files : [];
    const totalMb = files.reduce((a, f) => a + (f.data ? f.data.length * 0.75 : 0), 0) / 1048576;
    if (totalMb > MAX_TOTAL_MB) return json_({ ok: false, error: 'files too large' });

    // Save plans to Drive
    let folderUrl = '';
    if (files.length) {
      const root = getFolder_(DRIVE_FOLDER_NAME);
      const stamp = Utilities.formatDate(new Date(), 'America/New_York', 'yyyy-MM-dd HHmm');
      const sub = root.createFolder(`${stamp} - ${clean_(d.company || d.name)}`);
      files.forEach(f => {
        const blob = Utilities.newBlob(Utilities.base64Decode(f.data), f.type || 'application/octet-stream', clean_(f.name) || 'plan');
        sub.createFile(blob);
      });
      folderUrl = sub.getUrl();
    }

    // Log to the sheet
    const sh = getSheet_();
    const kind = d.kind === 'contact' ? 'Contact' : 'Quote request';
    sh.appendRow([new Date(), kind, d.service || '', d.name || '', d.company || '', d.phone || '', d.email || '',
      d.job_address || '', d.license || '', d.due || '', d.estimate || '', d.notes || '', d.sms_ok || '',
      d.language || '', folderUrl, 'New']);

    // Notify you
    const lines = [
      `New ${kind.toLowerCase()} from the website`, '',
      `Name: ${d.name || ''}`, `Company: ${d.company || ''}`, `Phone: ${d.phone || ''}`, `Email: ${d.email || ''}`,
      `Service: ${d.service || ''}`, `Price shown: ${d.estimate || ''}`, `Job address: ${d.job_address || ''}`,
      `License #: ${d.license || ''}`, `Needed by: ${d.due || ''}`, `OK to text: ${d.sms_ok || 'no'}`,
      `Language: ${d.language || ''}`, '', `Notes: ${d.notes || ''}`, '',
      folderUrl ? `Plans: ${folderUrl}` : 'No plans attached', `All requests: ${SpreadsheetApp.getActive().getUrl()}`
    ];
    MailApp.sendEmail({
      to: NOTIFY_EMAIL,
      subject: `Greenlight: ${kind} - ${d.name}${d.service ? ' (' + d.service + ')' : ''}`,
      body: lines.join('\n'),
      replyTo: d.email || NOTIFY_EMAIL
    });

    return json_({ ok: true });
  } catch (err) {
    console.error(err);
    return json_({ ok: false, error: String(err) });
  }
}

// Lets you open the /exec URL in a browser to confirm the deployment is live
function doGet() { return json_({ ok: true, service: 'greenlight-forms' }); }

// Run once from the editor to grant permissions and create the sheet header + Drive folder
function setup() {
  getSheet_();
  getFolder_(DRIVE_FOLDER_NAME);
  Logger.log('Ready. Notifications go to ' + NOTIFY_EMAIL);
}

function getSheet_() {
  const ss = SpreadsheetApp.getActive();
  let sh = ss.getSheetByName('Requests');
  if (!sh) {
    sh = ss.insertSheet('Requests');
    sh.appendRow(COLUMNS);
    sh.setFrozenRows(1);
    sh.getRange(1, 1, 1, COLUMNS.length).setFontWeight('bold').setBackground('#13201a').setFontColor('#ffffff');
  }
  return sh;
}
function getFolder_(name) {
  const it = DriveApp.getFoldersByName(name);
  return it.hasNext() ? it.next() : DriveApp.createFolder(name);
}
function clean_(s) { return String(s || '').replace(/[\\/:*?"<>|#%]/g, '').slice(0, 80).trim(); }
function json_(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }
