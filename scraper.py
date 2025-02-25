import time
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Path to Chromedriver
CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"

def install_chrome():
    """Installs Google Chrome and Chromedriver"""
    try:
        subprocess.run(
            "apt update && apt install -y wget unzip curl "
            "&& wget -q -O google-chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb "
            "&& dpkg -i google-chrome.deb || apt install -fy "
            "&& rm google-chrome.deb "
            "&& wget -q -O chromedriver.zip https://chromedriver.storage.googleapis.com/$(wget -qO- https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip "
            "&& unzip chromedriver.zip -d /usr/local/bin/ "
            "&& chmod +x /usr/local/bin/chromedriver "
            "&& rm chromedriver.zip",
            shell=True,
            check=True
        )
        print("✅ Google Chrome & Chromedriver installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Chrome installation failed: {e}")

def get_open_ipos():
    """Scrapes currently open IPOs from NepaliPaisa"""
    # Configure ChromeDriver
    service = Service(CHROMEDRIVER_PATH)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run Chrome in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    try:
        driver = webdriver.Chrome(service=service, options=options)
        driver.get("https://www.nepalipaisa.com/ipo/results")

        time.sleep(3)  # Wait for page to load

        ipos = []
        ipo_elements = driver.find_elements(By.CSS_SELECTOR, ".ipo-table tr")
        
        for row in ipo_elements[1:]:  # Skip header row
            cols = row.find_elements(By.TAG_NAME, "td")
            if cols and "Ordinary" in cols[2].text:  # Ensure it's an ordinary IPO
                ipo_name = cols[0].text.strip()
                status = cols[3].text.strip()
                if "Open" in status:
                    ipos.append(ipo_name)

        driver.quit()
        return ipos

    except Exception as e:
        print(f"❌ Error while scraping IPOs: {e}")
        return []

if __name__ == "__main__":
    install_chrome()
    print(get_open_ipos())
