import time
import pytz
import json
import schedule
from datetime import datetime
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from telegram import Bot

chromedriver_autoinstaller.install()

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)
# Replace with your actual values
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def get_open_ordinary_ipos():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
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
                "share_type": cols[1].text.strip(),
                "opening_date": cols[3].find_element("tag name", "abbr").get_attribute("title"),
                "closing_date": cols[4].find_element("tag name", "abbr").get_attribute("title"),
                "document_link": None
            }

            link = cols[7].find_elements("tag name", "a")
            if link:
                ipo["document_link"] = link[0].get_attribute("href")

            ordinary_open_ipos.append(ipo)

    driver.quit()
    return ordinary_open_ipos

def send_ipo_alert():
    bot = Bot(token=BOT_TOKEN)
    ipos = get_open_ordinary_ipos()

    if not ipos:
        return  # ❌ No ordinary open IPOs — stay silent

    for ipo in ipos:
        message = (
            f"📢 *Open IPO Alert*\n"
            f"🏢 Company: {ipo['company_name']}\n"
            f"📄 Type: {ipo['share_type']}\n"
            f"🗓️ Open: {ipo['opening_date']}\n"
            f"🗓️ Close: {ipo['closing_date']}\n"
        )
        if ipo['document_link']:
            message += f"🔗 [View Document]({ipo['document_link']})"

        bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")

# Run daily at 10:00 AM Nepal Time
def run_daily_check():
    npt = pytz.timezone("Asia/Kathmandu")

    def job():
        now = datetime.now(npt)
        if now.hour == 10 and now.minute == 0:
            send_ipo_alert()

    schedule.every().minute.do(job)

    while True:
        schedule.run_pending()
        time.sleep(30)

if __name__ == "__main__":
    run_daily_check()
