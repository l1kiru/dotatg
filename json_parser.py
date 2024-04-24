import os
import bz2
import json
import requests
from dotenv import load_dotenv

load_dotenv()
op_api_key= os.getenv('OPENDOTAAPIKEY')

def parse_replay(match_id):
    requests.post(url=f"https://api.opendota.com/api/request/{match_id}?api_key={op_api_key}")
    req = requests.get(url=f"https://api.opendota.com/api/matches/{match_id}?api_key={op_api_key}").json()
    replay_link = f"http://replay{req['cluster']}.valve.net/570/{match_id}_{req['replay_salt']}.dem.bz2" if (req.get('replay_salt')) else ''
    if(replay_link and not requests.get(replay_link).status_code == 404):
        req = requests.get(replay_link)
        with open(f"match{match_id}-replay.dem.bz2", 'wb') as f: 
            f.write(req.content)
        with open(f"match{match_id}-replay.dem", 'wb') as output_file, bz2.BZ2File(f'match{match_id}-replay.dem.bz2', 'rb') as input_file:
            output_file.write(input_file.read()) 
        os.remove(f'match{match_id}-replay.dem.bz2')
        os.system(f'curl 127.0.0.1:5600 --data-binary "@match{match_id}-replay.dem" > {match_id}.jsonlinesines')
        os.remove(f"match{match_id}-replay.dem")

        chname_slot = {}
        movement = [{},{},{},{},{},{},{},{},{},{}]
        lhts = [{},{},{},{},{},{},{},{},{},{}]
        networth = [{},{},{},{},{},{},{},{},{},{}]
        combatlogp_slot = {}
        purchase_log = [{},{},{},{},{},{},{},{},{},{}]
        combatlogd_slot = {}
        kills_log = [{},{},{},{},{},{},{},{},{},{}]
        with open(f"{match_id}.jsonlinesines") as file_:
            counter = 0
            for line in file_.buffer:
                line_ =  json.loads(line.decode('utf-8'))
                if(line_['type'] == "interval"):
                    if(line_['time'] >= 0):
                        match(line_['slot']): 
                            case 0:
                                result = parse_replay_interval(line=line_,counter=counter,chname_slot=chname_slot,movement=movement,lhts=lhts,networth=networth)
                                chname_slot, movement, lhts, networth = result['chname_slot'], result['movement'], result['lhts'], result['networth']
                            case 1:
                                result = parse_replay_interval(line=line_,counter=counter,chname_slot=chname_slot,movement=movement,lhts=lhts,networth=networth)
                                chname_slot, movement, lhts, networth = result['chname_slot'], result['movement'], result['lhts'], result['networth']
                            case 2:
                                result = parse_replay_interval(line=line_,counter=counter,chname_slot=chname_slot,movement=movement,lhts=lhts,networth=networth)
                                chname_slot, movement, lhts, networth = result['chname_slot'], result['movement'], result['lhts'], result['networth']
                            case 3:
                                result = parse_replay_interval(line=line_,counter=counter,chname_slot=chname_slot,movement=movement,lhts=lhts,networth=networth)
                                chname_slot, movement, lhts, networth = result['chname_slot'], result['movement'], result['lhts'], result['networth']
                            case 4:
                                result = parse_replay_interval(line=line_,counter=counter,chname_slot=chname_slot,movement=movement,lhts=lhts,networth=networth)
                                chname_slot, movement, lhts, networth = result['chname_slot'], result['movement'], result['lhts'], result['networth']
                            case 5:
                                result = parse_replay_interval(line=line_,counter=counter,chname_slot=chname_slot,movement=movement,lhts=lhts,networth=networth)
                                chname_slot, movement, lhts, networth = result['chname_slot'], result['movement'], result['lhts'], result['networth']
                            case 6:
                                result = parse_replay_interval(line=line_,counter=counter,chname_slot=chname_slot,movement=movement,lhts=lhts,networth=networth)
                                chname_slot, movement, lhts, networth = result['chname_slot'], result['movement'], result['lhts'], result['networth']
                            case 7:
                                result = parse_replay_interval(line=line_,counter=counter,chname_slot=chname_slot,movement=movement,lhts=lhts,networth=networth)
                                chname_slot, movement, lhts, networth = result['chname_slot'], result['movement'], result['lhts'], result['networth']
                            case 8:
                                result = parse_replay_interval(line=line_,counter=counter,chname_slot=chname_slot,movement=movement,lhts=lhts,networth=networth)
                                chname_slot, movement, lhts, networth = result['chname_slot'], result['movement'], result['lhts'], result['networth']
                            case 9:
                                result = parse_replay_interval(line=line_,counter=counter,chname_slot=chname_slot,movement=movement,lhts=lhts,networth=networth)
                                chname_slot, movement, lhts, networth = result['chname_slot'], result['movement'], result['lhts'], result['networth']
                                counter += 1
                if(line_['type'] == "DOTA_COMBATLOG_PURCHASE"):
                    targetname = line_['targetname'].lower().replace('_','')[11:]
                    if (targetname not in combatlogp_slot):
                        combatlogp_slot[targetname] = len(combatlogp_slot)
                    match(combatlogp_slot[targetname]):
                        case 0:
                            cscl = len(purchase_log[combatlogp_slot[targetname]])
                            if not line_['valuename'] == "item_ward_dispenser":
                                purchase_log[combatlogp_slot[targetname]][cscl] =  {line_['time']: line_['valuename']}
                        case 1:
                            cscl = len(purchase_log[combatlogp_slot[targetname]])
                            if not line_['valuename'] == "item_ward_dispenser":
                                purchase_log[combatlogp_slot[targetname]][cscl] =  {line_['time']: line_['valuename']}
                        case 2:
                            cscl = len(purchase_log[combatlogp_slot[targetname]])
                            if not line_['valuename'] == "item_ward_dispenser":
                                purchase_log[combatlogp_slot[targetname]][cscl] =  {line_['time']: line_['valuename']}
                        case 3:
                            cscl = len(purchase_log[combatlogp_slot[targetname]])
                            if not line_['valuename'] == "item_ward_dispenser":
                                purchase_log[combatlogp_slot[targetname]][cscl] =  {line_['time']: line_['valuename']}
                        case 4:
                            cscl = len(purchase_log[combatlogp_slot[targetname]])
                            if not line_['valuename'] == "item_ward_dispenser":
                                purchase_log[combatlogp_slot[targetname]][cscl] =  {line_['time']: line_['valuename']}
                        case 5:
                            cscl = len(purchase_log[combatlogp_slot[targetname]])
                            if not line_['valuename'] == "item_ward_dispenser":
                                purchase_log[combatlogp_slot[targetname]][cscl] =  {line_['time']: line_['valuename']}
                        case 6:
                            cscl = len(purchase_log[combatlogp_slot[targetname]])
                            if not line_['valuename'] == "item_ward_dispenser":
                                purchase_log[combatlogp_slot[targetname]][cscl] =  {line_['time']: line_['valuename']}
                        case 7:
                            cscl = len(purchase_log[combatlogp_slot[targetname]])
                            if not line_['valuename'] == "item_ward_dispenser":
                                purchase_log[combatlogp_slot[targetname]][cscl] =  {line_['time']: line_['valuename']}
                        case 8:
                            cscl = len(purchase_log[combatlogp_slot[targetname]])
                            if not line_['valuename'] == "item_ward_dispenser":
                                purchase_log[combatlogp_slot[targetname]][cscl] =  {line_['time']: line_['valuename']}
                        case 9:
                            cscl = len(purchase_log[combatlogp_slot[targetname]])
                            if not line_['valuename'] == "item_ward_dispenser":
                                purchase_log[combatlogp_slot[targetname]][cscl] =  {line_['time']: line_['valuename']}
                if(line_['type'] == "DOTA_COMBATLOG_DEATH"):
                    if("hero" in line_['targetname'] and "hero" in line_['sourcename']):
                        attackname = line_['sourcename'].lower().replace('_','')[11:]
                        if (attackname not in combatlogd_slot):
                            combatlogd_slot[attackname] = len(combatlogd_slot)
                        match(combatlogd_slot[attackname]):
                            case 0:
                                kills_log = parse_replay_death_log(who=combatlogd_slot[attackname],line=line_,kills_log=kills_log,combatlogd_slot=combatlogd_slot)
                            case 1: 
                                kills_log = parse_replay_death_log(who=combatlogd_slot[attackname],line=line_,kills_log=kills_log,combatlogd_slot=combatlogd_slot)
                            case 2:
                                kills_log = parse_replay_death_log(who=combatlogd_slot[attackname],line=line_,kills_log=kills_log,combatlogd_slot=combatlogd_slot)
                            case 3:
                                kills_log = parse_replay_death_log(who=combatlogd_slot[attackname],line=line_,kills_log=kills_log,combatlogd_slot=combatlogd_slot)
                            case 4:
                                kills_log = parse_replay_death_log(who=combatlogd_slot[attackname],line=line_,kills_log=kills_log,combatlogd_slot=combatlogd_slot)
                            case 5:
                                kills_log = parse_replay_death_log(who=combatlogd_slot[attackname],line=line_,kills_log=kills_log,combatlogd_slot=combatlogd_slot)
                            case 6: 
                                kills_log = parse_replay_death_log(who=combatlogd_slot[attackname],line=line_,kills_log=kills_log,combatlogd_slot=combatlogd_slot)
                            case 7:
                                kills_log = parse_replay_death_log(who=combatlogd_slot[attackname],line=line_,kills_log=kills_log,combatlogd_slot=combatlogd_slot)
                            case 8:
                                kills_log = parse_replay_death_log(who=combatlogd_slot[attackname],line=line_,kills_log=kills_log,combatlogd_slot=combatlogd_slot)
                            case 9:
                                kills_log = parse_replay_death_log(who=combatlogd_slot[attackname],line=line_,kills_log=kills_log,combatlogd_slot=combatlogd_slot)
        os.remove(f"{match_id}.jsonlinesines")
        return parse_replay_get_result(chname_slot=chname_slot,movement=movement,lhts=lhts,networth=networth,
                            combatlogp_slot=combatlogp_slot,purchase_log= purchase_log,
                            combatlogd_slot=combatlogd_slot,kills_log=kills_log)
    
    else:
        return None

