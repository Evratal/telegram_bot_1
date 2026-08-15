from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("services"))
async def cmd_services(message: Message):
    await message.answer(
        "🚀 Мои услуги вайбкодинга:\n\n"
        "1. **Лендинг под ключ** — от 3 дней\n"
        "   • Продающий текст\n"
        "   • Адаптивный дизайн\n"
        "   • Подключение аналитики\n\n"
        "2. **MVP для стартапа** — от 2 недель\n"
        "   • Быстрый запуск продукта\n"
        "   • Проверка гипотез\n"
        "   • Итеративное развитие\n\n"
        "3. **AI-автоматизация бизнеса** — от 5 дней\n"
        "   • Чат-боты\n"
        "   • Обработка заявок\n"
        "   • Автоматические отчёты\n\n"
        "4. **UI/UX дизайн** — от 2 дней\n"
        "   • Прототипы\n"
        "   • Дизайн-системы\n"
        "   • Адаптация под платформы\n\n"
        "Хотите узнать подробнее? Напишите мне!"
    )
