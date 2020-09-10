'''
1) Развернуть у себя на компьютере/виртуальной машине/хостинге
MongoDB и реализовать функцию, записывающую собранные вакансии
в созданную БД
2) Написать функцию, которая производит поиск и выводит на экран
вакансии с заработной платой больше введенной суммы. Поиск по двум
полям (мин и макс зарплату)
3) Написать функцию, которая будет добавлять в вашу базу данных
только новые вакансии с сайта
'''


from pymongo import MongoClient
from pprint import pprint
from grabber import get_vacancies_hh

# от min<limit и до бесконечности (0)
# от бесконечности (0) и до limit < max
# min < limit & limit < max
def find_vacancy_over(limit):
  for vacancy in db_vacancies.find({}):
    max = vacancy['compensation']['to']
    min = vacancy['compensation']['from']
    USD_RUR = 75
    KZT_RUR = 0.176906
    if min == 0 and max == 0: continue
    if vacancy['compensation']['currency'] == 'USD':
      min *= USD_RUR
      max *= USD_RUR
    if vacancy['compensation']['currency'] == 'KZT':
      min *= KZT_RUR
      max *= KZT_RUR
    if (min < limit and limit < max) or (min <= limit and max == 0):
      pprint(vacancy)


def add_vacancies():
  vacancies = get_vacancies_hh()
  amount_inserted = 0
  for vacancy in vacancies:
    if db_vacancies.count({'source_id': vacancy['source_id']}): continue
    db_vacancies.insert_one(vacancy)
    amount_inserted += 1

  print(f'{amount_inserted} vacancies out of {len(vacancies)} have been inserted')


client = MongoClient('127.0.0.1', 27017)
db = client['lesson_03_db']
db_vacancies = db.vacancies

add_vacancies()
find_vacancy_over(250000)

pass