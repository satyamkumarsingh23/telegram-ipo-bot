from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import logging
import os
import shutil
import subprocess

# Set up logging
logging.basicConfig(level=logging.INFO)

def install_chrome():
    """Install Google Chrome and Chromedriver if not already installed."""
    if not shutil.which("google-chrome"):
        logging.info("🚀 Installing Google Chrome...")
        subprocess.run(
            "wget -q -O google-chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && apt update && apt install -y ./google-chrome.deb",
            shell=True,
            check=True
        )

    if not shutil.which("chromedriver"):
        logging.info("🚀 Installing ChromeDriver...")
        subprocess.run(
            "wget -q -O chromedriver.zip https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip && unzip chromedriver.zip -d /usr/local/bin/",
            shell=True,
            check=True
        )

# Install Chrome if needed
install_chrome()

def get_open_ipos():
    """Scrapes open IPO/FPO data and filters only 'Ordinary' share types."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/google-chrome"  # Set correct Chrome path

    service = Service("/usr/local/bin/chromedriver")  # Set correct Chromedriver path
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
        logging.error(f"❌ Error while scraping: {e}")
        return []

    finally:
        driver.quit()  # Close the browser
