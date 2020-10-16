import scrapy


class CrawlerSpider(scrapy.Spider):
    name = 'crawler'
    allowed_domains = ['https://firststop.sos.nd.gov/search/business']
    start_urls = ['http://https://firststop.sos.nd.gov/search/business/']

    def parse(self, response):
        pass
