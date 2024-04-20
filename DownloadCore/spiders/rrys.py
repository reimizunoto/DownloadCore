import scrapy
from DownloadCore.items import RrysItem
import re
import m3u8

class RrysSpider(scrapy.Spider):
    name = "rrys"
    allowed_domains = ["rrys.pro"]
    start_urls = ["https://rrys.pro/dianshiju/meiju/27916"]

    def parse(self, response):
        title = response.xpath("//div[@class=\"detail_name mb_none clearfix\"]/span/text()").extract_first()
        title_detail = response.xpath("//dd[@class=\"playlist1\"]/ul/li/a/@title").extract()
        video_url = response.xpath("//dd[@class=\"playlist1\"]/ul/li/a/@href").extract()
        video_info_list = {key: value for key, value in zip(title_detail, video_url)}
        item = RrysItem()
        for key, value in video_info_list.items():
            item["title"] = title + "-" + key
            url = "https://rrys.pro/" + value
            yield scrapy.Request(url, callback=self.parse_video, meta={"rrys_item": item})
            break

    def parse_video(self, response):
        item = response.meta["rrys_item"]
        html = response.text
        m3u8_url = re.findall(r"now=\"(.*?)\";var", html)[0]
        index = m3u8_url.find("index.m3u8")
        base_url = m3u8_url[:index] + "1000k/hls/"
        m3u8_url = base_url + m3u8_url[index:]
        m3u8_obj = m3u8.load(m3u8_url)
        ts_list = m3u8_obj.segments.uri
        for ts in ts_list:
            yield scrapy.Request(base_url + ts, callback=self.parse_ts, meta={"rrys_item": item}, dont_filter=True)
            # break
        
            
    def parse_ts(self, response):
        item = response.meta["rrys_item"]
        item["video_ts"] = response.body
        yield item
        