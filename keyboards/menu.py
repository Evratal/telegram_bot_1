from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Главное меню с постоянными кнопками
main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛍️ Витрина")],
        [KeyboardButton(text="🛒 Корзина")],
        [KeyboardButton(text="📞 Связаться с человеком")]
    ],
    resize_keyboard=True,
    is_persistent=True  # делаем меню постоянным
)
