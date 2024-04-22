import requests

url = 'https://www.iyhdmm.com/vp/23420-2-0.html'
session = requests.Session()
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
    'Referer': 'https://www.iyhdmm.com/vp/23420-2-0.html',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'zh,zh-CN;q=0.9',
}
session.headers.update(hearder)
# response = session.get(url)
# print(response.cookies)
# print(response.request.headers)

print('<--------------------------------------------->')
code_url = 'https://www.iyhdmm.com/playurl?aid=23420&playindex=2&epindex=0&r=0.9868766377739571'
res = session.get(code_url)
print(res.text)