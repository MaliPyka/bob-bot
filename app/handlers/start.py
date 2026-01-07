from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext


from app.db import queries as db_queries
from app.db.queries import get_player_stats, add_user, get_baobab_size, get_top_baobab_size
from app.keyboards.inline import menu_kb, create_kb, back_kb, profile_kb
from app.keyboards.reply import start_menu, get_game_keyboard


# Класс состояний
class UserSettings(StatesGroup):
    waiting_for_nickname = State()


router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    # Сбрасываем любые зависшие состояния при перезапуске
    await state.clear()
    await message.answer(
        "Приветствую! \nДля получения информации и управления ботом вызовите команду: /menu",
        reply_markup=get_game_keyboard()
    )

@router.message(Command("menu"))
async def menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("📖", reply_markup=menu_kb())


@router.callback_query(F.data == "info")
async def info(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "ℹ️ О боте:\n📌 Версия: 0.1\n👤 Автор: не пидорас\n⚙️ Статус: кто прочитал тот лох",
        reply_markup=back_kb()
    )


@router.callback_query(F.data == "back")
async def back(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await callback.message.edit_text("📖", reply_markup=menu_kb())


@router.callback_query(F.data == "profile")
async def profile(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id

    # Получаем глобальную статистику игрока
    user = await get_player_stats(user_id)

    if user is None:
        await callback.message.edit_text(
            "❌ У тебя нет профиля. Нажми 'Создать профиль' в меню.",
            reply_markup=create_kb()
        )
        return

    # Получаем размер дерева конкретно в этом чате
    current_chat_size = await get_baobab_size(user_id, chat_id)

    nickname = user["nickname"] or "—"
    name = callback.from_user.first_name

    text = (
        f"👤 <b>Профиль</b>\n\n"
        f"📛 <b>Имя:</b> <a href=\"tg://user?id={user_id}\">{name}</a>\n"
        f"🏷 <b>Ник:</b> {nickname}\n\n"
        f"🔥 <b>Текущая серия:</b> {user['cur_streak']} дн.\n"
        f"🏆 <b>Рекорд серии:</b> {user['max_streak']} дн.\n"
        f"📈 <b>Всего поливов:</b> {user['total_grows']}\n\n"
        f"🌳 <b>Баобаб в этом чате:</b> {current_chat_size} см"
    )
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=profile_kb())


@router.callback_query(F.data == "top")
async def top(callback: CallbackQuery):
    await callback.answer()
    top_list = await get_top_baobab_size(callback.message.chat.id)

    if not top_list:
        await callback.message.answer("🌳 Пока никто не посадил баобаб!")
        return

    text = "🏆 <b>Топ:</b>\n\n"

    for i, user_data in enumerate(top_list, 1):
        nickname = user_data[0]
        size = user_data[1]
        user_id = user_data[2]

        text += f"{i}) <a href=\"tg://user?id={user_id}\">{nickname}</a> — <b>{size} см</b>\n"

    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=back_kb())


@router.callback_query(F.data == "create")
async def create(callback: CallbackQuery):
    await callback.answer()

    await add_user(callback.from_user.id, callback.from_user.first_name)
    await callback.message.edit_text(
        "✅ Профиль создан!",
        reply_markup=back_kb()
    )


@router.callback_query(F.data == "nick")
async def start_nick_change(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text("📥 Введи новый никнейм:")
    await state.set_state(UserSettings.waiting_for_nickname)


@router.message(UserSettings.waiting_for_nickname)
async def save_nickname(message: Message, state: FSMContext):
    new_nick = message.text.strip()


    if len(new_nick) < 3 or len(new_nick) > 15:
        await message.answer("❌ Ник должен быть от 3 до 15 символов!")
        return

    if len(new_nick.split()) > 1:
        await message.answer("❌ Ник должен состоять из одного слова!")
        return

    # Сохраняем в БД
    await db_queries.set_nick(message.from_user.id, new_nick)

    await message.answer(f"✅ Ник успешно изменен на: <b>{new_nick}</b>", parse_mode="HTML",reply_markup=back_kb())
    await state.clear()
