import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
YOOKASSA_SHOP_ID = os.getenv("YOOKASSA_SHOP_ID")
YOOKASSA_SECRET_KEY = os.getenv("YOOKASSA_SECRET_KEY")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env файле!")

if not YOOKASSA_SHOP_ID or not YOOKASSA_SECRET_KEY:
    print("⚠️ ЮKassa ключи не найдены. Оплата будет недоступна.")
