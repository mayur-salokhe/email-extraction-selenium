# Email Scraper using Selenium

This Python script scrapes emails from a list of websites, including their `/contact` pages, and saves them to a CSV file. It also filters out common non-relevant emails (e.g., `support@`, `info@`, `noreply@`).

---

## Features 🚀
- Extracts emails from the **homepage** and **contact page** (if available).
- **Avoids bot detection** using custom browser settings.
- Saves **all extracted emails** in `emails_raw.csv`.
- **Filters out non-relevant emails** (`support@`, `info@`, etc.) and saves the final result in `emails_filtered.csv`.
- Uses **logging** for tracking progress and errors.

---

## Prerequisites 📌
### Install Required Dependencies
Ensure you have Python installed (version 3.7+ recommended). Then, install dependencies:
```bash
pip install selenium pandas webdriver-manager
```

---

## Usage 📖
1. **Prepare Input File**:
    Place the list of websites in a CSV file at 'websites.csv'.

    The file should have one column without a header containing website URLs.
2. **Run the script**:
   ```bash
   python email_extraction.py
   ```
3. The script will:
   - Scrape emails from each website and its contact page.
   - Save all emails to `emails_raw.csv`.
   - Filter out non-relevant emails and save the final list to `emails_filtered.csv`.

---

## Output 📂
The script generates two files:
1. **`emails_raw.csv`** → Contains all extracted emails.
2. **`emails_filtered.csv`** → Contains only relevant emails (after filtering out common ones like `info@`).

### Example Output
**`emails_raw.csv` (Before filtering)**:
```
Website, Email
https://example.com, support@example.com
https://example.com, jhonny.depp@example.com
https://example.com/contact, contact@example.com
```

**`emails_filtered.csv` (After filtering)**:
```
Website, Email
https://example.com, jhonny.depp@example.com
```

---

## Logging 📜
The script logs all actions and errors in `email_scraper.log` for debugging purposes.

---
## Configuration

- User-Agent Rotation:

- Defined in the USER_AGENTS list to prevent detection.

- Proxy Support:

- Set USE_PROXY = True and define PROXY to enable proxy usage.

- Ignored Emails:

- Modify IGNORE_EMAILS to filter additional email prefixes.

## Customization 🎯
- **Modify the `IGNORE_EMAILS` set** in the script to filter additional unwanted email prefixes.
- **Adjust `time.sleep()` values** if pages take longer to load.
- **Expand the `websites` list** to scrape more sites.

---

## Troubleshooting 🛠️
### Common Issues & Fixes
1. **ChromeDriver Issues**:
   - Ensure you have **Google Chrome installed**.
   - If issues persist, update ChromeDriver:
     ```bash
     pip install --upgrade webdriver-manager
     ```

2. **No Emails Found**:
   - Increase `time.sleep()` to allow more time for pages to load.
   - Verify the website has visible email addresses.

3. **Bot Detection**:
   - Run the script **with a real Chrome window** (disable headless mode).
   - Use a **VPN or different IP** if getting blocked.

