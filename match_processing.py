from datetime import datetime
import os
import json
import requests
from dotenv import load_dotenv

from json_parser import parse_replay
from database import session_factory
from models import ProfileORM, MatchPlayerORM, MatchPlayerKdaORM
from models import MatchPlayerNetworthORM, MatchPlayerLvlUpORM, MatchORM

load_dotenv()
op_api_key= os.getenv('OPENDOTAAPIKEY')
steam_api_key= os.getenv('STEAMAPIKEY')

def match_full_processing(match_id):
    with session_factory() as session:
        if(not session.get(MatchORM,match_id)):
            #Получаем данные из реплея если есть ссылка, иначе Null
            parsed_data = parse_replay(match_id)
            #Запрашиваем информацию о матче с dota api
            answer = get_match(match_id)
            steam_profiles_arr = []
            min_ = answer.get('duration') // 60
            duration = f"{min_ // 3600}:{min_ % 60}:{answer.get('duration') % 60}"
            match_ = MatchORM(
                id=answer.get('match_id'),game_mode=answer.get('game_mode'),
                lobby_type=answer.get('lobby_type'),league_id=answer.get('leagueid'),
                series_id=answer.get('series_id'),series_type=answer.get('series_type'),
                start_time=answer.get('start_time'),
                match_seq_num=answer.get('match_seq_num'),duration=duration,
                dire_score=answer.get('dire_score'),dire_team_id=answer.get('dire_team_id'),
                radiant_score=answer.get('radiant_score'),radiant_team_id=answer.get('radiant_team_id'),
                radiant_win= True if(answer.get('radiant_win') == 0) else False,
                patch=answer.get('patch'),region=answer.get('region'),replay_url=answer.get('replay_url'),
                picks_bans=answer.get('picks_bans')
            )
            for player in answer['players']:
                account_names = get_profile_names(player)
                player_in_match = MatchPlayerORM(
                    rank_tier=player.get('rank_tier'),
                    isradiant= True if(player.get('isRadiant') == 0) else False,
                    player_slot=player.get('player_slot'),party_id=player.get('party_id'),
                    party_size=player.get('party_size'),
                    personaname=account_names.get('personaname') if account_names.get('personaname') else 'Аноним',
                    name=account_names.get('name'),hero_id=player.get('hero_id'),
                    inventory=create_inventory(
                        [player.get('item_0'),player.get('item_1'),player.get('item_2'),player.get('item_3'),
                        player.get('item_4'),player.get('item_5'),player.get('item_neutral'),
                        player.get('backpack_0'),player.get('backpack_1'),player.get('backpack_2')]),
                    hero_damage=player.get('hero_damage'),hero_healing=player.get('hero_healing'),
                    tower_damage=player.get('tower_damage'),
                    movement_by_time=get_parsed_data(hero_id=player['hero_id'],parsed_data=parsed_data,who='movement')
                )
                player_kda = MatchPlayerKdaORM(
                    kills=player.get('kills'),deaths=player.get('deaths'),assists=player.get('assists'),
                    last_hits=player.get('last_hits'),denies=player.get('denies'),
                    kills_by_time=get_parsed_data(hero_id=player['hero_id'],parsed_data=parsed_data,who='kills_log'),
                    lhts_by_time=get_parsed_data(hero_id=player['hero_id'],parsed_data=parsed_data,who='lhts')
                )
                player_lvlup = MatchPlayerLvlUpORM(
                    level=player.get('level'),xp_per_min=player.get('xp_per_min'),
                    ability_upgrades_arr=player.get('ability_upgrades_arr')
                )
                player_networth = MatchPlayerNetworthORM(
                    net_worth=player.get('net_worth'),gold_per_min=player.get('gold_per_min'),
                    networth_by_time=get_parsed_data(hero_id=player['hero_id'],parsed_data=parsed_data,who='networth'),
                    purchase_by_time=get_parsed_data(hero_id=player['hero_id'],parsed_data=parsed_data,who='purchase_log'),
                    additional_units=get_additional_units(player['hero_id'],match_id)
                )
                player_in_match.mp_kda = player_kda
                player_in_match.mp_lvlup = player_lvlup
                player_in_match.mp_networth = player_networth
                steam_profile = None
                match_.players.append(player_in_match)
                #Получаем данные профиля
                if(player.get('account_id')!= None and player.get('account_id') != "Unknown"):
                    plr = get_profile(player['account_id'])
                    try:
                        steam_profile = session.get(ProfileORM,player.get('account_id'))
                        steam_profile.personaname = plr['personaname']
                        steam_profile.prof_name = plr['name']
                        steam_profile.avatar_src = plr['avatar_src']
                        steam_profile.played_matches.append(player_in_match)
                    except:
                        steam_profile = ProfileORM(
                            account_id=player.get('account_id'),personaname=plr['personaname'],
                            prof_name=plr['name'],avatar_src=plr['avatar_src'])
                        steam_profile.played_matches.append(player_in_match)
                        steam_profiles_arr.append(steam_profile)
            session.add(match_)
            session.add_all(steam_profiles_arr)
            session.commit()
        else:
            return "Такой матч уже есть в базе."
    return "Матч обработан."

