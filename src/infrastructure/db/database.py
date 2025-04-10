import sqlite3
from datetime import date

DB_NAME = "orders.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        shop TEXT NOT NULL,
        date DATE NOT NULL,
        metadata TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        item TEXT NOT NULL,
        size REAL,
        quantity INTEGER NOT NULL,
        metadata TEXT,
        FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    conn.close()


def insert_order(order_data, items):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO orders (shop, date, metadata)
        VALUES (?, ?, ?)
    """, (order_data["shop"], order_data["date"], order_data.get("metadata", None)))

    order_id = cursor.lastrowid

    for item in items:
        cursor.execute("""
            INSERT INTO order_items (order_id, item, size, quantity, metadata)
            VALUES (?, ?, ?, ?, ?)
        """, (
            order_id,
            item["item"],
            item.get("size", None),
            item["quantity"],
            item.get("metadata", None)
        ))

    conn.commit()
    conn.close()


def get_orders_by_shop_and_date(shop, order_date):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT o.id, o.shop, o.date, i.item, i.size, i.quantity
        FROM orders o
        JOIN order_items i ON o.id = i.order_id
        WHERE o.shop = ? AND o.date = ?
    """, (shop, order_date))

    rows = cursor.fetchall()
    conn.close()
    return rows
