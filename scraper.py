import scrapy

from scrapy.http import Request
from scrapy.spiders import Spider
from scrapy.selector import Selector


class Spider(Spider):
    name = "baby_name_spider"
    start_urls = ["https://www.babynames.com/"]
    result = {'male': [], 'female': []}

    def parse(self, response):
        hxs = Selector(response)
        alphabets = hxs.xpath('//*[@id="headerletters"]/ul/li/a').extract()

        for alphabet in alphabets:
            link = alphabet.split('"')[1::2][0]
            url = response.url[0:-1] + link
            yield Request(url, callback=self.parse_page)

        self.crawler.signals.connect(self.write_csv, signal=scrapy.signals.spider_idle)

    def parse_page(self, response):
        hxs = Selector(response)
        male_names = Selector(response).xpath('//ul[@class="searchresults"]/li/a[@class="M"]/text()').extract()
        for male_name in male_names:
            self.result['male'].append(male_name)

        female_names = Selector(response).xpath('//ul[@class="searchresults"]/li/a[@class="F"]/text()').extract()
        for female_name in female_names:
            self.result['female'].append(female_name)

    def write_csv(self):
        self.result['male'].sort()
        self.result['female'].sort()

        print(self.result)
