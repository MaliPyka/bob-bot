import aiosqlite
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]   # .../baobab_bot/app
DB_PATH = BASE_DIR / "data" / "database.db"
print(f"DEBUG: База данных находится тут -> {DB_PATH}")


def get_db():
    return aiosqlite.connect(DB_PATH)

DB_PATH.parent.mkdir(parents=True, exist_ok=True)


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        # Глобальный профиль (только статистика и ник)
        await db.execute("""
                         CREATE TABLE IF NOT EXISTS players
                         (
                             user_id
                             INTEGER
                             PRIMARY
                             KEY,
                             name
                             TEXT,
                             nickname
                             TEXT,
                             cur_streak
                             INTEGER
                             DEFAULT
                             0,
                             max_streak
                             INTEGER
                             DEFAULT
                             0,
                             total_grows
                             INTEGER
                             DEFAULT
                             0
                             -- Дату отсюда убрали
                         )""")

        # Локальные деревья + дата полива именно В ЭТОМ чате
        await db.execute("""
                         CREATE TABLE IF NOT EXISTS baobabs
                         (
                             user_id
                             INTEGER,
                             chat_id
                             INTEGER,
                             baobab_size
                             INTEGER
                             DEFAULT
                             0,
                             max_size
                             INTEGER
                             DEFAULT
                             0,
                             last_grow_date
                             TEXT, -- Дату перенесли сюда
                             PRIMARY
                             KEY
                         (
                             user_id,
                             chat_id
                         )
                             )""")
        await db.commit()
