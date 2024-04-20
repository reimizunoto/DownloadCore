import scrapy
from DownloadCore.items import IyhdmmItem

class IyhdmmSpider(scrapy.Spider):
    name = "iyhdmm"
    allowed_domains = ["iyhdmm.com"]
    start_urls = ["https://www.iyhdmm.com/showp/19255.html"]

    def parse(self, response):
        title = response.xpath('//div[@class="rate r"]/h1/text()').extract_first()
        title_detail = response.xpath('//*[@id="main0"]/div[2]/ul/li/a/text()').extract()
        link = response.xpath('//*[@id="main0"]/div[2]/ul/li/a/@href').extract()
        video_info = {title + "-" + key: value for key, value in zip(title_detail, link)}
        base_url = "https://www.iyhdmm.com"
        for key, value in video_info.items():
            url = base_url + value
            item = IyhdmmItem()
            item['title'] = key
            print(key, url)
            yield scrapy.Request(url=url, callback=self.parse_video_ts, meta={'iyhdmm_item': item}, dont_filter=True)

    def parse_video_ts(self, response):
        
        item = response.meta['iyhdmm_item']