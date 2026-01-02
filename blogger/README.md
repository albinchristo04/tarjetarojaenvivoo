# Blogger Setup Guide for Tarjeta Roja En Vivo

This folder contains the necessary files to replicate the Tarjeta Roja design on Blogger and automate match posting.

## 1. Theme Setup

1.  Go to your Blogger Dashboard.
2.  Navigate to **Theme**.
3.  Click on the arrow next to "Customize" and select **Edit HTML**.
4.  **Backup** your current theme if necessary.
5.  Copy the entire content of `theme.xml` from this folder.
6.  Paste it into the Blogger HTML editor, replacing everything.
7.  Click **Save**.

### Mobile Settings
1.  In the **Theme** section, click the arrow next to "Customize".
2.  Select **Mobile Settings**.
3.  Choose **Desktop** (since our theme is responsive and handles mobile view itself).
4.  Save.

## 2. Auto-Posting Script Setup

To automatically post matches, you need to set up the Google Blogger API.

### A. Google Cloud Console
1.  Go to [Google Cloud Console](https://console.cloud.google.com/).
2.  Create a **New Project**.
3.  Search for **"Blogger API v3"** and **Enable** it.
4.  Go to **Credentials** -> **Create Credentials** -> **OAuth client ID**.
5.  Choose **Desktop App**.
6.  Download the JSON file and rename it to `client_secrets.json`.
7.  Place `client_secrets.json` inside this `blogger/` folder.

### B. Configure Script
1.  Open `autopost.py`.
2.  Find the line: `BLOG_ID = "YOUR_BLOG_ID_HERE"`
3.  Replace `"YOUR_BLOG_ID_HERE"` with your actual Blog ID (found in the URL of your Blogger dashboard, e.g., `.../blogID=123456789`).

### C. Install Dependencies
Open a terminal in this `blogger` folder and run:
```bash
pip install -r requirements.txt
```

### D. Run the Script
```bash
python autopost.py
```
*   On the first run, a browser window will open asking you to log in to your Google account and authorize the app.
*   Once authorized, it will create a `token.pickle` file for future runs.
*   The script will fetch matches and create posts on your Blogger site.

## 3. Domain Setup

You mentioned the domain: `https://rojadirecta.evaulthub.com/`

1.  Go to **Blogger Settings** -> **Publishing** -> **Custom Domain**.
2.  Enter `rojadirecta.evaulthub.com`.
3.  Blogger will provide CNAME records.
4.  Go to your DNS provider (where you manage `evaulthub.com`) and add the CNAME records provided by Blogger.
5.  Enable **HTTPS Availability** in Blogger Settings after the domain is verified.

## 4. Maintenance

*   Run `python autopost.py` periodically (e.g., every hour) to keep the schedule updated.
*   You can automate this using Windows Task Scheduler or a cron job if you move to a server.

## 5. GitHub Actions Automation (Optional)

## 5. GitHub Actions Automation

The workflow is set to run every 6 hours.

**IMPORTANT:** For this to work without secrets, you must commit your credential files to the repository.

1.  **Generate `token.pickle` locally**:
    *   Run `python autopost.py` on your machine once.
    *   Authenticate in the browser.
    *   This creates a `token.pickle` file.

2.  **Commit Files**:
    *   Ensure both `client_secrets.json` and `token.pickle` are in the `blogger/` folder.
    *   Commit and push them to GitHub.

The workflow will simply use these files to authenticate and post matches.


