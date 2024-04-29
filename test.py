import requests
import json
import os
import random
import time
from orm import session_factory
from models import MatchORM,MatchPlayerORM,MatchPlayerNetworthORM
from dotenv import load_dotenv
from match_processing import match_full_processing
from sqlalchemy import select



with session_factory() as session:
    stmt = select(MatchPlayerORM).where(MatchPlayerORM.hero_id == 123)
    data = session.execute(stmt).scalars()
    player_pbt_data = []
    for player in data:
        plist = player.mp_networth.purchase_by_time
        pbt_data = {0:[]}
        for item in plist:
            time = list(plist[item].keys())[0]
            if(int(time) <= 20):
                pbt_data[0].append({time:plist[item][time]})
            else:
                current_time = ((int(time) // 300) + 1) * 5
                if(not pbt_data.get(current_time)):
                    pbt_data[current_time] = []
                pbt_data[current_time].append({time:plist[item][time]})
        player_pbt_data.append(pbt_data)
    
    item_by_time = {}
    for ppd in player_pbt_data:
        for i in list(ppd.keys()):
            if(ppd.get(i)):
                for item in ppd[i]:
                    key = list(item.keys())[0]
                    item_name = item[key]
                    if(item_by_time.get(i) == None):
                        item_by_time[i] = {}
                    if item_by_time.get(i).get(item_name) == None:
                        item_by_time[i][item_name] = 1
                    else:
                        item_by_time[i][item_name] += 1
    
    filtered_dict = {key: {k: v for k, v in subdict.items() if v >= 10} for key, subdict in item_by_time.items()}
    
    for line in filtered_dict:
        print(f'{line}: {filtered_dict[line]}\n')