import json
import scrapy
import execjs
import re
from DownloadCore.items import NeteaseItem

class A163Spider(scrapy.Spider):
    name = "netease_music"
    allowed_domains = ["music.163.com"]
    start_urls = ["https://music.163.com"]

    def start_requests(self):
        music_id = input("请输入歌曲ID：")
        base_url = 'https://music.163.com/song?id='
        url = base_url + music_id
        item = NeteaseItem()
        item['music_id'] = music_id
        yield scrapy.Request(url, callback=self.parse, meta={'music_item': item})
        
        
    def parse(self, response):
        if response.status != 200:
            print("请求失败")
            return
        html = response.body
        music_name = re.findall(r'<meta property="og:title" content="(.*?)" />', html.decode('utf-8'))[0]
        item = response.meta['music_item']
        item['music_name'] = music_name
        base_url = 'https://music.163.com/weapi/song/enhance/player/url/v1'
        url = base_url + '?csrf_token=' + 'f0d7c28ac0caf90a16e2743f07e01a00'
        js_path = 'DownloadCore\\JSFiles\\netease\\netease_music.js'
        with open(js_path, 'r', encoding='utf-8') as f:
            js_code = f.read()
            ctx = execjs.compile(js_code)
        params = ctx.call('get_params', item['music_id'])
        # print(params)
        yield scrapy.FormRequest(url, formdata=params, callback=self._music_parse, method='POST', meta={'music_item': item})
        
    def _music_parse(self, response):
        if response.status != 200:
            print("请求失败")
            return
        music_info = json.loads(response.body.decode('utf-8'))
        music_url = music_info['data'][0]['url']
        item = response.meta['music_item']
        yield scrapy.Request(music_url, callback=self._music_download, meta={'music_item': item},dont_filter=True)
        
    def _music_download(self, response):
        if response.status != 200:
            print("音乐下载失败")
            return
        item = response.meta['music_item']
        item['music'] = response.body
        print("音乐下载成功")
        yield item