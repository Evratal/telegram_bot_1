from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "Вот что я умею:\n\n"
        "/start — начать работу\n"
        "/help — эта справка\n"
        "/about — о владельце\n"
        "/services — услуги вайбкодинга\n"
        "/projects — портфолио и проекты\n"
        "/contact — связаться с владельцем\n\n"
        "Или просто напишите свой вопрос — я постараюсь помочь!"
    )
