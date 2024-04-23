import re
import scrapy
import json
import execjs
import m3u8
from DownloadCore.items import HuohutvItem

class HuohutvSpider(scrapy.Spider):
    name = "huohutv"
    allowed_domains = ["www.huohutv.net"]
    start_urls = ["https://www.huohutv.net/vod-detail-id-59443.html"]

    def parse(self, response):
        # 获取视频信息
        title = response.xpath('//h2[@class="title"]/text()').extract_first().strip()
        video_list = response.xpath('//div[@class="play_source"]/div[2]/div/ul/li/a/text()').extract()
        video_url_list = response.xpath('//div[@class="play_source"]/div[2]/div/ul/li/a/@href').extract()
        video_infos = { title + '-' + key : value for key, value in zip(video_list, video_url_list)}
        item = HuohutvItem()
        base_url = 'https://www.huohutv.net'
        # 遍历每一集视频
        for key, value in video_infos.items():
            item['title'] = key
            url = base_url + value
            yield scrapy.Request(url, callback=self.parse_video, meta={'huohutv_item': item})
            break
        
    def parse_video(self, response):
        # 解析视频地址
        html = response.body.decode('utf-8')
        item = response.meta['huohutv_item']
        video_info = re.findall(r'player_data=(.*?)</script>', html)[0]
        video_info = json.loads(video_info)
        url = video_info['url']
        js_path = 'DownloadCore\\JSFiles\\huohutv\\huohutv.js'
        with open(js_path, 'r', encoding='utf-8') as f:
            ctx = execjs.compile(f.read())
        url = ctx.call('get_url', url)
        # print(url)
        yield scrapy.Request(url, callback=self.parse_m3u8, meta={'huohutv_item': item}, dont_filter=True)
        
    def parse_m3u8(self, response):
        # 获取m3u8地址文件
        item = response.meta['huohutv_item']
        url = re.findall(r"url: '(.*?)',", response.body.decode('utf-8'))[0]
        m3u8_obj = m3u8.load(url)
        play_list = m3u8_obj.segments.uri
        for play_url in play_list:
            yield scrapy.Request(play_url, callback=self.parse_ts, meta={'huohutv_item': item}, dont_filter=True)
    
    def parse_ts(self, response):
        item = response.meta['huohutv_item']
        item['video'] = response.body
        yield item