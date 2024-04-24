import os
import requests
from orm import session_factory
from models import TelegramUserORM
from match_processing import match_full_processing_async
from dotenv import load_dotenv

load_dotenv()
steam_api_key= os.getenv('STEAMAPIKEY')


def findMatchId(message_text):
    answer = 'Вы не указали id матча.'
    for word in message_text:
        if word.isdigit():
            answer = word
    return answer

def setAccountId(chat_id,account_id):
    with session_factory() as session:
        user = session.get(TelegramUserORM,chat_id)
        if(user.account_id == account_id):
            return "Этот id и так установлен"
        else:
            user.account_id = account_id
            session.commit()
            return "id обновлен"
            
def newUser(chat_id):
    with session_factory() as session:
        if(not session.get(TelegramUserORM,chat_id)):
            session.add(TelegramUserORM(chat_id=chat_id))
            session.commit()

async def lastMatches(chat_id):
    ans = [0,0,0,0]
    with session_factory() as session:
        chat = session.get(TelegramUserORM,chat_id)
        if(chat):
            req = requests.get(url=f'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v1/?account_id={chat.account_id}&key={steam_api_key}').json()
            for match in req['result']['matches']:
                res = await match_full_processing_async(match['match_id'])
                ans = resToAns(res,ans)
            return f'Есть-{ans[0]},Обнов-{ans[1]},Добав-{ans[2]},Ошиб-{ans[3]}'


def resToAns(res,ans):
    match(res):
        case 'Этот матч уже есть в базе.':
            ans[0] += 1
        case 'Этот матч уже есть базе, но не все данные были записаны. Прошло больше 7 дней ({days}) со старта матча. Ссылка на реплей удалена. Нельзя получить расширенные данные.':
            ans[0] += 1
        case 'Этот матч уже в базе данных, но не все данные были записаны. Не удалось получить ссылку на запись, попробуйте еще раз позже.':
            ans[0] += 1
        case 'Этот матч уже есть в базе, данные обновлены."':
            ans[1] += 1
        case 'Матч обработан.':
            ans[2] += 1
        case 'Матч обработан, но не все данные были записаны.':
            ans[2] += 1
        case 'Неизвестная ошибка.':
            ans[3] += 1
    return ans
        