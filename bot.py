import os
import asyncio
import logging
from datetime import datetime
import pytz
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from scraper import get_open_ipos  # Ensure scraper.py fetches IPO data correctly

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Validate TOKEN and CHAT_ID
if not TOKEN:
    raise ValueError("❌ TOKEN is missing! Make sure it is set in the .env file.")
if not CHAT_ID:
    raise ValueError("❌ CHAT_ID is missing! Make sure it is set in the .env file.")

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and scheduler
bot = Bot(token=TOKEN)
scheduler = AsyncIOScheduler()

# Nepal timezone
nepal_tz = pytz.timezone("Asia/Kathmandu")

async def send_alert():
    """Fetch open IPOs of type 'Ordinary' and send an alert."""
    open_ipos = get_open_ipos()  # Get currently open IPOs
    ordinary_ipos = [ipo for ipo in open_ipos if ipo.get("share_type") == "Ordinary"]


    if not ordinary_ipos:
        logging.info("No 'Ordinary' IPOs open today. Skipping alert.")
        return

    message = "📢 *Open IPO/FPO Alerts:*\n\n"
    for ipo in ordinary_ipos:
        message += f"🏢 *Company:* {ipo['company']}\n📅 *Opening Date:* {ipo['open_date']}\n📅 *Closing Date:* {ipo['close_date']}\n⚡ *Status:* {ipo['status']}\n\n"

    # Send message
    await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")
    logging.info("✅ Alert sent successfully!")

# Schedule job to run at 10 AM Nepal Time daily
scheduler.add_job(send_alert, "cron", hour=13, minute=31, timezone=nepal_tz)

async def main():
    """Start the scheduler and keep the script running."""
    scheduler.start()
    while True:
        await asyncio.sleep(3600)  # Prevent script from exiting

if __name__ == "__main__":
    asyncio.run(main())
