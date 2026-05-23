from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

gender_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Male"),
            KeyboardButton(text="Female")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)