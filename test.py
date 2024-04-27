import requests
import json
import os
import random
import time
from orm import session_factory
from models import MatchORM,MatchPlayerORM,MatchPlayerNetworthORM


def purchase_in_game(match_id):
    with session_factory() as session:
        match_ = session.get(MatchORM,match_id)
        player_pbt_data = []
        for player in match_.players:
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
    return player_pbt_data

puring = purchase_in_game('7698921185')

def max_value(puring):
    return max(max(pur.keys()) for pur in puring)

for pur in puring[:1]:
    for key in pur:
        for item in pur[key]:
            key0 = list(item.keys())[0]
            print(key0)
            #print(item[key0])