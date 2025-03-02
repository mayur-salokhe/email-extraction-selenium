import re
import time
import csv
import logging
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Logging Configuration
logging.basicConfig(
    filename="email_scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# User-Agent Rotation List
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
]

# Proxy Configuration (Set your proxy here)
USE_PROXY = False  # Set to True to enable proxy
PROXY = "172.10.164.178:29559"  # Replace with actual proxy


def extract_emails(text):
    """Extract emails using regex."""
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    return set(re.findall(email_pattern, text))


def get_contact_page(driver, base_url):
    """Find and return the contact page URL if it exists."""
    try:
        links = driver.find_elements(By.TAG_NAME, "a")
        for link in links:
            href = link.get_attribute("href")
            if href and "/contact" in href.lower():
                return href
    except Exception as e:
        logging.error(f"Error finding contact page on {base_url}: {e}")
    return None


def get_emails_from_site(url):
    """Scrape emails from a website including its contact page."""
    options = Options()
    options.headless = True  # Run browser in visible mode for debugging
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")
    # options.add_argument("window-size=1920x1080")
    options.add_argument("--headless=new")


    # Add Proxy if enabled
    if USE_PROXY:
        options.add_argument(f"--proxy-server={PROXY}")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    emails = set()
    try:
        logging.info(f"Scraping website: {url}")
        driver.get(url)
        time.sleep(3)  # Allow the page to load

        # Extract emails from homepage
        emails.update(extract_emails(driver.page_source))
        emails.update(extract_emails(driver.find_element(By.TAG_NAME, "body").text))

        # Look for contact page and scrape emails from there
        contact_page = get_contact_page(driver, url)
        if contact_page:
            logging.info(f"Found contact page: {contact_page}")
            driver.get(contact_page)
            time.sleep(3)
            emails.update(extract_emails(driver.page_source))
            emails.update(extract_emails(driver.find_element(By.TAG_NAME, "body").text))

        logging.info(f"Found {len(emails)} emails on {url} (including contact page)")
        return emails

    except Exception as e:
        logging.error(f"Error scraping {url}: {e}")
        return set()

    finally:
        driver.quit()


def save_emails_to_csv(email_dict, filename="emails_raw.csv"):
    """Save emails to a CSV file."""
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Website", "Email"])
        for site, emails in email_dict.items():
            for email in emails:
                writer.writerow([site, email])

    logging.info(f"Emails saved to {filename}")


# List of non-relevant email prefixes to filter out
IGNORE_EMAILS = {"support@", "info@", "noreply@", "contact@", "admin@", "webmaster@"}


def filter_emails(input_file="emails_raw.csv", output_file="emails_filtered.csv"):
    """Filter out non-relevant emails and save to a new CSV file."""
    filtered_emails = []

    with open(input_file, mode="r", newline="") as infile:
        reader = csv.reader(infile)
        header = next(reader)  # Read the header
        for row in reader:
            site, email = row
            if not any(email.lower().startswith(prefix) for prefix in IGNORE_EMAILS):
                filtered_emails.append([site, email])

    # Save filtered emails
    with open(output_file, mode="w", newline="") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["Website", "Email"])
        writer.writerows(filtered_emails)

    logging.info(f"Filtered emails saved to {output_file}")


def read_websites_from_csv(filename="websites.csv"):
    """Read websites from a CSV file."""
    websites = []
    try:
        with open(filename, mode="r", newline="") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if row:  # Ignore empty rows
                    websites.append(row[0].strip())
    except Exception as e:
        logging.error(f"Error reading {filename}: {e}")
    
    return websites


if __name__ == "__main__":
    websites = read_websites_from_csv()

    if not websites:
        logging.info("No websites found in CSV file. Exiting.")
    else:
        all_emails = {}

        for site in websites:
            emails = get_emails_from_site(site)
            if emails:
                all_emails[site] = emails

        if all_emails:
            save_emails_to_csv(all_emails)
            filter_emails()
        else:
            logging.info("No emails found on any site.")
