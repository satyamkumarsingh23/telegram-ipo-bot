import logging
import os
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Set up logging
logging.basicConfig(level=logging.INFO)

# Paths for Chrome and Chromedriver
CHROME_PATH = "/usr/bin/google-chrome-stable"
CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"

def install_chrome():
    """Install Google Chrome and Chromedriver if not already installed."""
    logging.info("🚀 Installing Google Chrome and Chromedriver...")

    try:
        subprocess.run(
            "apt update && apt install -y wget unzip curl && "
            "wget -q -O google-chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && "
            "dpkg -i google-chrome.deb || apt install -fy && rm google-chrome.deb && "
            "wget -q -O chromedriver.zip https://chromedriver.storage.googleapis.com/$(wget -qO- https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip && "
            "unzip chromedriver.zip -d /usr/local/bin/ && chmod +x /usr/local/bin/chromedriver && rm chromedriver.zip",
            shell=True,
            check=True
        )
        logging.info("✅ Chrome and Chromedriver installed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Chrome installation failed: {e}")
        return False

    return True

def get_open_ipos():
    """Scrapes open IPO/FPO data and filters only 'Ordinary' share types."""
    
    # Ensure Chrome is installed before proceeding
    if not install_chrome():
        return []

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Set correct Chrome binary path
    options.binary_location = CHROME_PATH

    # Use the installed Chromedriver
    service = Service(CHROMEDRIVER_PATH)  

    driver = webdriver.Chrome(service=service, options=options)

    try:
        url = "https://nepalipaisa.com/ipo"
        driver.get(url)

        # Wait until the table is loaded (max wait: 10 seconds)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "tbody"))
        )

        # Extract page source after JavaScript execution
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Locate the IPO/FPO table
        table = soup.find("tbody")
        if not table:
            logging.error("❌ No IPO table found.")
            return []

        ipo_data = []
        rows = table.find_all("tr")

        for row in rows:
            columns = row.find_all("td")
            if len(columns) < 7:
                continue  # Skip incomplete rows

            company = columns[0].text.strip()
            share_type = columns[1].text.strip()
            open_date = columns[3].find("abbr")["title"] if columns[3].find("abbr") else "N/A"
            close_date = columns[4].find("abbr")["title"] if columns[4].find("abbr") else "N/A"
            status = columns[6].text.strip()

            # Filter only 'Ordinary' share types and open status
            if share_type == "Ordinary" and status == "Open":
                ipo_data.append({
                    "company": company,
                    "share_type": share_type,
                    "open_date": open_date,
                    "close_date": close_date,
                    "status": status
                })

        logging.info(f"✅ {len(ipo_data)} Open IPOs Found.")
        return ipo_data

    except Exception as e:
        logging.error(f"❌ Error while scraping IPOs: {e}")
        return []

    finally:
        driver.quit()  # Close the browser
