import requests
import execjs

url = 'https://www.huohutv.net/vod-detail-id-52720.html'
res = requests.get(url)
print(res.text)