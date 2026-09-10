import sqlite3
from datetime import datetime
from typing import Optional, List, Dict

DB_PATH = "shop.db"


def init_db():
    """Создаёт таблицы в базе данных"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Таблица пользователей
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Таблица корзины
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            item_name TEXT,
            price REAL,
            quantity INTEGER DEFAULT 1,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    """)

    # Таблица заказов (обновлённая с payment_id)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            items TEXT,
            total_price REAL,
            status TEXT DEFAULT 'pending',
            payment_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    """)

    conn.commit()
    conn.close()


def add_user(user_id: int, username: str = None, first_name: str = None):
    """Добавляет пользователя в базу"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO users (user_id, username, first_name) VALUES (?, ?, ?)",
        (user_id, username, first_name)
    )
    conn.commit()
    conn.close()


def get_cart(user_id: int) -> List[Dict]:
    """Возвращает корзину пользователя"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT item_name, price, quantity FROM cart WHERE user_id = ?",
        (user_id,)
    )
    items = [
        {"name": row[0], "price": row[1], "quantity": row[2]}
        for row in cursor.fetchall()
    ]
    conn.close()
    return items


def add_to_cart(user_id: int, item_name: str, price: float):
    """Добавляет товар в корзину"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Проверяем, есть ли уже такой товар в корзине
    cursor.execute(
        "SELECT id, quantity FROM cart WHERE user_id = ? AND item_name = ?",
        (user_id, item_name)
    )
    result = cursor.fetchone()

    if result:
        # Увеличиваем количество
        cursor.execute(
            "UPDATE cart SET quantity = quantity + 1 WHERE id = ?",
            (result[0],)
        )
    else:
        # Добавляем новый товар
        cursor.execute(
            "INSERT INTO cart (user_id, item_name, price) VALUES (?, ?, ?)",
            (user_id, item_name, price)
        )

    conn.commit()
    conn.close()


def clear_cart(user_id: int):
    """Очищает корзину пользователя"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()


def add_order(user_id: int, items: str, total_price: float, payment_id: str = None):
    """Создаёт заказ в базе данных"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO orders (user_id, items, total_price, payment_id) VALUES (?, ?, ?, ?)",
        (user_id, items, total_price, payment_id)
    )
    order_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return order_id


def update_order_status(payment_id: str, status: str):
    """Обновляет статус заказа по payment_id"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE orders SET status = ? WHERE payment_id = ?",
        (status, payment_id)
    )
    conn.commit()
    conn.close()


def get_orders_by_user(user_id: int) -> List[Dict]:
    """Возвращает все заказы пользователя"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, items, total_price, status, created_at FROM orders WHERE user_id = ? ORDER BY created_at DESC",
        (user_id,)
    )
    orders = [
        {"id": row[0], "items": row[1], "total_price": row[2], "status": row[3], "created_at": row[4]}
        for row in cursor.fetchall()
    ]
    conn.close()
    return orders
