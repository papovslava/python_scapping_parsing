import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class HhruSpider(scrapy.Spider):
  name = 'hhru'
  allowed_domains = ['hh.ru']
  start_urls = ['https://izhevsk.hh.ru/search/vacancy?L_save_area=true&clusters=true&enable_snippets=true&text=python&showClusters=true']

  def parse(self, response:HtmlResponse):
    vacancies = response.css("div.vacancy-serp-item__row_header a.bloko-link::attr(href)").extract()
    for vacancy in vacancies:
      yield response.follow(vacancy,callback=self.vacancy_parse)

    next_page = response.css("a.HH-Pager-Controls-Next::attr(href)").extract_first()
    if next_page:
      yield response.follow(next_page, callback=self.parse)


  def vacancy_parse(self, response:HtmlResponse):
    title = response.css('.vacancy-title > h1').extract_first()
    salary = response.css('.vacancy-salary').extract_first()
    link = response.url
    hostname = response.url

    yield JobparserItem(title=title, salary=salary, link=link, hostname=hostname)