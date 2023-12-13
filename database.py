import psycopg2
import json

class Match:
    def __init__(self,match_id,game_mode,lobby_type,leagueid,
                 series_id,series_type,human_players,start_time,
                 match_seq_num,duration,dire_score,dire_team_id,
                 radiant_score,radiant_team_id,radiant_win,
                 patch,region,replay_url,picks_bans):
        #integer
        if(match_id is not None): self.match_id = match_id
        else: raise Exception("[class match()] Неверный атрибут match_id")
        #integer
        if(game_mode is not None): self.game_mode = game_mode
        else: raise Exception("[class match()] Неверный атрибут game_mode")
        #integer
        if(lobby_type is not None): self.lobby_type = lobby_type
        elif(lobby_type is None): self.lobby_type = lobby_type
        else: raise Exception("[class match()] Неверный атрибут lobby_type")
        #integer
        if(leagueid is not None): self.leagueid = leagueid
        elif(leagueid is None): self.leagueid = leagueid
        else: raise Exception("[class match()] Неверный атрибут leagueid")
        #integer
        if(series_id is not None): self.series_id = series_id
        elif(series_id is None): self.series_id = series_id
        else: raise Exception("[class match()] Неверный атрибут series_id")
        #integer
        if(series_type is not None): self.series_type = series_type
        elif(series_type is None): self.series_type = series_type
        else: raise Exception("[class match()] Неверный атрибут series_type")
        #integer
        if(human_players is not None): self.human_players = human_players
        else: raise Exception("[class match()] Неверный атрибут human_players")
        #timestamp
        if(start_time is not None): self.start_time = start_time
        else: raise Exception("[class match()] Неверный атрибут start_time")
        #integer
        if(match_seq_num is not None):self.match_seq_num = match_seq_num
        else: raise Exception("[class match()] Неверный атрибут match_seq_num")
        #integer -> time without time zone
        if(duration is not None):
            min_ = duration // 60
            self.duration = f"{min_ // 60}:{min_ % 60}:{duration % 60}"
        else: raise Exception("[class match()] Неверный атрибут duration")
        #integer
        if(dire_score is not None): self.dire_score = dire_score
        else: raise Exception("[class match()] Неверный атрибут dire_score")
        #integer
        if(dire_team_id is not None): self.dire_team_id = dire_team_id
        elif(dire_team_id is None): self.dire_team_id = dire_team_id
        else: raise Exception("[class match()] Неверный атрибут dire_team_id")
        #integer
        if(radiant_score is not None): self.radiant_score = radiant_score
        else: raise Exception("[class match()] Неверный атрибут radiant_score")
        #integer
        if(radiant_team_id is not None): self.radiant_team_id = radiant_team_id
        elif(radiant_team_id is None): self.radiant_team_id = radiant_team_id
        else: raise Exception("[class match()] Неверный атрибут radiant_team_id")
        #integer
        if(radiant_win is not None):
            if(radiant_win == 0): self.radiant_win = False
            else: self.radiant_win = True
        else: raise Exception("[class match()] Неверный атрибут radiant_win")
        #integer
        if(patch is not None): self.patch = patch
        else: raise Exception("[class match()] Неверный атрибут patch")
        #integer
        if(region is not None): self.region = region
        else: raise Exception("[class match()] Неверный атрибут region")
        #string
        if(replay_url is not None):
            if("http://replay" in replay_url): self.replay_url = replay_url
            else: raise Exception("[class match()] Неверный атрибут replay_url")
        else: raise Exception("[class match()] Неверный атрибут replay_url")
        #json
        if(picks_bans is not None ):
            try:
                self.picks_bans = json.dumps(picks_bans)
            except ValueError:
                raise Exception("[class match()] Неверный атрибут picks_bans")
        elif(picks_bans is None): self.picks_bans = picks_bans
        else: raise Exception("[class match()] Неверный атрибут picks_bans")

    def get_INSERT_req(self):
        return """INSERT INTO match (match_id,game_mode,lobby_type,leagueid,
                 series_id,series_type,human_players,start_time,
                 match_seq_num,duration,dire_score,dire_team_id,
                 radiant_score,radiant_team_id,radiant_win,
                 patch,region,replay_url,picks_bans) 
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
    def get_data_tuple(self):
        return (self.match_id,self.game_mode,self.lobby_type,self.leagueid,
                self.series_id,self.series_type,self.human_players,self.start_time,
                self.match_seq_num,self.duration,self.dire_score,self.dire_team_id,
                self.radiant_score,self.radiant_team_id,self.radiant_win,
                self.patch,self.region,self.replay_url,self.picks_bans)

class PlayerInMatch:
    def __init__(self,match_id,account_id,rank_tier,isRadiant,
                 player_slot,party_id,party_size,personaname,
                 name,hero_id,level,net_worth,kills,deaths,assists,
                 last_hits,denies,gold_per_min,xp_per_min,
                 
                 item_0,item_1,item_2,item_3,item_4,item_5,item_neutral,
                 backpack_0,backpack_1,backpack_2,
                 
                 hero_damage,hero_healing,tower_damage,
                 ability_upgrades_arr,additional_units,
                 movement_by_time,lhts_by_time,networth_by_time,
                 purchase_by_time,kills_by_time):
        #integer
        if(match_id is not None): self.match_id = match_id
        else: raise Exception("[class player()] Неверный атрибут match_id")
        #integer or None
        self.account_id = account_id
        #integer
        if(rank_tier is not None): self.rank_tier = rank_tier
        elif(rank_tier is None): self.rank_tier = rank_tier
        else: raise Exception("[class player()] Неверный атрибут rank_tier")
        #integer
        if(isRadiant is not None and (isRadiant == 0 or isRadiant == 1)):
            self.isRadiant = False if(isRadiant == 0) else  True
        else: raise Exception("[class player()] Неверный атрибут isRadiant")
        #integer
        if(player_slot is not None): self.player_slot = player_slot
        else: raise Exception("[class player()] Неверный атрибут player_slot")
        #integer
        if(party_id is not None): self.party_id = party_id
        elif(party_id is None): self.party_id = party_id
        else: raise Exception("[class player()] Неверный атрибут party_id")
        #integer
        if(party_size is not None): self.party_size = party_size
        elif(party_size is None): self.party_size = party_size
        else: raise Exception("[class player()] Неверный атрибут party_size")
        #string
        self.personaname = personaname
        #string 
        self.name = name
        #integer
        if(hero_id is not None): self.hero_id = hero_id
        else: raise Exception("[class player()] Неверный атрибут hero_id")
        #integer
        if(level is not None): self.level = level
        else: raise Exception("[class player()] Неверный атрибут level")
        #integer
        if(net_worth is not None): self.net_worth = net_worth
        else: raise Exception("[class player()] Неверный атрибут net_worth")
        #integer
        if(kills is not None): self.kills = kills
        else: raise Exception("[class player()] Неверный атрибут kills")
        #integer
        if(deaths is not None): self.deaths = deaths
        else: raise Exception("[class player()] Неверный атрибут deaths")
        #integer
        if(assists is not None): self.assists = assists
        else: raise Exception("[class player()] Неверный атрибут assists")
        #integer
        if(last_hits is not None): self.last_hits = last_hits
        else: raise Exception("[class player()] Неверный атрибут last_hits")
        #integer
        if(denies is not None): self.denies = denies
        else: raise Exception("[class player()] Неверный атрибут denies")
        #integer
        if(gold_per_min is not None): self.gold_per_min = gold_per_min
        else: raise Exception("[class player()] Неверный атрибут gold_per_min")
        #integer
        if(xp_per_min is not None): self.xp_per_min = xp_per_min
        else: raise Exception("[class player()] Неверный атрибут xp_per_min")
        #item_0,item_1,item_2,item_3,item_4,item_5,item_neutral,backpack_0,backpack_1,backpack_2
        #json
        inventory = create_inventory([item_0,item_1,item_2,item_3,item_4,item_5,item_neutral,backpack_0,backpack_1,backpack_2])
        self.inventory = json.dumps(inventory)
        #integer
        if(hero_damage is not None): self.hero_damage = hero_damage
        else: raise Exception("[class player()] Неверный атрибут hero_damage")
        #integer
        if(hero_healing is not None): self.hero_healing = hero_healing
        elif(hero_healing is None): self.hero_healing = hero_healing
        else: raise Exception("[class player()] Неверный атрибут hero_healing")
        #integer
        if(tower_damage is not None): self.tower_damage = tower_damage
        elif(tower_damage is None): self.tower_damage = tower_damage
        else: raise Exception("[class player()] Неверный атрибут tower_damage")
        #json
        if(ability_upgrades_arr is not None ):
            try:
                self.ability_upgrades_arr = json.dumps(ability_upgrades_arr)
            except ValueError:
                raise Exception("[class player()] Неверный атрибут ability_upgrades_arr")
        else: raise Exception("[class player()] Неверный атрибут ability_upgrades_arr")
        #json
        if(additional_units is not None ):
            try:
                self.additional_units = json.dumps(additional_units)
            except ValueError:
                raise Exception("[class player()] Неверный атрибут additional_units")
        elif(additional_units is None): self.additional_units = additional_units
        else: raise Exception("[class player()] Неверный атрибут additional_units")
        #json
        self.movement_by_time = json.dumps(list(movement_by_time))
        #json
        self.lhts_by_time = json.dumps(list(lhts_by_time))
        #json
        self.networth_by_time = json.dumps(list(networth_by_time))
        #json
        self.purchase_by_time = json.dumps(list(purchase_by_time))
        #json
        self.kills_by_time = json.dumps(list(kills_by_time))

    def get_INSERT_req(self):
        return """INSERT INTO match_player (match_id,account_id,rank_tier,
                 isRadiant,player_slot,party_id,party_size,personaname,
                 name,hero_id,level,net_worth,kills,deaths,assists,
                 last_hits,denies,gold_per_min,xp_per_min,
                 
                 inventory,
                 
                 hero_damage,hero_healing,tower_damage,
                 ability_upgrades_arr,additional_units,
                 movement_by_time,lhts_by_time,networth_by_time,
                 purchase_by_time,kills_by_time
                 ) 
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
    def get_data_tuple(self):
        return  (self.match_id,self.account_id,self.rank_tier,self.isRadiant,
                 self.player_slot,self.party_id,self.party_size,self.personaname,
                 self.name,self.hero_id,self.level,self.net_worth,self.kills,self.deaths,
                 self.assists,self.last_hits,self.denies,self.gold_per_min,self.xp_per_min,
                 
                 self.inventory,
                 
                 self.hero_damage,self.hero_healing,self.tower_damage,
                 self.ability_upgrades_arr,self.additional_units,
                 self.movement_by_time,self.lhts_by_time,self.networth_by_time,
                 self.purchase_by_time,self.kills_by_time)

