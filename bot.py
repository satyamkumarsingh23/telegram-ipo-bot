import os
import asyncio
import logging
from datetime import datetime
import pytz
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from scraper import get_open_ipos  # Ensure scraper.py is correctly fetching IPO data

# Load environment variables
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and scheduler
bot = Bot(token=TOKEN)
scheduler = AsyncIOScheduler()

# Nepal timezone
nepal_tz = pytz.timezone("Asia/Kathmandu")

async def send_alert():
    """Fetch open IPOs and send an alert if any are available."""
    open_ipos = get_open_ipos()  # Get currently open IPOs
    if not open_ipos:
        logging.info("No open IPOs to alert.")
        return

    message = "📢 *Open IPO/FPO Alerts:*\n\n"
    for ipo in open_ipos:
        message += f"🏢 *Company:* {ipo['company']}\n📅 *Opening Date:* {ipo['open_date']}\n📅 *Closing Date:* {ipo['close_date']}\n⚡ *Status:* {ipo['status']}\n\n"

    # Send message
    await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")
    logging.info("✅ Alert sent successfully!")

# Schedule job to run at 10 AM Nepal Time daily
scheduler.add_job(send_alert, "cron", hour=10, minute=0, timezone=nepal_tz)

async def main():
    """Start the scheduler and keep the script running."""
    scheduler.start()
    while True:
        await asyncio.sleep(3600)  # Prevent script from exiting

if __name__ == "__main__":
    asyncio.run(main())
