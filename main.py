import streamlit as st
import pandas as pd
from database import init_db, add_product, get_products, add_price_log, get_price_history
from scraper import get_amazon_price
from notifier import send_telegram_alert
import time

# Initialize Database on startup
init_db()

st.title("🕵️ Deal Hunter Bot")
st.write("Track prices and get notified on Telegram!")

# --- Sidebar: Add New Product ---
st.sidebar.header("Add New Product")
with st.sidebar.form("new_product"):
    name = st.text_input("Product Name (e.g., MacBook M1)")
    url = st.text_input("Amazon URL")
    target = st.number_input("Target Price (₹)", min_value=1.0)
    submitted = st.form_submit_button("Start Tracking")
    
    if submitted:
        if url and target:
            add_product(name, url, target)
            st.sidebar.success(f"Tracking {name}!")
            # Send a test notification
            send_telegram_alert(f"Started tracking {name} at target ₹{target}")
        else:
            st.sidebar.error("Please fill all fields.")

# --- Main Area: Dashboard ---
st.subheader("Your Tracking List")
products = get_products() # Returns list of tuples: (id, name, url, target)

if products:
    for prod in products:
        p_id, p_name, p_url, p_target = prod
        
        with st.expander(f"{p_name} (Target: ₹{p_target})"):
            col1, col2 = st.columns(2)
            
            with col1:
                # Button to check price manually right now
                if st.button(f"Check Price Now", key=f"btn_{p_id}"):
                    current_price = get_amazon_price(p_url)
                    if current_price:
                        add_price_log(p_id, current_price)
                        st.metric("Current Price", f"₹{current_price}", delta=f"₹{p_target - current_price}")
                        
                        if current_price <= p_target:
                            st.success("Target Price Met! Alert Sent.")
                            send_telegram_alert(f"🚨 DEAL ALERT! {p_name} is now ₹{current_price}!")
                    else:
                        st.error("Could not fetch price. Amazon might be blocking bots.")
            
            with col2:
                # Show Price History Graph
                history = get_price_history(p_id)
                if history:
                    df = pd.DataFrame(history, columns=["Time", "Price"])
                    st.line_chart(df.set_index("Time"))
                else:
                    st.info("No price history yet.")
                    
            st.write(f"[View on Amazon]({p_url})")

else:
    st.info("No products tracked yet. Add one from the sidebar!")