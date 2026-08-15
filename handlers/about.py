from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("about"))
async def cmd_about(message: Message):
    await message.answer(
        "👨‍💻 О владельце:\n\n"
        "Я — специалист по вайбкодингу. Помогаю предпринимателям и стартапам "
        "быстро превращать идеи в работающие продукты.\n\n"
        "Моя специализация:\n"
        "• Лендинги и корпоративные сайты\n"
        "• MVP для стартапов\n"
        "• AI-автоматизация бизнеса\n"
        "• UI/UX дизайн\n\n"
        "Работаю с современными технологиями и AI-инструментами, "
        "чтобы создавать продукты быстро и качественно."
    )
