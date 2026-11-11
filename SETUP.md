# Greenlight Permits & Takeoffs: setup

The site is hosted for free on **GitHub Pages**. Its two forms, *Upload your plans* and *Contact us*, send to a **Google Apps Script** in your own Google account. Each request:

- adds a row to a private Google Sheet (**Greenlight - Requests**)
- saves uploaded plans in Google Drive (**Greenlight - Client Plans**)
- sends a notification to your Gmail

Your phone number and email do not appear anywhere on the website or in the GitHub repository.

## 1. Google: set up the form backend (about 5 minutes)

1. Go to **sheets.new** to create a Google Sheet, and name it **Greenlight - Requests**.
2. In the Sheet, open **Extensions → Apps Script**.
3. Delete everything in `Code.gs`, paste in the contents of `google-apps-script/Code.gs`, and click **Save**.
4. In the function dropdown at the top, select **setup** and click **Run**. Google will ask you to authorize it. Choose your account, then **Advanced → Go to project (unsafe) → Allow**. Google shows this warning for any script you write yourself. The script only touches this Sheet, one Drive folder, and sends email to you.
5. Click **Deploy → New deployment → gear icon → Web app**.
   - Execute as: **Me**
   - Who has access: **Anyone**
   - Click **Deploy** and copy the **Web app URL** (it ends in `/exec`).
6. Open that URL in a browser. You should see `{"ok":true,"service":"greenlight-forms"}`.

## 2. Connect the site to Google

In `index.html`, find this line:

```js
const FORM_ENDPOINT = 'PASTE_YOUR_APPS_SCRIPT_URL_HERE';
```

Replace the placeholder with your `/exec` URL and commit. GitHub Pages updates within a minute or two.

## 3. Test

Open the live site, send a test request with a small PDF, and check that:

- a row appears in the Sheet
- a folder with the PDF appears in Drive
- an email arrives in your inbox

## Changing prices

All prices are in one block at the top of the script in `index.html`, marked `PRICES: edit these numbers`. The sources for the current prices are listed in the comment above that block.

## If you change Code.gs later

Use **Deploy → Manage deployments → Edit (pencil) → Version: New version → Deploy**. This keeps the same URL. If you choose *New deployment* instead, you get a new URL and have to paste it into `index.html` again.
