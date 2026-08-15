from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("projects"))
async def cmd_projects(message: Message):
    await message.answer(
        "📂 Мои проекты:\n\n"
        "1. **Лендинг для кофейни** — 4 дня\n"
        "   • Увеличил заявки в 2 раза\n"
        "   • Продающий дизайн\n\n"
        "2. **MVP для доставки еды** — 3 недели\n"
        "   • Автоматизация заказов\n"
        "   • Интеграция с Telegram\n\n"
        "3. **AI-бот для поддержки клиентов** — 1 неделя\n"
        "   • Отвечает на 80% вопросов\n"
        "   • Работает 24/7\n\n"
        "4. **Интернет-магазин на Telegram** — 2 недели\n"
        "   • Приём заказов\n"
        "   • Оплата через Telegram\n\n"
        "Хотите узнать подробнее? Напишите мне!"
    )