async def match_full_processing_async(match_id):
    status = 0
    print(f"Поступил запрос на match_id: {match_id}")
    try:
        with session_factory() as session:
            current_match = session.get(MatchORM,match_id)
            if(not current_match):
                #Получаем данные из реплея если есть ссылка, иначе Null
                parsed_data = parse_replay(match_id)
                #Запрашиваем информацию о матче с dota api
                answer = get_match(match_id)
                if("{'error': 'Not Found'}" in str(answer)):
                    return "Неправльный id матча, попробуйте еще раз."
                steam_profiles_arr = []
                min_ = answer.get('duration') // 60
                duration = f"{min_ // 60}:{min_ % 60}:{answer.get('duration') % 60}"
                match_ = MatchORM(
                    id=answer.get('match_id'),game_mode=answer.get('game_mode'),
                    lobby_type=answer.get('lobby_type'),league_id=answer.get('leagueid'),
                    series_id=answer.get('series_id'),series_type=answer.get('series_type'),
                    start_time=answer.get('start_time'),
                    match_seq_num=answer.get('match_seq_num'),duration=duration,
                    dire_score=answer.get('dire_score'),dire_team_id=answer.get('dire_team_id'),
                    radiant_score=answer.get('radiant_score'),radiant_team_id=answer.get('radiant_team_id'),
                    radiant_win= False if(answer.get('radiant_win') == 0) else True,
                    patch=answer.get('patch'),region=answer.get('region'),replay_url=answer.get('replay_url'),
                    picks_bans=answer.get('picks_bans')
                )
                for player in answer['players']:
                    account_names = get_profile_names(player)
                    player_in_match = MatchPlayerORM(
                        rank_tier=player.get('rank_tier'),
                        isradiant= False if(player.get('isRadiant') == 0) else True,
                        player_slot=player.get('player_slot'),party_id=player.get('party_id'),
                        party_size=player.get('party_size'),
                        personaname= (account_names.get('personaname')) if account_names.get('personaname') else 'Аноним',
                        name=account_names.get('name'),hero_id=player.get('hero_id'),
                        inventory=create_inventory(
                            [player.get('item_0'),player.get('item_1'),player.get('item_2'),player.get('item_3'),
                            player.get('item_4'),player.get('item_5'),player.get('item_neutral'),
                            player.get('backpack_0'),player.get('backpack_1'),player.get('backpack_2')]),
                        hero_damage=player.get('hero_damage'),hero_healing=player.get('hero_healing'),
                        tower_damage=player.get('tower_damage'),
                        movement_by_time=get_parsed_data(hero_id=player['hero_id'],parsed_data=parsed_data,who='movement')
                    )
                    player_kda = MatchPlayerKdaORM(
                        kills=player.get('kills'),deaths=player.get('deaths'),assists=player.get('assists'),
                        last_hits=player.get('last_hits'),denies=player.get('denies'),
                        kills_by_time=get_parsed_data(hero_id=player['hero_id'],parsed_data=parsed_data,who='kills_log'),
                        lhts_by_time=get_parsed_data(hero_id=player['hero_id'],parsed_data=parsed_data,who='lhts')
                    )
                    player_lvlup = MatchPlayerLvlUpORM(
                        level=player.get('level'),xp_per_min=player.get('xp_per_min'),
                        ability_upgrades_arr=player.get('ability_upgrades_arr')
                    )
                    player_networth = MatchPlayerNetworthORM(
                        net_worth=player.get('net_worth'),gold_per_min=player.get('gold_per_min'),
                        networth_by_time=get_parsed_data(hero_id=player['hero_id'],parsed_data=parsed_data,who='networth'),
                        purchase_by_time=get_parsed_data(hero_id=player['hero_id'],parsed_data=parsed_data,who='purchase_log'),
                        additional_units=get_additional_units(player['hero_id'],match_id)
                    )
                    player_in_match.mp_kda = player_kda
                    player_in_match.mp_lvlup = player_lvlup
                    player_in_match.mp_networth = player_networth
                    steam_profile = None
                    match_.players.append(player_in_match)
                    #Получаем данные профиля
                    if(player.get('account_id')!= None and player.get('account_id') != "Unknown"):
                        plr = get_profile(player['account_id'])
                        try:
                            steam_profile = session.get(ProfileORM,player.get('account_id'))
                            steam_profile.personaname = plr['personaname'] if plr['personaname'] else 'Аноним'
                            steam_profile.prof_name = plr['name']
                            steam_profile.avatar_src = plr['avatar_src']
                            steam_profile.played_matches.append(player_in_match)
                        except:
                            steam_profile = ProfileORM(
                                account_id=player.get('account_id'),personaname=plr['personaname'] if plr['personaname'] else 'Аноним',
                                prof_name=plr['name'],avatar_src=plr['avatar_src'])
                            steam_profile.played_matches.append(player_in_match)
                            steam_profiles_arr.append(steam_profile)
                session.add(match_)
                session.add_all(steam_profiles_arr)
                session.commit()
                if(get_parsed_data(hero_id=player['hero_id'],parsed_data=parsed_data,who='movement')):
                    status = 2
                else:
                    status = 1
            else:
                if(current_match.players[0].movement_by_time):
                    return "Этот матч уже есть в базе."
                else:
                    days = (datetime.now() - datetime.fromtimestamp(current_match.start_time)).days 
                    parsed_data = parse_replay(match_id)
                    if(parsed_data):
                        for player in current_match.players:
                            player.movement_by_time = get_parsed_data(hero_id=player.hero_id,parsed_data=parsed_data,who='movement')
                            player.mp_kda.kills_by_time = get_parsed_data(hero_id=player.hero_id,parsed_data=parsed_data,who='kills_log')
                            player.mp_kda.lhts_by_time = get_parsed_data(hero_id=player.hero_id,parsed_data=parsed_data,who='lhts')
                            player.mp_networth.networth_by_time = get_parsed_data(hero_id=player.hero_id,parsed_data=parsed_data,who='networth')
                            player.mp_networth.purchase_by_time = get_parsed_data(hero_id=player.hero_id,parsed_data=parsed_data,who='purchase_log')
                            session.commit()
                            return f"Этот матч уже есть в базе, данные обновлены."
                    elif(days >= 7 and not parsed_data):
                        return f"Этот матч уже есть базе, но не все данные были записаны. Прошло больше 7 дней ({days}) со старта матча. Ссылка на реплей удалена. Нельзя получить расширенные данные."
                    else:
                        return f"Этот матч уже в базе данных, но не все данные были записаны. Не удалось получить ссылку на запись, попробуйте еще раз позже."
        if(status == 2):
            return "Матч обработан."
        else:
            return "Матч обработан, но не все данные были записаны."
    except Exception as _ex:
        print(_ex)
        return "Неизвестная ошибка."

