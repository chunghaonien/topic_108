import urllib.request

url = 'https://movie.douban.com/j/chart/top_list?type=5&interval_id=100%3A90&action=&start=0&limit=20'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0'
}

request = urllib.request.Request(url = url, headers= headers)

response = urllib.request.urlopen(request)
content = response.read().decode('utf-8')

#fp = open('douban.json', 'w', encoding='utf-8')
#fp.write(content)

with open('doban.json', 'w',encoding='utf-8') as fp:
    fp.write(content)