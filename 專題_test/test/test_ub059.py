import urllib.request
import urllib.parse

url = 'https://translate.google.com.tw/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0'
}

data = {
    'f.req': '[[["AVdN8","[\"spider\",\"en\",\"zh-TW\"]",null,"generic"]]]',
    'at' : 'AO-hD9wCkJxxZwziOrozjJk_UOXd:1678122760848',
    'sl': 'en',
    'tl': 'zh-TW',
    'op': 'translate'
}

data = urllib.parse.urlencode(data).encode('utf-8')

request = urllib.request.Request(url= url, data= data, headers= headers)

response = urllib.request.urlopen(request)

content = response.read().decode('utf-8')

print(content)