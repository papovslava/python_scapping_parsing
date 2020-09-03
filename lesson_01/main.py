# 1. Посмотреть документацию к API GitHub,
# разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.

import requests
import json


task_01_api_endpoint_url = 'https://api.github.com/users/papovslava/repos'
params = {'Accept': 'application/vnd.github.v3+json', 'User-Agent': 'GeekBrains study app'}
response = requests.get(task_01_api_endpoint_url, params)

if response.ok:
  with open('task_01.json', 'w') as outfile:
    json.dump(response.text, outfile)

# 2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis).
# Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию.
# Ответ сервера записать в файл.

API_KEY = '573e8f21e5afb794dc0f974fc3e7b7db'
task_02_api_endpoint_url = 'http://ws.audioscrobbler.com/2.0/?method=chart.gettopartists&format=json&api_key='
response = requests.get(task_02_api_endpoint_url + API_KEY)

if response.ok:
  with open('task_02.json', 'w') as outfile:
    json.dump(response.text, outfile)