import telegram
import schedule
import time
from datetime import datetime
from config import BOT_TOKEN, CHAT_ID
from scraper import get_ipo_data

bot = telegram.Bot(token=BOT_TOKEN)

def send_ipo_alert():
    ipo_list = get_ipo_data()
    today = datetime.today().strftime('%Y-%m-%d')

    messages = []
    for name, open_date, close_date in ipo_list:
        if open_date <= today <= close_date:  # Check if IPO is open
            messages.append(f"📢 IPO Open: {name}\n📅 Open Date: {open_date}\n📅 Close Date: {close_date}")

    if messages:
        bot.send_message(chat_id=CHAT_ID, text="\n\n".join(messages))

# Schedule to run at 11 AM every day
schedule.every().day.at("11:00").do(send_ipo_alert)

print("Bot is running...")
while True:
    schedule.run_pending()
    time.sleep(30)  # Check every 30 seconds
