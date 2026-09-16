# payments.py
import uuid
import requests
from config import YOOKASSA_SHOP_ID, YOOKASSA_SECRET_KEY

YOOKASSA_API_URL = "https://api.yookassa.ru/v3/payments"


def create_payment(amount: float, description: str, user_id: int) -> dict:
    """Создаёт платёж в ЮKassa"""
    if not YOOKASSA_SHOP_ID or not YOOKASSA_SECRET_KEY:
        return {"error": "ЮKassa не настроена"}

    idempotence_key = str(uuid.uuid4())
    headers = {
        "Content-Type": "application/json",
        "Idempotence-Key": idempotence_key,
    }

    # Аутентификация через basic auth
    auth = (YOOKASSA_SHOP_ID, YOOKASSA_SECRET_KEY)

    data = {
        "amount": {
            "value": f"{amount:.2f}",
            "currency": "RUB"
        },
        "capture": True,
        "confirmation": {
            "type": "redirect",
            "return_url": "https://t.me/Evrat_First_Tele_bot"
        },
        "description": description,
        "metadata": {
            "user_id": str(user_id)
        }
    }

    try:
        response = requests.post(
            YOOKASSA_API_URL,
            headers=headers,
            auth=auth,
            json=data,
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Ошибка ЮKassa: {response.status_code} {response.text}")
            return {"error": f"Ошибка {response.status_code}"}
    except requests.exceptions.RequestException as e:
        print(f"Сетевая ошибка: {e}")
        return {"error": "Сетевая ошибка"}


def check_payment_status(payment_id: str) -> str:
    """Проверяет статус платежа"""
    if not YOOKASSA_SHOP_ID or not YOOKASSA_SECRET_KEY:
        return "error"

    headers = {"Content-Type": "application/json"}
    auth = (YOOKASSA_SHOP_ID, YOOKASSA_SECRET_KEY)

    try:
        response = requests.get(
            f"{YOOKASSA_API_URL}/{payment_id}",
            headers=headers,
            auth=auth,
            timeout=30
        )
        if response.status_code == 200:
            return response.json().get("status", "unknown")
        else:
            print(f"Ошибка проверки платежа: {response.status_code} {response.text}")
            return "error"
    except requests.exceptions.RequestException as e:
        print(f"Сетевая ошибка: {e}")
        return "error"
