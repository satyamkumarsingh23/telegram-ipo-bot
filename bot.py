from dotenv import load_dotenv
load_dotenv()
import os
import time
import pytz
import chromedriver_autoinstaller
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def get_open_ordinary_ipos():
    chromedriver_autoinstaller.install()

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    driver.get("https://nepalipaisa.com/ipo")
    time.sleep(5)

    rows = driver.find_elements("css selector", "#tblIpo tbody tr")
    ordinary_open_ipos = []

    for row in rows:
        cols = row.find_elements("tag name", "td")
        if len(cols) < 8:
            continue

        share_type = cols[1].text.strip().lower()
        status = cols[6].text.strip().lower()

        if share_type == "ordinary" and status == "open":
            ipo = {
                "company_name": cols[0].text.strip(),
                "opening_date": cols[3].find_element("tag name", "abbr").get_attribute("title"),
                "closing_date": cols[4].find_element("tag name", "abbr").get_attribute("title"),
            }

            

            ordinary_open_ipos.append(ipo)

    driver.quit()
    return ordinary_open_ipos

def send_ipo_alert():
    ipos = get_open_ordinary_ipos()
    if not ipos:
        return

    bot = Bot(token=BOT_TOKEN)
    for ipo in ipos:
        message = (
            f"📢 *Open IPO Alert*\n"
            f"🏢 Company: {ipo['company_name']}\n"
            f"🗓️ Open: {ipo['opening_date']}\n"
            f"🗓️ Close: {ipo['closing_date']}\n"
        )
     
        bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")

if __name__ == "__main__":
    send_ipo_alert()
