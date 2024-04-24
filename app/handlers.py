import os
from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types.web_app_info import WebAppInfo
import requests

from app.botscripts import findMatchId, newUser, setAccountId, lastMatches
from match_processing import match_full_processing_async
from dotenv import load_dotenv

load_dotenv()
steam_api_key= os.getenv('STEAMAPIKEY')

router = Router()

@router.message(Command('start','Start'))
async def start(message: Message):
    newUser(message.chat.id)
    await message.answer('Я работаю.')

@router.message(Command('commands','Commands'))
async def start(message: Message):
    first = '1: "Матч + {id матча}" - запрос обработать матч.'
    second = '2: "Последние матчи" - запрос обработать последние 25 матчей.'
    third = '3: "Мой id + {id профиля в доте}" - запрос на установку id'
    await message.answer(f"""{first}\n{second}\n{third}""")

@router.message(F.text)
async def start(message: Message):
    if("последние матчи" in message.text.lower()):
        test = await message.reply("Обрабатываю.")
        answer = await lastMatches(message.chat.id)
        await test.edit_text(answer) 
    elif("матч" in message.text.lower()):
        match_id = findMatchId(message.text.split())
        test = await message.reply("Обрабатываю.")
        answer = await match_full_processing_async(match_id)
        markup = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text='Показать.',web_app=WebAppInfo(url='https://ya.ru'))]
        ])
        await test.edit_text(answer,reply_markup=markup)
    elif("мой id" in message.text.lower()):
        newUser(message.chat.id)
        account_id = findMatchId(message.text.split())
        req = requests.get(url=f'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v1/?account_id={account_id}&key={steam_api_key}').json()
        if(req['result']['status'] == 1):
            await message.reply(setAccountId(message.chat.id,account_id))
        else:
            await message.reply("Некорректный ID. Попробуйте еще раз.")
        