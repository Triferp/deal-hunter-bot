import requests
import os
from dotenv import load_dotenv

# Load secrets from .env file
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_alert(message):
    """Sends a message to your Telegram app."""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        requests.post(url, json=payload)
        print("Message sent to Telegram!")
    except Exception as e:
        print(f"Failed to send alert: {e}")