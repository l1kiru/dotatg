import requests
import json
import os
import random
import time

def download_file(url, filename):
    # Проверяем, существует ли уже файл с таким именем
    if os.path.exists(f'static/images/items/{filename}.png'):
        print(f"Файл {filename}.png уже существует.")
        return False

    # Создаем список различных User-Agent'ов для имитации поведения разных браузеров
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/97.0.1072.76 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36",
    ]

    headers = {'User-Agent': random.choice(user_agents)}
    time.sleep(random.uniform(0.05, 0.2))  # Задержка
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open(f'static/images/items/{filename}.png', 'wb') as f:
            f.write(response.content)
        print("Файл успешно сохранен как:", filename)
        return False
    else:
        print("Файл не удалось сохранить:", filename)
        return filename

with open("dota/item_ids.json") as file_:
    items = json.load(file_)
    names = ''
    for item_id in items:
        item_name = items[item_id]
        #src=f"https://cdn.steamstatic.com/apps/dota2/images/dota_react/abilities/{ability_name}.png"
        src=f"https://cdn.dota2.com/apps/dota2/images/items/{item_name}_lg.png"
        if(not 'special_bonus_' in item_name):
            res = download_file(src, item_name)
            if res:
                names += f'{res}\n'
        else:
            print(f"Файл {item_name} был пропущен")
            pass
    with open('names.txt', 'w') as f:
        f.write(names)
