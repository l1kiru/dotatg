import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
import logging

from botscripts import findMatchId
from match_processing import match_full_processing

bot = Bot('123')
dp = Dispatcher()

@dp.message(Command('start'))
async def start(message: Message):
    await message.answer('Я работаю.')

@dp.message(F.text == 'ты кто?')
async def start(message: Message):
    await message.answer('Я бот.')

@dp.message(F.text)
async def start(message: Message):
    if("матч" in message.text.lower()):
        match_id = findMatchId(message.text.split())
        print(f"Поступил запрос на match_id: {match_id}")
        await message.reply("Обрабатываю.")
        answer = await match_full_processing(match_id)
        await message.answer(answer)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Выходим.')