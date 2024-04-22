import scrapy
from DownloadCore.items import IyhdmmItem
import execjs
import requests
import json
import m3u8

class IyhdmmSpider(scrapy.Spider):
    name = "iyhdmm"
    allowed_domains = ["iyhdmm.com"]
    start_urls = ["https://www.iyhdmm.com/showp/23420.html"]

    def parse(self, response):
        title = response.xpath('//div[@class="rate r"]/h1/text()').extract_first()
        title_detail = response.xpath('//*[@id="main0"]/div[2]/ul/li/a/text()').extract()
        link = response.xpath('//*[@id="main0"]/div[2]/ul/li/a/@href').extract()
        video_info = {title + "-" + key: value for key, value in zip(title_detail, link)}
        base_url = "https://www.iyhdmm.com"
        execjs_path = 'DownloadCore\\JSFiles\\iyhdmm\\iyhdmm.js'
        with open(execjs_path, 'r', encoding='utf-8') as f:
            js_code = f.read()
        ctx = execjs.compile(js_code)
        for key, value in video_info.items():
            url = base_url + value
            item = IyhdmmItem()
            item['title'] = key
            # <------------------------------------------------------------------->
            # 获取m3u8地址
            session = requests.session()
            hearder = {
                'Host': 'www.iyhdmm.com',
                'Connection': 'keep-alive',
                'Accept': '*/*',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
                'sec-ch-ua-platform': "Windows",
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Referer': url,
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept-Language': 'zh,zh-CN;q=0.9',
            }
            session.headers.update(hearder)
            session.get(url)
            print(key, url)
            code_url = base_url + ctx.call('setPlayFrm', url)
            print(code_url)
            response = session.get(code_url)
            code = response.text
            m3u8_url_list = json.loads(ctx.call('_0xc6b4e6', code))
            m3u8_url = base_url + m3u8_url_list['purl'] + m3u8_url_list['vurl']
            print(m3u8_url)
            # <-------------------------------------------------------------------->
            # 获取m3u8文件
            m3u8_url = ctx.call('GetUrlQuery', m3u8_url)
            print(m3u8_url)
            yield scrapy.Request(url=m3u8_url, callback=self.parse_m3u8, meta={'iyhdmm_item': item}, dont_filter=True)
            break

    def parse_m3u8(self, response):
        item = response.meta['iyhdmm_item']
        temp = response.text.split('\n')[2]
        index = response.request.url.find('com') + 3
        base_url = response.request.url[:index]
        m3u8_url = base_url + temp
        print(m3u8_url)
        m3u8_obj = m3u8.load(m3u8_url)
        ts_list = m3u8_obj.segments.uri
        for ts in ts_list:
            ts_url = base_url + ts
            yield scrapy.Request(url=ts_url, callback=self.parse_ts, meta={'iyhdmm_item': item}, dont_filter=True)

    def parse_ts(self, response):
        item = response.meta['iyhdmm_item']
        item['video'] = response.body
        yield item