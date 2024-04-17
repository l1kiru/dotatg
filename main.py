import os
import json
import requests
import time

from dbconfig import host, user, password, db_name, port
from database import Match, PlayerInMatch, SteamProfile, Database
from database import MatchPlayerKDA, MatchPlayerNetworth, MatchPlayerLvlUp
from json_parser import parse_replay

def main():
    match_id = '7690580819'

    match_full_processing([f'{match_id}'])


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

        account_insert_req_arr, account_data_tuples_arr = [], []
        players_insert_req_arr, players_data_tuples_arr = [], []
        player_kda_insert_req_arr, player_kda_data_tuples_arr = [], []
        player_networth_insert_req_arr, player_networth_data_tuples_arr = [], []
        player_lvlup_insert_req_arr, player_lvlup_data_tuples_arr = [], []

        #Проверяем есть ли матч в базе данных
        if(database_.check_match(match)):
            #Запрашиваем информацию о матче с dota api
            answer = get_match(match)
            #Достаем id всех участников матча
            max_index = database_.get_startids() + 1
            for player in answer['players']:
                #Получаем данные профиля
                if(player['account_id']!= None):
                    plr = get_profile(player['account_id'])
                    steam_profile_ = SteamProfile(
                    account_id=player['account_id'],personaname=plr['personaname'],
                    prof_name=plr['name'],avatar_src=plr['avatar_src']
                    )
                    account_insert_req_arr.append(steam_profile_.get_INSERT_req())
                    account_data_tuples_arr.append(steam_profile_.get_data_tuple())
                account_names = get_profile_names(player)
                player_in_match_ = PlayerInMatch(
                    match_id=match,account_id=account_names['account_id'],
                    rank_tier=player['rank_tier'],isRadiant=player['isRadiant'],
                    player_slot=player['player_slot'],party_id=player['party_id'],
                    party_size=player['party_size'],personaname=account_names['personaname'],
                    name=account_names['name'],hero_id=player['hero_id'],
                    item_0=player['item_0'],item_1=player['item_1'],item_2=player['item_2'],
                    item_3=player['item_3'],item_4=player['item_4'],item_5=player['item_5'],
                    item_neutral=player['item_neutral'],backpack_0=player['backpack_0'],
                    backpack_1=player['backpack_1'],backpack_2=player['backpack_2'],
                    hero_damage=player['hero_damage'],hero_healing=player['hero_healing'],
                    tower_damage=player['tower_damage'],
                    movement_by_time=get_parsed_data(hero_id=player['hero_id'],parsed_data=parsed_data,who='movement'),
                    mpk_id=max_index,mpn_id=max_index,mpl_id=max_index)
                
                player_kda = MatchPlayerKDA(mpk_id=max_index,kills=player['kills'],deaths=player['deaths'],assists=player['assists'],
                                            last_hits=player['last_hits'],denies=player['denies'],
                                            kills_by_time=get_parsed_data(hero_id=player['hero_id'],parsed_data=parsed_data,who='kills_log'),
                                            lhts_by_time=get_parsed_data(hero_id=player['hero_id'],parsed_data=parsed_data,who='lhts'))
                
                player_kda_insert_req_arr.append(player_kda.get_INSERT_req())
                player_kda_data_tuples_arr.append(player_kda.get_data_tuple())

                player_networth = MatchPlayerNetworth(mpn_id=max_index,net_worth=player['net_worth'],gold_per_min=player['gold_per_min'],
                                                    networth_by_time=get_parsed_data(hero_id=player['hero_id'],parsed_data=parsed_data,who='networth'),
                                                    purchase_by_time=get_parsed_data(hero_id=player['hero_id'],parsed_data=parsed_data,who='purchase_log'),
                                                    additional_units=get_additional_units(player['hero_id'],match)
                                                    )
                
                player_networth_insert_req_arr.append(player_networth.get_INSERT_req())
                player_networth_data_tuples_arr.append(player_networth.get_data_tuple())

                player_lvlup = MatchPlayerLvlUp(mpl_id=max_index,level=player['level'],xp_per_min=player['xp_per_min'],
                                                ability_upgrades_arr=player['ability_upgrades_arr'])

                player_lvlup_insert_req_arr.append(player_lvlup.get_INSERT_req())
                player_lvlup_data_tuples_arr.append(player_lvlup.get_data_tuple())

                players_insert_req_arr.append(player_in_match_.get_INSERT_req())
                players_data_tuples_arr.append(player_in_match_.get_data_tuple())

                max_index += 1
            #Создаем элемент матча для занесения в базу данных
            match_ = Match(
                        match_id=answer['match_id'],game_mode=answer['game_mode'],
                        lobby_type=answer['lobby_type'],league_id=answer['leagueid'],
                        series_id=answer['series_id'] if('series_id' in answer) else None,
                        series_type=answer['series_type'] if('series_id' in answer) else None,
                        start_time=answer['start_time'],
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
                players_insert_req_arr,players_data_tuples_arr,
                player_kda_insert_req_arr,player_kda_data_tuples_arr,
                player_networth_insert_req_arr,player_networth_data_tuples_arr,
                player_lvlup_insert_req_arr,player_lvlup_data_tuples_arr
                ) 


def get_parsed_data(hero_id,parsed_data,who):
    with open('dota/heroes.json') as file_:
        file_ = json.loads(file_.read())
        hero_name = file_[f'{hero_id}']['name'].lower().replace('_','')[11:]
        return parsed_data[hero_name][who]
    
def get_additional_units(hero_id,match_id):
    if(hero_id == 80):
        with open('dota/heroes.json') as file_:
            file_ = json.loads(file_.read())
            res = requests.get(url=f"https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v1/?match_id={match_id}&key=5D500F9B0FDACA07F87220B405F32342").json()
            for player in res['result']['players']:
                if player['hero_id'] == hero_id:
                    return res['result']['players'][2]['additional_units']
    else:
        return None

def get_profile_names(player):
    if(player['account_id']!= None):
        return player
    else: return {'account_id': "Unknown",'personaname': "Anonymous",'name': None}

#Возвращает имя в стиме и аватар
def get_profile(profile_id):
    if not os.path.exists("images"):
        os.mkdir("images")
    if(profile_id != None):
        try:
            answer = requests.get(url=f"https://api.opendota.com/api/players/{profile_id}").json()
            #Создаем папку для хранения аватара пользователя
            if not os.path.exists(f"images/{profile_id}"):
                os.mkdir(f"images/{profile_id}")
            #Получение аватарки
            answerProfileAvatar = answer['profile']['avatarfull']
            if(answerProfileAvatar != None):
                profile_Avatar = requests.get(url=f"{answerProfileAvatar}")
                #Сохраняем аватарку или перезаписываем
                with open(f'images/{profile_id}/avatar.jpg', 'wb') as f: 
                    f.write(profile_Avatar.content)
            
                return {'personaname': answer['profile']['personaname'],'name': answer['profile']['name'],'avatar_src': f'images/{profile_id}/avatar.jpg'}
            return {'personaname': answer['profile']['personaname'],'name': answer['profile']['name'],'avatar_src': None}
        except:
            print("[get_profile()] Неправильный profile_id или другая ошибка!")
            return None
    else:
        return {'personaname': None,'name': None,'avatar_src': None}

#Возвращает информацию о определенном матче
def get_match(match_id):
    try:
        return requests.get(url=f"https://api.opendota.com/api/matches/{match_id}").json()
    except:
        print("[get_match()] Неправильный match_id")
        return None


if __name__ == '__main__':
    main()