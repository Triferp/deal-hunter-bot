import schedule
import time
from database import get_products, add_price_log, get_price_history
from scraper import get_amazon_price
from notifier import send_telegram_alert

def check_prices():
    print("  Waking up to check prices...")
    
    products = get_products()
    
    if not products:
        print("   No products to check.")
        return

    for prod in products:
        p_id, p_name, p_url, p_target = prod
        
        # --- RETRY LOGIC ---
        current_price = None
        for attempt in range(1, 4): # Try 3 times
            current_price = get_amazon_price(p_url)
            if current_price:
                break # Success! Stop retrying
            print(f"     Attempt {attempt} failed for {p_name}. Retrying in 5s...")
            time.sleep(5)
        # ----------------------------------------
        
        if current_price:
            print(f"     Checked {p_name}: ₹{current_price}")
            
            # Get the PREVIOUS price from history
            history = get_price_history(p_id)
            
            if history:
                previous_price = history[-1][1] 
            else:
                previous_price = float('inf') 
            
            # Log the NEW price to database
            add_price_log(p_id, current_price)
            
            # Smart Alert Logic
            is_deal = current_price <= p_target
            was_expensive = previous_price > p_target
            
            if is_deal and was_expensive:
                print(f"     NEW DEAL! Sending alert...")
                alert_msg = f"  DEAL ALERT! {p_name} dropped to ₹{current_price}!"
                send_telegram_alert(alert_msg)
            elif is_deal and not was_expensive:
                print(f"     {p_name} is still cheap (no new alert sent).")
                
        else:
            print(f"     FAILED to fetch {p_name} after 3 attempts. Skipping.")
            
    print("  Check finished. Sleeping...")

# --- THE SCHEDULE ---

# Run every 4 hours (Safe for Amazon, useful for project)
schedule.every(4).hours.do(check_prices)

# FOR TESTING ONLY: Uncomment the next line to test it every 30 seconds
# schedule.every(30).seconds.do(check_prices)

print("--- Smart Price Scheduler Started ---")
print("I will check prices every 4 hours (with retries).")
print("Press Ctrl+C to stop.")

# Run once immediately when script starts
check_prices()

while True:
    schedule.run_pending()
    time.sleep(1)