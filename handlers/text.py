from aiogram import Router
from aiogram.types import Message

router = Router()

@router.message()
async def handle_text(message: Message):
    text = message.text.lower()

    if any(word in text for word in ["привет", "здравствуй", "добрый день", "hello", "hi"]):
        await message.answer(
            "Здравствуйте! 👋\n\n"
            "Я бот-консультант по вайбкодингу. Расскажу о своих услугах, помогу выбрать подходящий вариант.\n\n"
            "Вот что я могу:\n"
            "/services — мои услуги\n"
            "/projects — мои проекты\n"
            "/about — обо мне\n"
        )

        await message.answer()
