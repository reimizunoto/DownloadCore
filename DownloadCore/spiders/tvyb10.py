import scrapy
import re
import json
import execjs
import m3u8
from DownloadCore.items import Tvyb10Item

class Tvyb10Spider(scrapy.Spider):
    name = "tvyb10"
    allowed_domains = ["www.tvyb10.com"]
    start_urls = ["http://www.tvyb10.com/vod/detail/id/168492.html"]

    def parse(self, response):
        title = response.xpath('//div[@class="myui-content__detail"]/h1/text()').extract_first()
        title_detail = response.xpath('//div[@class="myui-panel_bd clearfix"]/ul/li/a/text()').extract()
        video_url = response.xpath('//div[@class="myui-panel_bd clearfix"]/ul/li/a/@href').extract()
        video_info = {title + '_' + key : value for key, value in zip(title_detail, video_url)}
        base_url = 'http://www.tvyb10.com'
        item = Tvyb10Item()
        for key, value in video_info.items():
            url = base_url + value
            item['title'] = key
            yield scrapy.Request(url, callback=self.parse_video, meta={'tvyb10_title': item})
            break
        
    def parse_video(self, response):
        item = response.meta['tvyb10_title']
        # 获取m3u8地址
        html = response.body.decode('utf-8')
        video_info = re.findall(r'player_aaaa=(.*?)</script>', html)[0]
        video_info = json.loads(video_info)
        url = video_info['url']
        js_path = 'DownloadCore\\JSFiles\\huohutv\\huohutv.js'
        with open(js_path, 'r', encoding='utf-8') as f:
            js_code = f.read()
            ctc = execjs.compile(js_code)
        m3u8_url = ctc.call('get_url', url)
        m3u8_obj = m3u8.load(m3u8_url)
        url = m3u8_obj.base_uri + m3u8_obj.playlists[0].uri
        music_m3u8_obj = m3u8.load(url)
        index = m3u8_url.find('index.m3u8')
        base_url = music_m3u8_obj.base_uri[:index]
        ts_list = music_m3u8_obj.segments.uri
        for ts in ts_list:
            url = base_url + ts
            yield scrapy.Request(url, callback=self.parse_ts, meta={'tvyb10_item': item}, dont_filter=True)

    def parse_ts(self, response):
        if response.status != 200:
            print('下载失败')
            return
        item = response.meta['tvyb10_item']
        item['video'] = response.body
        yield item
