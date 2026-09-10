from .menu import main_menu_kb
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Клавиатура с кнопкой "Связаться с человеком"
contact_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📞 Связаться с человеком")]
    ],
    resize_keyboard=True
)
