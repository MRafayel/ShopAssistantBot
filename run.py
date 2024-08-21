import asyncio
import sys
import logging

from aiogram import Dispatcher
from Bot.handlers import router, bot
from DB.database import create_db


async def main():
    create_db()
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("[INFO] Exit")