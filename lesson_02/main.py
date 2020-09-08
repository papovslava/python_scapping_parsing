'''

Необходимо собрать информацию о вакансиях на вводимую должность
(используем input или через аргументы) с сайтов Superjob и HH.
Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).

Получившийся список должен содержать в себе минимум:
- Наименование вакансии.
- Предлагаемую зарплату (отдельно минимальную и максимальную).
- Ссылку на саму вакансию.
- Сайт, откуда собрана вакансия.

По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
Структура должна быть одинаковая для вакансий с обоих сайтов.
Общий результат можно вывести с помощью dataFrame через pandas.

'''

from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import re
# import pandas as pd

def parse_compensation(comp_str):
  result = {
    'from': 0,
    'to': 0,
    'currency': 'NA'
  }
  if comp_str == None:
    return result
  comp_str = comp_str.getText()
  #comp_str = comp_str.replace('\\xa', '')
  delim = comp_str.rfind(' ')
  result['currency'] = comp_str[delim+1:]
  comp_str = comp_str[:delim]

  delim = comp_str.find('от')
  if delim > -1:
    result['from'] = int(re.sub('[^0-9]','', comp_str[3:]))
  delim = comp_str.find('до')
  if delim > -1:
    result['to'] = int(re.sub('[^0-9]','', comp_str[3:]))
  delim = comp_str.find('-')
  if delim > -1:
    result['from'] = int(re.sub('[^0-9]','', comp_str[:delim]))
    result['to'] = int(re.sub('[^0-9]','', comp_str[delim:]))

  return result


search_URL = 'https://hh.ru/search/vacancy'
payload = {'text': 'python+developer'}
headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 '
                'Safari/537.36'}

results = []
current_page = 0

while True:
  payload.update({'page': current_page})
  payload_str = "&".join("%s=%s" % (k, v) for k, v in payload.items())
  html = requests.get(search_URL, params=payload_str, headers=headers)
  soup = bs(html.text, 'html.parser')

  vacancies = soup.find_all('div', {'class': 'vacancy-serp-item'})
  for vacancy in vacancies:
    title_elem = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
    compensation_elem = vacancy.find('div', {'class': 'vacancy-serp-item__sidebar'})
    results.append({
      'title': title_elem.getText(),
      'compensation': parse_compensation(compensation_elem),
      'link': title_elem.attrs['href'],
      'source': 'hh.ru'
    })

  if soup.find('a', {'data-qa': 'pager-next'}) == None: break
  current_page += 1

# df = pd.read_json(results)

pprint(results)
# pprint(df)
pprint()
