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

@app.route('/match/<int:match_id>')
def index(match_id):
    match_ = None
    with session_factory() as session:
        match_ = session.get(MatchORM,match_id)
    return render_template('match.html', match=match_) 


if __name__ == "__main__":
    app.run(debug=False,port=3000)