#item_0,item_1,item_2,item_3,item_4,item_5,item_neutral,backpack_0,backpack_1,backpack_2
def create_inventory(item_arr):
    slots_names = ['item_0','item_1','item_2','item_3','item_4','item_5','item_neutral','backpack_0','backpack_1','backpack_2']
    counter = 0
    inventory = []
    for item in item_arr:
        if(item is not None):
            inventory.append({slots_names[counter] : item})
        else:
            raise Exception(f"[class player() create_inventory()] Неверный атрибут {item}")
        counter += 1
    return inventory
            
class SteamProfile():
    def __init__(self,account_id,personaname,prof_name,avatar_src):
        #integer
        if(account_id is not None): self.account_id = account_id
        #else: raise Exception("[class steam_profile()] Неверный атрибут account_id")
        #String
        self.personaname = personaname
        #String
        self.prof_name = prof_name
        #String
        self.avatar_src = avatar_src
    def get_INSERT_req(self):
        return """INSERT INTO profile (account_id,personaname,prof_name,avatar_src) 
                    VALUES (%s,%s,%s,%s) 
                    ON CONFLICT (account_id)
                    DO UPDATE SET 
                    personaname = EXCLUDED.personaname, prof_name = EXCLUDED.prof_name;"""
    def get_data_tuple(self):
        return(self.account_id,self.personaname,self.prof_name,self.avatar_src)

