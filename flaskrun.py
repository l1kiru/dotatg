import json
from datetime import datetime
from flask import Flask, render_template, url_for
from orm import session_factory
from models import MatchORM

app = Flask(__name__)

def timestamp_to_days(timestamp):
    return (datetime.now() - datetime.fromtimestamp(timestamp)).days 

app.jinja_env.filters['timestamp_to_days'] = timestamp_to_days

def networth_round(number):
    return round(number / 1000, 1)

app.jinja_env.filters['networth_round'] = networth_round

def get_game_mode(id):
    print(f"id: {id}")
    with open("dota/game_mode.json") as file_:
        data = json.load(file_)
    id = str(id)
    return data[id]['name']

app.jinja_env.filters['get_game_mode'] = get_game_mode

def get_heroes(id):
    with open("dota/heroes.json") as file_:
        data = json.load(file_)
    hero_name = data[f'{id}']['name']
    short_name = hero_name.split("npc_dota_hero_")[1]
    return short_name

app.jinja_env.filters['get_heroes'] = get_heroes

def get_item(item):
    key = list(item.keys())[0]
    with open("dota/item_ids.json") as file_:
        data = json.load(file_)
    return data[f'{item[key]}']
 
app.jinja_env.filters['get_item'] = get_item

def get_ability(id):
    with open("dota/ability_ids.json") as file_:
        data = json.load(file_)
    return data[f'{id}']

app.jinja_env.filters['get_ability'] = get_ability

def get_ability_value(ability):
    if(ability):
        with open("dota/abilities.json") as file_:
            data = json.load(file_)
        return data[ability]
    else:
        return None

app.jinja_env.filters['get_ability_value'] = get_ability_value

def get_region(region_id):
    with open("dota/region.json") as file_:
        data = json.load(file_)
    return data[f"{region_id}"]

app.jinja_env.filters['get_region'] = get_region

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

app.jinja_env.filters['purchase_in_game'] = purchase_in_game

def max_value(puring):
    return max(max(pur.keys()) for pur in puring)

app.jinja_env.filters['max_value'] = max_value

def get_pur_name(item):
    key0 = list(item.keys())[0]
    return item[key0].split("item_")[1]

app.jinja_env.filters['get_pur_name'] = get_pur_name

def get_pur_time(item):
    total_seconds = int(list(item.keys())[0])
    is_negative = total_seconds < 0
    total_seconds = abs(total_seconds)
    hours = total_seconds // 3600
    remaining_seconds = total_seconds % 3600
    minutes = remaining_seconds // 60
    seconds = remaining_seconds % 60
    if hours > 0:
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    elif is_negative:
        return f"-{minutes:02}:{seconds:02}"
    else:
        return f"{minutes:02}:{seconds:02}"

app.jinja_env.filters['get_pur_time'] = get_pur_time

@app.route('/match/<int:match_id>')
def index(match_id):
    match_ = None
    with session_factory() as session:
        match_ = session.get(MatchORM,match_id)
    return render_template('match.html', match=match_) 


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=3000)