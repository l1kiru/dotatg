import os
import json
import requests
import time

from dbconfig import host, user, password, db_name, port
from database import Match, PlayerInMatch, SteamProfile, Database
from json_parser import parse_replay

def main():
    #match_id = 7356874131
    match_id = 7470591268

    #res = requests.get(url=f"https://api.opendota.com/api/matches/{match_id}?api_key=7a659faa-0957-46c5-be5d-91cede0c2f5a")
    #with open(f'{match_id}.json', 'wb') as f: 
    #    f.write(res.content)

    match_full_processing(['7356874131'])


def match_full_processing(matches_arr):
    database_ = Database(
            host=host,
            user=user,
            password=password,
            db_name=db_name,
            port=port)
    for match in matches_arr:
        parsed_data = parse_replay(match)

        with open(f'parsed_data.txt', 'w') as f: 
            f.write(str(parsed_data))

        if('lonedruid' not in parsed_data):
            #В не игре было Лон друида
            account_insert_req_arr, account_data_tuples_arr = [], []
            players_insert_req_arr, players_data_tuples_arr = [], []
            #Проверяем есть ли матч в базе данных
            if(database_.check_match(match)):
                #Запрашиваем информацию о матче с dota api
                answer = get_match(match)
                #Достаем id всех участников матча
                for player in answer['players']:
                    #Получаем данные профиля
                    plr = get_profile(player['account_id'])
                    steam_profile_ = SteamProfile(
                        account_id=player['account_id'],personaname=plr['personaname'],
                        prof_name=plr['name'],avatar_src=plr['avatar_src']
                        )
                    account_insert_req_arr.append(steam_profile_.get_INSERT_req())
                    account_data_tuples_arr.append(steam_profile_.get_data_tuple())
                    player_in_match_ = PlayerInMatch(
                        match_id=player['match_id'],account_id=player['account_id'],
                        rank_tier=player['rank_tier'],isRadiant=player['isRadiant'],
                        player_slot=player['player_slot'],party_id=player['party_id'],
                        party_size=player['party_size'],personaname=player['personaname'],
                        name=player['name'],hero_id=player['hero_id'],level=player['level'],
                        net_worth=player['net_worth'],kills=player['kills'],deaths=player['deaths'],
                        assists=player['assists'],last_hits=player['last_hits'],denies=player['denies'],
                        gold_per_min=player['gold_per_min'],xp_per_min=player['xp_per_min'],
                        item_0=player['item_0'],item_1=player['item_1'],item_2=player['item_2'],
                        item_3=player['item_3'],item_4=player['item_4'],item_5=player['item_5'],
                        item_neutral=player['item_neutral'],backpack_0=player['backpack_0'],
                        backpack_1=player['backpack_1'],backpack_2=player['backpack_2'],
                        hero_damage=player['hero_damage'],hero_healing=player['hero_healing'],
                        tower_damage=player['tower_damage'],ability_upgrades_arr=player['ability_upgrades_arr'],
                        additional_units=get_additional_units(player['hero_id']),
                        movement_by_time=get_parsed_data(hero_id=player['hero_id'],parsed_data=parsed_data,who='movement'),
                        lhts_by_time=get_parsed_data(hero_id=player['hero_id'],parsed_data=parsed_data,who='lhts'),
                        networth_by_time=get_parsed_data(hero_id=player['hero_id'],parsed_data=parsed_data,who='networth'),
                        purchase_by_time=get_parsed_data(hero_id=player['hero_id'],parsed_data=parsed_data,who='purchase_log'),
                        kills_by_time=get_parsed_data(hero_id=player['hero_id'],parsed_data=parsed_data,who='kills_log')
                            )
                    players_insert_req_arr.append(player_in_match_.get_INSERT_req())
                    players_data_tuples_arr.append(player_in_match_.get_data_tuple())
                #Создаем элемент матча для занесения в базу данных
                match_ = Match(
                            match_id=answer['match_id'],game_mode=answer['game_mode'],
                            lobby_type=answer['lobby_type'],leagueid=answer['leagueid'],
                            series_id=answer['series_id'],series_type=answer['series_type'],
                            human_players=answer['human_players'],start_time=answer['start_time'],
                            match_seq_num=answer['match_seq_num'],duration=answer['duration'],
                            dire_score=answer['dire_score'],dire_team_id=answer['dire_team_id'],
                            radiant_score=answer['radiant_score'],radiant_team_id=answer['radiant_team_id'],
                            radiant_win=answer['radiant_win'],patch=answer['patch'],
                            region=answer['region'],replay_url=answer['replay_url'],
                            picks_bans=answer['picks_bans']
                            )
                #Вносим информацию в базу данных
                database_.insert_data(
                    match_.get_INSERT_req(),match_.get_data_tuple(),
                    account_insert_req_arr,account_data_tuples_arr,
                    players_insert_req_arr,players_data_tuples_arr
                    )
        else:
            #В игре был Лон друид занчит нам надо будет дополнительно вызывать valve api
            pass        

def get_parsed_data(hero_id,parsed_data,who):
    with open('dota\heroes.json') as file_:
        file_ = json.loads(file_.read())
        hero_name = file_[f'{hero_id}']['name'].lower().replace('_','')[11:]
        return parsed_data[hero_name][who]
    
def get_additional_units(hero_id):
    if(hero_id == 80):
        with open('dota\heroes.json') as file_:
            file_ = json.loads(file_.read())
            res = requests.get(url=f"https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v1/?match_id=7356874131&key=5D500F9B0FDACA07F87220B405F32342").json()
            for player in res['result']['players']:
                if player['hero_id'] == hero_id:
                    return res['result']['players'][2]['additional_units']
    else:
        return None

#Возвращает имя в стиме и аватар
def get_profile(profile_id):
    try:
        answer = requests.get(url=f"https://api.opendota.com/api/players/{profile_id}").json()
        #Создаем папку для хранения аватара пользователя
        if not os.path.exists(f"images/{profile_id}"):
            os.mkdir(f"images/{profile_id}")
        #Получение аватарки
        answerProfileAvatar = answer['profile']['avatarfull']
        profile_Avatar = requests.get(url=f"{answerProfileAvatar}")
        #Сохраняем аватарку или перезаписываем
        with open(f'images/{profile_id}/avatar.jpg', 'wb') as f: 
            f.write(profile_Avatar.content)

        return {'personaname': answer['profile']['personaname'],'name': answer['profile']['name'],'avatar_src': f'images/{profile_id}/avatar.jpg'}
    except:
        print("[get_profile()] Неправильный profile_id или другая ошибка!")
        return None

#Возвращает информацию о определенном матче
def get_match(match_id):
    try:
        return requests.get(url=f"https://api.opendota.com/api/matches/{match_id}").json()
    except:
        print("[get_match()] Неправильный match_id")
        return None


if __name__ == '__main__':
    main()