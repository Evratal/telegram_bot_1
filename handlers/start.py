from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я бот-консультант по услугам вайбкодинга 🚀\n\n"
        "Я помогу вам:\n"
        "• Создать лендинг под ключ\n"
        "• Разработать MVP вашего продукта\n"
        "• Автоматизировать бизнес с помощью AI\n"
        "• Улучшить UI/UX вашего сервиса\n\n"
        "Что вас интересует? Напишите мне, или используйте команды:\n"
        "/services — наши услуги\n"
        "/projects — портфолио\n"
        "/contact — связаться с владельцем\n"
        "/help — помощь"
    )
