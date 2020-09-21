''' Selenium в Python

1) Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить данные
о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
Логин тестового ящика: study.ai_172@mail.ru
Пароль тестового ящика: NextPassword172

'''


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pymongo import MongoClient
import datetime
import time


driver = webdriver.Chrome('./materials/chromedriver.exe')


# sign in
driver.get('https://account.mail.ru/login')
elem = driver.find_element_by_name('username')
elem.send_keys('study.ai_172@mail.ru')
elem.submit()

elem = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'password')))
elem.send_keys('NextPassword172')
elem.submit()


# заходим в первое письмо
try:
  elem = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.js-letter-list-item')))
  elem.click()
except:
  print("Писем нет :(")
  exit(0)


# собираем данные, идем в следующее письмо
emails = []
all_emails_fetched = False
next_email = None
last_url = None

email_wrapper = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.thread')))
next_email_button = driver.find_element_by_css_selector('[title^="Следующее"]')

while not all_emails_fetched:
    # URL is the same, wait till content is updated
    while last_url == driver.current_url:
      time.sleep(1)
    emails.append({
      'created_at': datetime.datetime.now().isoformat(),
      'from': email_wrapper.find_element_by_css_selector('.letter-contact').text,
      'date': email_wrapper.find_element_by_css_selector('.letter__date').text,
      'subject': email_wrapper.find_element_by_css_selector('.thread__subject').text,
      'body': email_wrapper.find_element_by_css_selector('.letter-body').text,
      'url': driver.current_url
    })
    last_url = driver.current_url

    try:
      next_email_button.click()
    except:
      all_emails_fetched = True


# сохраняем собранные письма в БД
client = MongoClient('127.0.0.1', 27017)
db = client['lesson_05_db']
db_emails = db.emails
db_emails.insert_many(emails)

# sign out
driver.find_element_by_id('PH_logoutLink').click()
driver.close()