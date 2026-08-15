from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("contact"))
async def cmd_contact(message: Message):
    await message.answer(
        "📬 Связаться со мной:\n\n"
        "• **Telegram:** @Evrat_First_Tele_bot\n"
        "• **Email:** ваш_email@example.com\n"
        "• **Время работы:** Пн-Сб, 10:00–19:00 МСК\n\n"
        "Напишите мне — отвечу в течение часа!"
    )
