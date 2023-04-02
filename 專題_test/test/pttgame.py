import urllib.request as req
import bs4

# 設定要爬取的版名和頁數
board = 'Gossiping'
page = 1

url = 'https://www.ptt.cc/bbs/Gossiping/index2.html'

headers = {
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0'
}

#建立一個request物件，附加request headers資訊
request=req.Request(url = url, headers = headers) 

response = req.urlopen(request)
# 解析 HTML
content = response.read().decode('utf-8')

print(content)