import requests
from bs4 import BeautifulSoup
import random

# User Agents to avoid detection (Amazon thinks we are a browser)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]

def get_amazon_price(url):
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9",
    }
    
    try:
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")
        
        # Logic to find price on Amazon (Classes change often, this is the most common one)
        price_whole = soup.find("span", {"class": "a-price-whole"})
        
        if price_whole:
            # Cleanup: Remove commas and convert to float (e.g., "50,000" -> 50000.0)
            return float(price_whole.get_text().replace(",", "").replace(".", ""))
        else:
            return None
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None