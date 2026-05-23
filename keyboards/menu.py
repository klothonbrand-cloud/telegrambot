from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="💬 Chat"),
            KeyboardButton(text="⚙️ Settings")
        ],
        [
            KeyboardButton(text="❓ Help"),
            KeyboardButton(text="ℹ️ About")
        ]
    ],
    resize_keyboard=True
)