from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from ai_helper import client, SYSTEM_PROMPT
from keyboards import contact_kb

router = Router()

# Память диалога (последние 20 сообщений)
conversation_history = {}


@router.message(Command("contact"))
async def contact_handler(message: Message):
    await message.answer(
        "📞 Связаться с человеком:\n\n"
        "Телеграм: @vibecoder_portfolio\n"
        "Почта: vibecoder@example.com",
        reply_markup=contact_kb
    )


@router.message()
async def handle_text(message: Message):
    # Если нажали кнопку "Связаться с человеком"
    if message.text == "📞 Связаться с человеком":
        await message.answer(
            "📞 Связаться с человеком:\n\n"
            "Телеграм: @vibecoder_portfolio\n"
            "Почта: vibecoder@example.com"
        )
        return

    # Обрабатываем обычные команды
    text = message.text.lower()

    if any(word in text for word in ["привет", "здравствуй", "добрый день", "hello", "hi"]):
        await message.answer(
            "Здравствуйте! 👋\n\n"
            "Я бот-консультант по вайбкодингу. Расскажу о своих услугах, помогу выбрать подходящий вариант.\n\n"
            "Вот что я могу:\n"
            "/services — мои услуги\n"
            "/projects — мои проекты\n"
            "/about — обо мне\n"
            "/contact — связаться со мной",
            reply_markup=contact_kb
        )
        return

    # Отправляем вопрос в DeepSeek
    user_id = message.from_user.id

    # Инициализируем историю для пользователя
    if user_id not in conversation_history:
        conversation_history[user_id] = []

    # Добавляем сообщение пользователя в историю
    conversation_history[user_id].append({"role": "user", "content": message.text})

    # Ограничиваем историю последними 20 сообщениями
    conversation_history[user_id] = conversation_history[user_id][-20:]

    # Формируем сообщения для DeepSeek
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(conversation_history[user_id])

    try:
        response = await client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            temperature=0.7
        )

        bot_reply = response.choices[0].message.content

        # Добавляем ответ бота в историю
        conversation_history[user_id].append({"role": "assistant", "content": bot_reply})
        conversation_history[user_id] = conversation_history[user_id][-20:]

        await message.answer(bot_reply, reply_markup=contact_kb)
    except Exception as e:
        await message.answer(
            "Извините, произошла ошибка. Попробуйте позже или свяжитесь с человеком: @vibecoder_portfolio",
            reply_markup=contact_kb
        )
