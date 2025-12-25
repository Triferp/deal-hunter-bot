# Deal Hunter Bot

A full-stack Python web application that tracks product prices on Amazon and notifies users via Telegram when their target price is met.

## Features
- **Real-time Scraping:** Fetches live pricing data from Amazon using `requests` and `BeautifulSoup`.
- **Data Persistence:** Stores product history and targets in a local `SQLite` database.
- **Interactive Dashboard:** Built with `Streamlit` to visualize price trends and manage tracking links.
- **Mobile Alerts:** Integrated with `Telegram Bot API` for instant push notifications on price drops.

## Tech Stack
- **Language:** Python 3.9+
- **Frontend:** Streamlit
- **Database:** SQLite
- **Libraries:** Pandas, BeautifulSoup4, APScheduler, Python-Telegram-Bot

## Installation
1. Clone the repo
git clone [https://github.com/Triferp/deal-hunter-bot.git](https://github.com/Triferp/deal-hunter-bot.git)

2. Install dependencies
pip install -r requirements.txt

3. Set up environment variables Create a .env file and add your Telegram credentials:
TELEGRAM_TOKEN = your_token_here 
TELEGRAM_CHAT_ID = your_chat_id

4. Run the App
streamlit run main.py