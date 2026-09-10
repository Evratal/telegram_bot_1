from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text == "📞 Связаться с человеком")
async def contact_from_menu(message: Message):
    """Обработчик кнопки 'Связаться с человеком' из меню"""
    await message.answer(
        "📬 Связаться со мной:\n\n"
        "• **Telegram:** @Evrat_First_Tele_bot\n"
        "• **Email:** ваш_email@example.com\n"
        "• **Время работы:** Пн-Сб, 10:00–19:00 МСК\n\n"
        "Напишите мне — отвечу в течение часа!"
    )

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
