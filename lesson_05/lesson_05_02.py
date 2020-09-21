''' Selenium в Python

2) Написать программу, которая собирает «Хиты продаж» с сайта техники mvideo и складывает данные в БД.
Магазины можно выбрать свои. Главный критерий выбора: динамически загружаемые товары

'''


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
from pymongo import MongoClient


driver = webdriver.Chrome('./materials/chromedriver.exe')


driver.get('https://www.mvideo.ru/')
all_products_fetched = False
galleries = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.gallery-layout')))

for gallery in galleries:
  try:
    title = gallery.find_element_by_css_selector('.gallery-title-wrapper')
    if title and title.text == 'Хиты продаж':
      gallery.click()
      next_slide_button = gallery.find_element_by_css_selector('.next-btn.sel-hits-button-next')
      while next_slide_button.is_displayed():
        next_slide_button.click()
      products = gallery.find_elements_by_css_selector('.sel-product-tile-title')
      hits_data = [json.loads(product.get_attribute('data-product-info')) for product in products]
  except:
    pass

# сохраняем собранные письма в БД
client = MongoClient('127.0.0.1', 27017)
db = client['lesson_05_db']
db_hits = db.hits
db_hits.insert_many(hits_data)

# end session
driver.close()