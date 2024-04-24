import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from app.handlers import router
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('BOTTOKEN')

bot = Bot(token)
dp = Dispatcher()

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Выходим.')