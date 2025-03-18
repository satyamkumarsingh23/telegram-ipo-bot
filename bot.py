import os
import time
import asyncio
import logging
import requests
import subprocess
from apscheduler.schedulers.background import BackgroundScheduler
from scraper import scrape_and_send_alert  # Import your scraping function

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Telegram Bot Token and Chat ID
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Function to send a test message
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            logging.info("Test message sent successfully.")
        else:
            logging.error(f"Failed to send message: {response.text}")
    except Exception as e:
        logging.error(f"Error sending message: {str(e)}")

# Function to install Chrome and ChromeDriver
def install_chrome_and_driver():
    logging.info("Installing Chrome and ChromeDriver...")

    # Install Chrome
    subprocess.run("apt update", shell=True, check=True)
    subprocess.run("apt install -y wget unzip", shell=True, check=True)
    subprocess.run("wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb", shell=True, check=True)
    subprocess.run("apt install -y ./google-chrome-stable_current_amd64.deb", shell=True, check=True)

    # Install ChromeDriver
    subprocess.run("wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip", shell=True, check=True)
    subprocess.run("unzip chromedriver_linux64.zip", shell=True, check=True)
    subprocess.run("mv chromedriver /usr/bin/chromedriver", shell=True, check=True)
    subprocess.run("chmod +x /usr/bin/chromedriver", shell=True, check=True)

    logging.info("Chrome and ChromeDriver installed successfully.")

# Function to schedule the daily alert job
def schedule_alert():
    scheduler = BackgroundScheduler()
    scheduler.add_job(scrape_and_send_alert, "cron", hour=4, minute=15, timezone="Asia/Kathmandu")  # Runs at 10 AM NPT
    scheduler.start()
    logging.info("Scheduler started.")

# Main function
if __name__ == "__main__":
    install_chrome_and_driver()  # Install necessary dependencies
    send_telegram_message("🚀 Bot started successfully!")  # Send test message on startup
    schedule_alert()  # Schedule IPO/FPO alerts

    # Keep the bot running to prevent Railway from stopping it
    while True:
        time.sleep(60)
