from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

country_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🇮🇳 India"),
            KeyboardButton(text="🇺🇸 America")
        ],
        [
            KeyboardButton(text="🇬🇧 UK"),
            KeyboardButton(text="🌍 Earth")
        ]
    ],
    resize_keyboard=True
)