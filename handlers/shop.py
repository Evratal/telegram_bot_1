from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from database import add_to_cart

router = Router()

# Каталог услуг (данные из portfolio.txt)
SERVICES = {
    "landing": {
        "name": "Лендинг под ключ",
        "description": "Одностраничный сайт с формой заявки",
        "price": 15000,
        "features": ["Продающий текст", "Адаптивный дизайн", "Срок: 5 дней"]
    },
    "bot": {
        "name": "Телеграм-бот",
        "description": "Консультант или продажник для вашего бизнеса",
        "price": 30000,
        "features": ["Бот-консультант или продажник", "Срок: 7–10 дней"]
    },
    "mvp": {
        "name": "MVP приложения",
        "description": "Прототип вашего приложения",
        "price": 50000,
        "features": ["Быстрый запуск продукта", "Срок: 14–20 дней"]
    },
    "ai": {
        "name": "AI-автоматизация",
        "description": "Подключение нейросетей к бизнес-процессам",
        "price": 20000,
        "features": ["Подключение нейросетей", "Срок зависит от задачи"]
    }
}


def format_price(price: int) -> str:
    """Форматирует цену с пробелами"""
    return f"{price:,}".replace(",", " ") + " ₽"


def create_service_card(service_key: str) -> tuple[str, InlineKeyboardMarkup]:
    """Создаёт карточку услуги и кнопку добавления в корзину"""
    service = SERVICES[service_key]

    text = (
        f"**{service['name']}**\n"
        f"_{service['description']}_\n\n"
    )

    # Добавляем характеристики
    for feature in service["features"]:
        text += f"• {feature}\n"

    text += f"\n💰 Цена: **{format_price(service['price'])}**"

    # Кнопка "Добавить в корзину"
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=f"🛒 Добавить в корзину",
                callback_data=f"add_{service_key}"
            )]
        ]
    )

    return text, kb


@router.message(F.text == "🛍️ Витрина")
async def show_shop(message: Message):
    """Показывает витрину услуг"""
    await message.answer("🛍️ **Наша витрина услуг:**\n\nВыберите услугу:")

    # Показываем карточки услуг по одной
    for service_key in SERVICES:
        text, kb = create_service_card(service_key)
        await message.answer(text, reply_markup=kb, parse_mode="Markdown")


@router.callback_query(F.data.startswith("add_"))
async def add_to_cart_callback(callback: CallbackQuery):
    """Обработчик добавления в корзину"""
    service_key = callback.data.replace("add_", "")
    service = SERVICES.get(service_key)

    if not service:
        await callback.answer("❌ Услуга не найдена", show_alert=True)
        return

    # Добавляем в корзину
    add_to_cart(
        user_id=callback.from_user.id,
        item_name=service["name"],
        price=service["price"]
    )

    # Отвечаем на callback
    await callback.answer(f"✅ {service['name']} добавлен в корзину!", show_alert=True)

    # Показываем кнопку "Корзина"
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🛒 Перейти в корзину", callback_data="show_cart")]
        ]
    )
    await callback.message.answer("Что дальше?", reply_markup=kb)
