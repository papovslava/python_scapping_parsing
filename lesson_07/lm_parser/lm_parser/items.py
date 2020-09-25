# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst

# название;
# все фото;
# параметры товара в объявлении;
# ссылка;
# цена.


def price_to_float(value):
    return float(value.replace(' ', ''))

class LmParserItem(scrapy.Item):
    _id = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    chars = scrapy.Field()
    link = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(price_to_float), output_processor=TakeFirst())
