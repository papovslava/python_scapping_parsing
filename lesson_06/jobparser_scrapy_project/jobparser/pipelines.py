# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re


class JobparserPipeline:
  def __init__(self):
    client = MongoClient('localhost',27017)
    self.mongobase = client.lesson_06

  def process_item(self, item, spider):
    item['title'] = BeautifulSoup(item['title'], features="lxml").get_text()
    parsed_uri = urlparse(item['link'])
    item['hostname'] = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    item['salary'] = self.process_salary(BeautifulSoup(item['salary'], features="lxml").get_text(), spider.name)
    vacancy = dict(item)
    collection = self.mongobase[spider.name]
    collection.insert_one(vacancy)
    return item


  def process_salary(self, comp_str, spider_name):
    result = {
      'from': None,
      'to': None,
      'currency': None
    }

    if comp_str == 'з/п не указана' or comp_str == 'По договорённости': return result

    comp_str = re.sub(' ', ' ', comp_str)
    comp_str = re.sub('\/месяц|\/мес| на руки', '', comp_str)

    delim = comp_str.rfind(' ')
    result['currency'] = comp_str[delim + 1:]
    comp_str = re.sub(' ', '', comp_str[:delim])

    from_comp = re.findall('от (\d{1,})', comp_str)
    to_comp = re.findall('до (\d{1,})', comp_str)

    if len(from_comp): result['from'] = int(from_comp[0])
    if len(to_comp): result['from'] = int(from_comp[0])

    if spider_name == 'superjobru':
      from_to_comp = re.findall('(\d{1,})—(\d{1,})', comp_str)
      if len(from_to_comp):
        result['from'] = int(from_to_comp[0][0])
        result['to'] = int(from_to_comp[0][1])
      pass

    return result