class Database():
    def __init__(self,host,user,password,db_name,port):
        self.host=host
        self.user=user
        self.password=password
        self.db_name=db_name
        self.port=port
    
    def insert_data(self,match_insert_req,match_data_tuple,
                    account_insert_req_arr, account_data_tuples_arr,
                    players_insert_req_arr,players_data_tuples_arr):
        try:
            #Подключение к базе данных
            connection = psycopg2.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.db_name,
                port=self.port
            )
            connection.autocommit = False
            with connection.cursor() as cursor:
                #Сначала мы добавляем в базу аккаунты игроков в стиме
                #если они у нас еще не хранятся 
                try:
                    if(account_insert_req_arr):
                        for i in range(len(account_insert_req_arr)):
                            cursor.execute(account_insert_req_arr[i], account_data_tuples_arr[i])
                except Exception as _ex:
                    raise Exception(f"[class player()] Добавляем в базу аккаунты игроков {_ex}")
                #Потом добавляем сам матч
                try:
                    cursor.execute(match_insert_req, match_data_tuple)
                except Exception as _ex:
                    raise Exception(f"[class player()] Добавляем сам матч {_ex}")
                #И в конце добавояем данные о том как каждый игрок сыграл этот матч
                try:
                    for i in range(10):
                        cursor.execute(players_insert_req_arr[i], players_data_tuples_arr[i])
                except Exception as _ex:
                    raise Exception(f"[class player()] Добавляем данные о том как каждый игрок сыграл {_ex}")
                #Если все удалось сохраняем изменения
                connection.commit()
        except Exception as _ex:
            #Добавить данные не удалось, выкидываем ошибку и откатываем изменения
            print(f"[class database()] [insert_data()] {_ex}")
            connection.rollback()
        finally:
            if connection: connection.close()

    def check_match(self,match_id):
        try:
            #Подключение к базе данных
            connection = psycopg2.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.db_name,
                port=self.port
            )
            connection.autocommit = False
            with connection.cursor() as cursor:
                cur = cursor.execute(f"SELECT * FROM match WHERE match_id={match_id}")
                if cur:
                    if cur.fetchone() is not None:
                        connection.commit()
                        if connection: connection.close()
                        return None
                connection.commit()
                if connection: connection.close()
                return match_id
        except Exception as _ex:
            print(f"[class database()] [check_match()] {_ex}")