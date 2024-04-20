import scrapy
import json
import re
from DownloadCore.items import BilibiliItem
from urllib.parse import urlencode


class BilibiliSpider(scrapy.Spider):
    name = "bilibili"
    allowed_domains = ["bilibili.com"]
    start_urls = ["https://www.bilibili.com/bangumi/play/ss25739"]

    def start_requests(self):
        if "BV" in self.start_urls[0]:
            yield scrapy.Request(self.start_urls[0], callback=self._bv_parse)
        if "ss" in self.start_urls[0] and "bangumi" in self.start_urls[0]:
            yield scrapy.Request(self.start_urls[0], callback=self._ss_parse)
        
    def parse(self, response):
        pass
    
    def _ss_parse(self, response):
        html = response.text
        episodes = re.findall(r'episodes":(.*?),"user_status', html)[0]
        episode_list = json.loads(episodes)
        base_url = "https://api.bilibili.com/pgc/player/web/v2/playurl?"
        item = BilibiliItem()
        for episode in episode_list:
            item["title"] = episode["playerEpTitle"]
            params = {
                "avid": episode["aid"],
                "cid": episode["cid"],
                "ep_id": episode["ep_id"],
                "fnval": 4048
            }
            url = base_url + urlencode(params)
            yield scrapy.Request(url, callback=self._episode_parse, meta={"bilibili_item": item})
            break
    
    def _episode_parse(self, response):
        if response.status != 200:
            print("episode download failed")
            return
        item = response.meta["bilibili_item"]
        
        video_info = json.loads(response.text)["result"]["video_info"]
        # 视频格式
        format = video_info["support_formats"][0]
        video_url = ""
        video_info_list = video_info["dash"]["video"]
        for info in video_info_list:
            if info["id"] == format["quality"] and info["codecs"] == format["codecs"][0]:
                video_url = info["baseUrl"]
        audio_url = video_info["dash"]["audio"][0]["baseUrl"]
        yield scrapy.Request(video_url, callback=self._video_parse, meta={"bilibili_item": item}, dont_filter=True)
        yield scrapy.Request(audio_url, callback=self._audio_parse, meta={"bilibili_item": item}, dont_filter=True)
        
        
            
    def _bv_parse(self, response):
        html = response.text
        title = re.findall(r'<title data-vue-meta="true">(.*?)</title>', html)[0]
        video_info = re.findall(r'video":(.*?),"audio', html)[0]
        video_info_list = json.loads(video_info)
        audio_info = re.findall(r'audio":(.*?),"dolby', html)[0]
        audio_info_list = json.loads(audio_info)
        video_url = video_info_list[0]["baseUrl"]
        audio_url = audio_info_list[0]["baseUrl"]
        item = BilibiliItem()
        item["title"] = title
        print("video_url:", video_url)
        print("audio_url:", audio_url)
        yield scrapy.Request(video_url, callback=self._video_parse, meta={"bilibili_item": item}, dont_filter=True)
        yield scrapy.Request(audio_url, callback=self._audio_parse, meta={"bilibili_item": item}, dont_filter=True)
    
    def _video_parse(self, response):
        if response.status != 200:
            print("video download failed")
            return
        item = response.meta["bilibili_item"]
        video = response.body
        item["video"] = video
        print("video download success")
        yield item
    
    def _audio_parse(self, response):
        if response.status != 200:
            print("audio download failed")
            return
        item = response.meta["bilibili_item"]
        audio = response.body
        item["audio"] = audio
        print("audio download success")
        yield item