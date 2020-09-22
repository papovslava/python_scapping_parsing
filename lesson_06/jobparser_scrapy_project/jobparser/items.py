# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from urllib.parse import urlparse


class JobparserItem(scrapy.Item):
  # define the fields for your item here like:
  title = scrapy.Field()
  link = scrapy.Field()
  hostname = scrapy.Field()
  salary = scrapy.Field()
  min_salary = scrapy.Field()
  max_salary = scrapy.Field()
  currency = scrapy.Field()

