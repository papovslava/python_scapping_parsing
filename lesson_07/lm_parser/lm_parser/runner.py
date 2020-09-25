from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from lm_parser.spiders.lm import LmSpider
from lm_parser import settings

if __name__ == '__main__':
  crawler_settings = Settings()
  crawler_settings.setmodule(settings)

  process = CrawlerProcess(settings=crawler_settings)
  process.crawl(LmSpider, {'query':'фанера'})
  process.crawl(LmSpider, {'query':'дсп'})

  process.start()