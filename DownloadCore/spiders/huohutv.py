import scrapy


class HuohutvSpider(scrapy.Spider):
    name = "huohutv"
    allowed_domains = ["www.huohutv.net"]
    start_urls = ["https://www.huohutv.net/"]

    def parse(self, response):
        pass
