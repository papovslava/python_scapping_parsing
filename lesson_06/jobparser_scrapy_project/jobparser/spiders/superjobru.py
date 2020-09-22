import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SuperjobruSpider(scrapy.Spider):
    name = 'superjobru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response: HtmlResponse):
        vacancies = response.css("a.icMQ_._6AfZ9._2JivQ._1UJAN::attr(href)").extract()
        for vacancy in vacancies:
            yield response.follow(vacancy, callback=self.vacancy_parse)

        next_page = response.css("a.icMQ_._1_Cht._3ze9n.f-test-button-dalshe.f-test-link-Dalshe::attr(href)").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def vacancy_parse(self, response: HtmlResponse):
        title = response.css('h1._3mfro.rFbjy.s1nFK._2JVkc').extract_first()
        salary = response.css('._1OuF_.ZON4b').extract_first()
        link = response.url
        hostname = response.url

        yield JobparserItem(title=title, salary=salary, link=link, hostname=hostname)
