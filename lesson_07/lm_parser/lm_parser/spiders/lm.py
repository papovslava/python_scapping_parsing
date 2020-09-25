import scrapy
from scrapy.http import HtmlResponse
from lm_parser.items import LmParserItem
from scrapy.loader import ItemLoader


def product_page_parse(response: HtmlResponse):
    loader = ItemLoader(item=LmParserItem(), response=response)

    loader.add_xpath('_id', "//span[@slot='article']/@content")
    loader.add_xpath('title', "//h1[@slot='title']//text()")
    loader.add_xpath('photos', "//*[@slot='media-content']//@srcset")
    loader.add_xpath('chars', "//div[@class='def-list__group']//text()")
    loader.add_value('link', response.url)
    loader.add_xpath('price', "//meta[@itemprop='price']/@content")

    yield loader.load_item()


class LmSpider(scrapy.Spider):
    name = 'lm'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, params):
        self.search_query = params['query']
        self.start_urls = [f"https://leroymerlin.ru/search/?q={self.search_query}"]

    def parse(self, response: HtmlResponse):
        products_links = response.xpath('//product-card/@data-product-url').extract()
        for product_link in products_links:
            yield response.follow(product_link, callback=product_page_parse)

        next_products_page = response.xpath("//a[@class='paginator-button next-paginator-button']/@href").extract_first()
        if next_products_page:
            yield response.follow(next_products_page, callback=self.parse)
