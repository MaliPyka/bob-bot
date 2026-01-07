from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from app.db.queries import get_baobab_size, get_top_baobab_size, get_last_grow_date, update_grow_stats, add_user, get_player_stats

from datetime import datetime
import random


game_router = Router()

@game_router.message(Command("size"))
async def size_cmd(message: Message):
    size = await get_baobab_size(message.from_user.id, message.chat.id)
    await message.answer(f"📊 Высота твоего баобаба 🌴: ️{size} см")


@game_router.message(Command("top"))
async def top_cmd(message: Message):
    top_list = await get_top_baobab_size(message.chat.id)

    if not top_list:
        await message.answer("🌳 Пока никто не посадил баобаб!")
        return

    text = "🏆 <b>Топ:</b>\n\n"

    for i, user_data in enumerate(top_list, 1):
        nickname = user_data[0]
        size = user_data[1]
        user_id = user_data[2]

        text += f"{i}) <a href=\"tg://user?id={user_id}\">{nickname}</a> — <b>{size} см</b>\n"

    await message.answer(text, parse_mode="HTML")


@game_router.message(Command("grow"))
async def grow_cmd(message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    last_date = await get_last_grow_date(user_id, chat_id)

    today = datetime.now().strftime("%Y-%m-%d")
    if last_date == today:
        await message.answer("🌱 Жди завтра.")
        return

    growth = random.randint(1, 10)
    new_size = await update_grow_stats(user_id, chat_id, growth)

    await message.answer(
        f"📈 Твой баобаб вырос на <b>{growth} см</b>!\n"
        f"🌳 Теперь его высота: <b>{new_size} см</b>."
    )