def parse_replay_interval(line,counter,chname_slot,movement,lhts,networth):
    unit_str = line['unit'].lower().replace('_','')[13:]
    if(unit_str not in chname_slot):
        chname_slot[unit_str] = line['slot']
    movement[line['slot']][counter] = {'x' : line['x'], 'y' : line['y']}
    if(line['time'] % 60 == 0):
        lhts[line['slot']][counter] = {'lh' : line['lh']}
        networth[line['slot']][counter] = {'networth' : line['networth']}
    return {'chname_slot':chname_slot,'movement':movement,'lhts':lhts,'networth':networth}

def parse_replay_death_log(who,line,kills_log,combatlogd_slot):
    targetname = line['targetname'].lower().replace('_','')[11:]
    if (targetname not in combatlogd_slot):
        combatlogd_slot[targetname] = len(combatlogd_slot)
    cscl = len(kills_log[who])
    kills_log[who][cscl] =  {line['time']: line['targetname']}
    return kills_log

def parse_replay_get_result(chname_slot,movement,lhts,networth,combatlogp_slot,purchase_log,combatlogd_slot,kills_log):
    parsed_data = {}
    for i in range(10):
        chname = [key for key in chname_slot if chname_slot[key] == i][0]
        parsed_data[chname] = {}
        parsed_data[chname]['movement'] = movement[i]
        parsed_data[chname]['lhts'] = lhts[i]
        parsed_data[chname]['networth'] = networth[i]
        chname_from_clsp = combatlogp_slot[chname]
        parsed_data[chname]['purchase_log'] = purchase_log[chname_from_clsp]
        chname_from_clsd = combatlogd_slot[chname]
        parsed_data[chname]['kills_log'] = kills_log[chname_from_clsd]
    return parsed_data
            