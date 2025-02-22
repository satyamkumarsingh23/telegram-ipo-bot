import telegram
import schedule
import time
from datetime import datetime
from config import BOT_TOKEN, CHAT_ID
from scraper import get_offering_data  # Updated function name

bot = telegram.Bot(token=BOT_TOKEN)

def send_offering_alert():
    offering_list = get_offering_data()  # Fetch IPO & FPO data
    today = datetime.today().strftime('%Y-%m-%d')

    messages = []
    for name, offering_type, open_date, close_date in offering_list:
        if open_date <= today <= close_date:  # Check if offering is open
            messages.append(f"📢 {offering_type} Open: {name}\n📅 Open Date: {open_date}\n📅 Close Date: {close_date}")

    if messages:
        bot.send_message(chat_id=CHAT_ID, text="\n\n".join(messages))

# Schedule to run at 11 AM every day
schedule.every().day.at("11:00").do(send_offering_alert)

print("Bot is running...")
while True:
    schedule.run_pending()
    time.sleep(30)  # Check every 30 seconds
