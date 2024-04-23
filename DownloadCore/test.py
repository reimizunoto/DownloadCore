import requests
import execjs

music_id = input('请输入歌曲ID：')
url = 'https://music.163.com/weapi/v3/song/detail?csrf_token=f0d7c28ac0caf90a16e2743f07e01a00'
js_path = 'DownloadCore\\JSFiles\\netease\\netease_music.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js_code = f.read()
ctx = execjs.compile(js_code)
params = ctx.call('get_params', music_id)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
    'Accept': '*/*',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    # 'Accept-Language': 'zh-CN,zh;q=0.9',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'https://music.163.com/'
}

res = requests.post(url, headers=headers, data=params)
print(res.text)