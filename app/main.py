import asyncio
import logging

from app.config import load_config
from app.bot.setup import create_bot, create_dispatcher
from app.db.database import init_db

async def main():
    logging.basicConfig(level=logging.INFO)

    config = load_config()
    bot = create_bot(config.bot_token)
    dp = create_dispatcher()

    await init_db()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())