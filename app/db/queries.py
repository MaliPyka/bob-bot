from datetime import datetime, timedelta
import aiosqlite
from app.db.database import get_db


# 1. Регистрация теперь идет в players (глобально)
async def add_user(user_id: int, name: str):
    async with get_db() as db:
        await db.execute(
            "INSERT OR IGNORE INTO players (user_id, name) VALUES (?, ?)",
            (user_id, name)
        )
        await db.commit()


# 2. Получение глобальной статистики для профиля
async def get_player_stats(user_id: int):
    async with get_db() as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM players WHERE user_id = ?", (user_id,))
        return await cursor.fetchone()


# 3. Получение размера конкретного баобаба в конкретном чате
async def get_baobab_size(user_id: int, chat_id: int):
    async with get_db() as db:
        cursor = await db.execute(
            "SELECT baobab_size FROM baobabs WHERE user_id = ? AND chat_id = ?",
            (user_id, chat_id)
        )
        row = await cursor.fetchone()
        return row[0] if row else 0


# 4. Установка ника (теперь в глобальной таблице)
async def set_nick(user_id: int, nickname: str | None):
    async with get_db() as db:
        await db.execute(
            "UPDATE players SET nickname = ? WHERE user_id = ?",
            (nickname, user_id)
        )
        await db.commit()

# Получение имени для отображения (Ник или Имя из ТГ)
async def get_display_name(user_id: int):
    async with get_db() as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT name, nickname FROM players WHERE user_id = ?",
            (user_id,)
        )
        row = await cursor.fetchone()
        if row:
            return row["nickname"] if row["nickname"] else row["name"]
        return "-"


# 6. Топ именно для ЭТОГО чата (используем JOIN, чтобы достать имена из глобальной таблицы)
async def get_top_baobab_size(chat_id: int):
    async with get_db() as db:
        cursor = await db.execute("""
                                  SELECT COALESCE(p.nickname, p.name), b.baobab_size, p.user_id
                                  FROM baobabs b
                                           JOIN players p ON b.user_id = p.user_id
                                  WHERE b.chat_id = ?
                                  ORDER BY b.baobab_size DESC LIMIT 10
                                  """, (chat_id,))
        return await cursor.fetchall()


# 7. Глобальная проверка даты (полил ли он дерево ХОТЬ ГДЕ-ТО сегодня)
async def get_last_grow_date(user_id: int, chat_id: int):
    async with get_db() as db:
        cursor = await db.execute(
            "SELECT last_grow_date FROM baobabs WHERE user_id = ? AND chat_id = ?",
            (user_id, chat_id)
        )
        row = await cursor.fetchone()
        return row[0] if row else None


# 8. Главная функция обновления
async def update_grow_stats(user_id: int, chat_id: int, growth: int):
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    async with get_db() as db:
        db.row_factory = aiosqlite.Row

        # 1. Берем глобальные статы для стрика
        cursor = await db.execute("SELECT * FROM players WHERE user_id = ?", (user_id,))
        player = await cursor.fetchone()

        # 2. Берем локальные статы для размера и даты
        cursor = await db.execute("SELECT * FROM baobabs WHERE user_id = ? AND chat_id = ?", (user_id, chat_id))
        baobab = await cursor.fetchone()

        last_date_any = player["last_grow_date"] if (player and "last_grow_date" in player.keys()) else None
        # (Если хочешь стрик тоже по чатам - пиши, переделаем)

        current_size = (baobab["baobab_size"] if baobab else 0) + growth

        # ОБНОВЛЯЕМ ГЛОБАЛЬНО (статистика)
        await db.execute("""
                         INSERT INTO players (user_id, total_grows)
                         VALUES (?, 1) ON CONFLICT(user_id) DO
                         UPDATE SET
                             total_grows = total_grows + 1
                         """, (user_id,))

        # ОБНОВЛЯЕМ ЛОКАЛЬНО (размер и дата конкретного чата)
        await db.execute("""
                         INSERT INTO baobabs (user_id, chat_id, baobab_size, last_grow_date)
                         VALUES (?, ?, ?, ?) ON CONFLICT(user_id, chat_id) DO
                         UPDATE SET
                             baobab_size = ?,
                             last_grow_date = ?
                         """, (user_id, chat_id, current_size, today, current_size, today))

        await db.commit()
    return current_size