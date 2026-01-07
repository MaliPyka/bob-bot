from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


button_info = InlineKeyboardButton(text="ℹ️ info", callback_data="info")
button_profile = InlineKeyboardButton(text="👤 profile", callback_data="profile")
button_back = InlineKeyboardButton(text="⬅️ back", callback_data="back")

def menu_kb():
    button_info = InlineKeyboardButton(
        text="ℹ️ Инфа",
        callback_data="info"
    )
    button_profile = InlineKeyboardButton(
        text="👤 Профиль",
        callback_data="profile"
    )
    button_top = InlineKeyboardButton(
        text="🏆 Топ",
        callback_data="top"
    )

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [button_info, button_top],
            [button_profile]
        ]
    )

def back_kb() -> InlineKeyboardMarkup:
    button_back = InlineKeyboardButton(
        text="⬅️ back",
        callback_data="back"
    )
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [button_back]
        ]
    )

def create_kb() -> InlineKeyboardMarkup:
    button_creat = InlineKeyboardButton(
        text="✚ Cоздать профиль",
        callback_data="create"
    )

    button_back = InlineKeyboardButton(
        text="⬅️ back",
        callback_data="back"
    )

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [button_creat],[button_back]
        ]
    )

def profile_kb() -> InlineKeyboardMarkup:
    button_profile = InlineKeyboardButton(text="✍🏼 Изменить ник", callback_data="nick")
    button_back = InlineKeyboardButton(
        text="⬅️ back",
        callback_data="back"
    )

    return InlineKeyboardMarkup(
        inline_keyboard=[[button_profile],[button_back]]
    )


