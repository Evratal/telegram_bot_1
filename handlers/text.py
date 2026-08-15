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
            "/contact — связаться со мной"
        )
    elif any(word in text for word in ["цена", "стоимость", "сколько стоит"]):
        await message.answer(
            "💰 Стоимость услуг:\n\n"
            "• Лендинг — от 15 000 ₽\n"
            "• MVP — от 50 000 ₽\n"
            "• AI-автоматизация — от 20 000 ₽\n"
            "• UI/UX дизайн — от 10 000 ₽\n\n"
            "Точную цену назову после обсуждения деталей. "
            "Напишите, что вас интересует!"
        )
    else:
        await message.answer(
            "Не совсем понял вас 😅\n\n"
            "Попробуйте использовать команды:\n"
            "/services — услуги\n"
            "/projects — портфолио\n"
            "/about — обо мне\n"
            "/contact — связаться\n"
            "/help — помощь"
        )
