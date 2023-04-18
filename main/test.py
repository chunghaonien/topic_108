import urllib.request
from lxml import etree
from bs4 import BeautifulSoup

url = 'https://forum.gamer.com.tw/B.php?page=1&bsn=36730'

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0'
}

request = urllib.request.Request(url = url, headers= headers)

response = urllib.request.urlopen(request)
content = response.read().decode('utf-8')

tree = etree.HTML(content)
url_list = tree.xpath("//td[@class='b-list__main']/a/@href")

print(url_list)

for url in url_list:
   
    url1 = 'https://forum.gamer.com.tw/' + str(url)
    request = urllib.request.Request(url = url1, headers= headers)
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf-8')
    soup = BeautifulSoup(content, 'html.parser')
    title_element = soup.find('h1', class_='c-post__header__title')
    author_element = soup.find('div', class_='c-article__content')

    if title_element:
        title = title_element.text
        print(title)
    else:
        print("未找到標題元素")
    if author_element:
        author = author_element.text
        print(author)
    else:
        print("未找到內容元素")