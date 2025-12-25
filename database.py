import sqlite3
from datetime import datetime

DB_NAME = "tracker.db"

def init_db():
    """Creates the database tables if they don't exist."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Table for storing product details
    c.execute('''CREATE TABLE IF NOT EXISTS products 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  name TEXT, 
                  url TEXT, 
                  target_price REAL)''')
    
    # Table for storing price history (for the graph)
    c.execute('''CREATE TABLE IF NOT EXISTS prices 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  product_id INTEGER, 
                  price REAL, 
                  timestamp DATETIME,
                  FOREIGN KEY(product_id) REFERENCES products(id))''')
    conn.commit()
    conn.close()

def add_product(name, url, target_price):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO products (name, url, target_price) VALUES (?, ?, ?)", 
              (name, url, target_price))
    conn.commit()
    conn.close()

def get_products():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    return c.fetchall()

def add_price_log(product_id, price):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO prices (product_id, price, timestamp) VALUES (?, ?, ?)", 
              (product_id, price, datetime.now()))
    conn.commit()
    conn.close()

def get_price_history(product_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT timestamp, price FROM prices WHERE product_id = ?", (product_id,))
    return c.fetchall()