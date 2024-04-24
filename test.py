import json
from orm import session_factory
from models import MatchORM

def get_item(ability):
    with open("dota/ability_ids.json") as file_:
        data = json.load(file_)
    ability = data[f'{id}']
    with open("dota/abilities.json") as file_:
        data = json.load(file_)
    return data[f'{ability}']


#with session_factory() as session:
#    match_ = session.get(MatchORM,7698921185)
#    player = match_.players[5]
#    for item in player.mp_lvlup.ability_upgrades_arr:
#        print(get_item(item)['dname'])



import os
from dotenv import load_dotenv

load_dotenv()
host = os.getenv('HOST')
user = os.getenv('USERDB')
password = os.getenv('PASSWORD')
db_name = os.getenv('DB_NAME')
port = os.getenv('PORT')


print(user)