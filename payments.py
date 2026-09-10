# payments.py
import uuid
import requests
from config import YOOKASSA_SHOP_ID, YOOKASSA_SECRET_KEY

YOOKASSA_API_URL = "https://api.yookassa.ru/v3/payments"


def create_payment(amount: float, description: str, user_id: int) -> dict:
    """Создаёт платёж в ЮKassa"""
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
            "return_url": "https://t.me/your_bot"  # замените на вашего бота
        },
        "description": description,
        "metadata": {
            "user_id": str(user_id)
        }
    }

    response = requests.post(
        YOOKASSA_API_URL,
        headers=headers,
        auth=auth,
        json=data
    )

    return response.json()


def check_payment_status(payment_id: str) -> str:
    """Проверяет статус платежа"""
    headers = {"Content-Type": "application/json"}
    auth = (YOOKASSA_SHOP_ID, YOOKASSA_SECRET_KEY)

    response = requests.get(
        f"{YOOKASSA_API_URL}/{payment_id}",
        headers=headers,
        auth=auth
    )

    data = response.json()
    return data.get("status", "unknown")
