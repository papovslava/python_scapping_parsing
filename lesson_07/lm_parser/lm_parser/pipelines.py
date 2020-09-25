# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline
import scrapy
import hashlib
from scrapy.utils.python import to_bytes

class LmParserPipeline:
  def __init__(self):
    client = MongoClient('localhost', 27017)
    self.mongo_base = client.lm_parser

  def process_item(self, item, spider):
    chars = item['chars']
    chars = [char for char in [char.strip() for char in chars] if len(char)]
    item['chars'] = dict(zip(chars[0::2], chars[1::2]))
    collection = self.mongo_base[spider.name]
    collection.update_one({"_id": item['_id']}, {'$set': item}, upsert=True)
    return item

class LmPhotosPipeline(ImagesPipeline):
  def get_media_requests(self, item, info):
    photos_links = item['photos'][::5] # take only 2000x2000 photos

    for photo_link in photos_links:
      try:
        yield scrapy.Request(photo_link, meta={'subfolder': f"{info.spider.search_query}/{item['_id']}"})
      except:
        pass

  def file_path(self, request, response=None, info=None):
    image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
    return f"full/{request.meta.get('subfolder', '')}/{image_guid}.jpg"

  def item_completed(self, results, item, info):
    if results:
      item['photos'] = [itm[1] for itm in results if itm[0]]
    return item