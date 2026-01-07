from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from app.keyboards.inline import menu_kb


start_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="/menu")]])

def get_game_keyboard() -> ReplyKeyboardMarkup:

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="/grow"),
                KeyboardButton(text="/top")
            ],
            [
                KeyboardButton(text="/menu")
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите команду..."
    )
    return keyboard


