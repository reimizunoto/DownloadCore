import scrapy


class AcfunSpider(scrapy.Spider):
    name = "acfun"
    allowed_domains = ["www.acfun.cn"]
    start_urls = ["https://www.acfun.cn/bangumi/aa6004319"]

    def parse(self, response):
        pass
