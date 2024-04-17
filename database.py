import psycopg2
import json

class Match:
    def __init__(self,match_id,game_mode,lobby_type,league_id,
                 series_id,series_type,start_time,
                 match_seq_num,duration,dire_score,dire_team_id,
                 radiant_score,radiant_team_id,radiant_win,
                 patch,region,replay_url,picks_bans):
        self.match_id = match_id
        self.game_mode = game_mode
        self.lobby_type = lobby_type
        self.league_id = league_id
        self.series_id = series_id
        self.series_type = series_type
        self.start_time = start_time
        self.match_seq_num = match_seq_num

        min_ = duration // 60
        self.duration = f"{min_ // 60}:{min_ % 60}:{duration % 60}"

        self.dire_score = dire_score
        self.dire_team_id = dire_team_id
        self.radiant_score = radiant_score
        self.radiant_team_id = radiant_team_id
        self.radiant_win = True if(radiant_win == 0) else False
        self.patch = patch
        self.region = region
        self.replay_url = replay_url
        if(picks_bans is not None ):
            try:
                self.picks_bans = json.dumps(picks_bans)
            except ValueError:
                raise Exception("[class Match()] Неверный атрибут picks_bans")
        else: self.picks_bans = picks_bans

    def get_INSERT_req(self):
        return """INSERT INTO match (match_id,game_mode,lobby_type,
                 league_id,series_id,series_type,start_time,
                 match_seq_num,duration,dire_score,dire_team_id,
                 radiant_score,radiant_team_id,radiant_win,
                 patch,region,replay_url,picks_bans) 
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
    def get_data_tuple(self):
        return (self.match_id,self.game_mode,self.lobby_type,self.league_id,
                self.series_id,self.series_type,self.start_time,
                self.match_seq_num,self.duration,self.dire_score,self.dire_team_id,
                self.radiant_score,self.radiant_team_id,self.radiant_win,
                self.patch,self.region,self.replay_url,self.picks_bans)

class PlayerInMatch:
    def __init__(self,match_id,account_id,rank_tier,isRadiant,
                 player_slot,party_id,party_size,personaname,
                 name,hero_id,
                 item_0,item_1,item_2,item_3,item_4,item_5,item_neutral,
                 backpack_0,backpack_1,backpack_2,
                 hero_damage,hero_healing,tower_damage,movement_by_time,
                 mpk_id,mpn_id,mpl_id):
        
        self.match_id = match_id
        self.account_id = account_id
        self.rank_tier = rank_tier
        self.isRadiant = False if(isRadiant == 0) else  True
        self.player_slot = player_slot
        self.party_id = party_id
        self.party_size = party_size
        self.personaname = personaname
        self.name = name
        self.hero_id = hero_id

        #item_0,item_1,item_2,item_3,item_4,item_5,item_neutral,backpack_0,backpack_1,backpack_2
        inventory = create_inventory([item_0,item_1,item_2,item_3,item_4,item_5,item_neutral,backpack_0,backpack_1,backpack_2])
        self.inventory = json.dumps(inventory)
        
        self.hero_damage = hero_damage
        self.hero_healing = hero_healing
        self.tower_damage = tower_damage
        self.movement_by_time = json.dumps(movement_by_time)
        self.mpk_id = mpk_id
        self.mpn_id = mpn_id
        self.mpl_id = mpl_id

    def get_INSERT_req(self):
        return """INSERT INTO match_player (match_id,account_id,
                 rank_tier,isRadiant,player_slot,party_id,party_size,
                 personaname,name,hero_id,
                 inventory,
                 hero_damage,hero_healing,tower_damage,
                 movement_by_time,mpk_id,mpn_id,mpl_id
                 ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
    def get_data_tuple(self):
        return  (self.match_id,self.account_id,self.rank_tier,
                 self.isRadiant,self.player_slot,self.party_id,
                 self.party_size,self.personaname,self.name,self.hero_id,
                 
                 self.inventory,
                 
                 self.hero_damage,self.hero_healing,self.tower_damage,
                 self.movement_by_time,self.mpk_id,self.mpn_id,self.mpl_id) 

#item_0,item_1,item_2,item_3,item_4,item_5,item_neutral,backpack_0,backpack_1,backpack_2
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
        
class MatchPlayerKDA:
    def __init__(self,mpk_id,kills,deaths,assists,last_hits,
                 denies,kills_by_time,lhts_by_time):
        self.mpk_id = mpk_id
        self.kills = kills
        self.deaths = deaths
        self.assists = assists
        self.last_hits = last_hits
        self.denies = denies

        self.kills_by_time = json.dumps(kills_by_time)
        self.lhts_by_time = json.dumps(lhts_by_time)
    
    def get_INSERT_req(self):
        return """INSERT INTO match_player_kda (
                    mpk_id, kills, deaths, assists,
                    last_hits, denies, kills_by_time,
                    lhts_by_time
                 ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"""
    
    def get_data_tuple(self):
        return (self.mpk_id, self.kills, self.deaths,self.assists,
                self.last_hits, self.denies,self.kills_by_time,
                self.lhts_by_time)

class MatchPlayerNetworth:
    def __init__(self,mpn_id,net_worth,gold_per_min,
                 networth_by_time,purchase_by_time,
                 additional_units):
        self.mpn_id = mpn_id
        self.net_worth = net_worth
        self.gold_per_min = gold_per_min
        self.networth_by_time = json.dumps(networth_by_time)
        self.purchase_by_time = json.dumps(purchase_by_time)
        
        if(additional_units is not None ):
            try:
                self.additional_units = json.dumps(additional_units)
            except ValueError:
                raise Exception("[class MatchPlayerNetworth()] Неверный атрибут additional_units")
        else: self.additional_units = additional_units
    
    def get_INSERT_req(self):
        return """INSERT INTO match_player_networth (
                    mpn_id, net_worth, gold_per_min, 
                    networth_by_time, purchase_by_time,
                    additional_units
                 ) 
                VALUES (%s,%s,%s,%s,%s,%s);"""
    
    def get_data_tuple(self):
        return (self.mpn_id, self.net_worth, self.gold_per_min,
                self.networth_by_time, self.purchase_by_time,
                self.additional_units)

class MatchPlayerLvlUp:
    def __init__(self,mpl_id,level,xp_per_min,
                 ability_upgrades_arr):
        self.mpl_id = mpl_id
        self.level = level
        self.xp_per_min = xp_per_min
        try:
            self.ability_upgrades_arr = json.dumps(ability_upgrades_arr)
        except ValueError:
            raise Exception("[class MatchPlayerLvlUp()] Неверный атрибут ability_upgrades_arr")

    def get_INSERT_req(self):
        return """INSERT INTO match_player_lvlup (
                    mpl_id, level, xp_per_min, 
                    ability_upgrades_arr
                 ) 
                VALUES (%s,%s,%s,%s);"""
    
    def get_data_tuple(self):
        return (self.mpl_id, self.level, self.xp_per_min,
                self.ability_upgrades_arr)

class SteamProfile:
    def __init__(self,account_id,personaname,prof_name,avatar_src):
        if(account_id is not None): self.account_id = account_id
        self.personaname = personaname
        self.prof_name = prof_name
        self.avatar_src = avatar_src
    def get_INSERT_req(self):
        return """INSERT INTO profile (account_id,personaname,prof_name,avatar_src) 
                    VALUES (%s,%s,%s,%s) 
                    ON CONFLICT (account_id)
                    DO UPDATE SET 
                    personaname = EXCLUDED.personaname, prof_name = EXCLUDED.prof_name;"""
    def get_data_tuple(self):
        return(self.account_id,self.personaname,self.prof_name,self.avatar_src)

class Database:
    def __init__(self,host,user,password,db_name,port):
        self.host=host
        self.user=user
        self.password=password
        self.db_name=db_name
        self.port=port
    
    def insert_data(self,match_insert_req,match_data_tuple,
                    account_insert_req_arr, account_data_tuples_arr,
                    players_insert_req_arr,players_data_tuples_arr,
                    player_kda_insert_req_arr,player_kda_data_tuples_arr,
                    player_networth_insert_req_arr,player_networth_data_tuples_arr,
                    player_lvlup_insert_req_arr,player_lvlup_data_tuples_arr):
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
                    raise Exception(f"Добавляем в базу аккаунты игроков {_ex}")
                #Потом добавляем сам матч
                try:
                    cursor.execute(match_insert_req, match_data_tuple)
                except Exception as _ex:
                    raise Exception(f"Добавляем сам матч {_ex}")
                #И в конце добавояем данные о том как каждый игрок сыграл этот матч
                try:
                    for i in range(10):
                        cursor.execute(players_insert_req_arr[i], players_data_tuples_arr[i])
                        try:
                            cursor.execute(player_kda_insert_req_arr[i], player_kda_data_tuples_arr[i])
                            cursor.execute(player_networth_insert_req_arr[i], player_networth_data_tuples_arr[i])
                            cursor.execute(player_lvlup_insert_req_arr[i], player_lvlup_data_tuples_arr[i])
                        except Exception as _ex:
                            raise Exception(f"Добавляем данные о кда нетворсе и прокачке {_ex}")
                        
                except Exception as _ex:
                    raise Exception(f"Добавляем данные о том как каждый игрок сыграл {_ex}")
                #Если все удалось сохраняем изменения
                connection.commit()
        except Exception as _ex:
            #Добавить данные не удалось, выкидываем ошибку и откатываем изменения
            print(f"[class Database()] [insert_data()] {_ex}")
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
                cursor.execute(f"SELECT * FROM match WHERE match_id={match_id}")
                connection.commit()
                if connection: connection.close()
                return match_id
        except Exception as _ex:
            print(f"[class Database()] [check_match()] {_ex}")
    
    def get_startids(self):
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
                cursor.execute("SELECT MAX(mpk_id) FROM match_player_kda")
                max_index = cursor.fetchone()[0]
                self.max_index = 0 if(not max_index) else max_index
                connection.commit()
                if connection: connection.close()
                return self.max_index
        except Exception as _ex:
            print(f"[class Database()] [check_match()] {_ex}")