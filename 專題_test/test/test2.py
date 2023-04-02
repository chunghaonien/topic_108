import urllib.request as req
import bs4
url="https://www.ptt.cc/bbs/movie/index.html"

#建立一個request物件，附加request headers資訊
request=req.Request(url,headers={
    "user-agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36"
}) 

with req.urlopen(request) as response:
  data=response.read().decode("utf-8")

root=bs4.BeautifulSoup(data,"html.parser")
print(root.title.string) #抓頁面標題

root1=bs4.BeautifulSoup(data,"html.parser")
titles=root1.find_all("div",class_="title") #尋找class="title"的div標籤

for title in titles: #利用迴圈取出整個頁面文章標題
  if title.a!=None:
    print(title.a.string)