async def matches_full_processing_async(account_id):
    req = requests.get(url=f'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v1/?account_id={account_id}&key={steam_api_key}')
    for match in req.json()['result']['matches']:
        print(match['match_id'])

def get_parsed_data(hero_id,parsed_data,who):
    if(parsed_data):
        with open('dota/heroes.json') as file_:
            file_ = json.loads(file_.read())
            hero_name = file_[f'{hero_id}']['name'].lower().replace('_','')[11:]
            return parsed_data[hero_name][who]
    else:
        return None
    
def get_additional_units(hero_id,match_id):
    if(hero_id == 80):
        with open('dota/heroes.json') as file_:
            file_ = json.loads(file_.read())
            res = requests.get(url=f"https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v1/?match_id={match_id}&key={steam_api_key}").json()
            for player in res['result']['players']:
                if player['hero_id'] == hero_id:
                    return res['result']['players'][2]['additional_units']
    else:
        return None

def create_inventory(item_arr):
    slots_names = ['item_0','item_1','item_2','item_3','item_4','item_5','item_neutral','backpack_0','backpack_1','backpack_2']
    counter = 0
    inventory = []
    for item in item_arr:
        if(item is not None):
            inventory.append({slots_names[counter] : item})
        else:
            raise Exception(f"[create_inventory()] Неверный атрибут {item}")
        counter += 1
    return inventory

def get_profile_names(player):
    if(player.get('account_id')!= None):
        return player
    else: return {'account_id': "Unknown",'personaname': "Аноним",'name': None}

#Возвращает имя в стиме и аватар
def get_profile(profile_id):
    if not os.path.exists("images"):
        os.mkdir("images")
    if(profile_id != None):
        try:
            answer = requests.get(url=f"https://api.opendota.com/api/players/{profile_id}?api_key={op_api_key}").json()
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
        return requests.get(url=f"https://api.opendota.com/api/matches/{match_id}?api_key={op_api_key}").json()
    except:
        print("[get_match()] Неправильный match_id")
        return None