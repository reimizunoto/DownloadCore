import scrapy
import re
from html2text import html2text
from DownloadCore.items import BigeeItem

class BigeeSpider(scrapy.Spider):
    name = "bigee"
    allowed_domains = ["www.bigee.cc"]
    start_urls = ["https://www.bigee.cc/book/4184"]

    def parse(self, response):
        title = response.xpath('//div[@class="info"]/h1/text()').extract_first()
        title_detail = response.xpath('//div[@class="listmain"]/dl/dd/a/text()').extract()
        novel_url = response.xpath('//div[@class="listmain"]/dl/dd/a/@href').extract()
        novel_info = {title+'-'+key:value for key, value in zip(title_detail, novel_url)}
        base_url = 'https://www.bigee.cc'
        item = BigeeItem()
        for key, value in novel_info.items():
            url = base_url + value
            item['title'] = key
            # print(key, url)
            yield scrapy.Request(url=url, callback=self.parse_novel, meta={'bigee_title': item})
            break
            
    def parse_novel(self, response):
        item = response.meta['bigee_title']
        html = response.body.decode('utf-8')
        novel = re.findall(r'<div id="chaptercontent" class="Readarea ReadAjax_content">(.*?)请收藏本站', html, re.S)[0].strip()
        item['novel'] = html2text(novel)
        yield item