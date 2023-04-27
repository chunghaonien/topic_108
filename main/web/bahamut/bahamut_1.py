import urllib.request
from lxml import etree
from bs4 import BeautifulSoup

def analyze_web(url):
        headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0'
        }

        request = urllib.request.Request(url = url, headers= headers)
        response = urllib.request.urlopen(request)
        content = response.read().decode('utf-8')

        return content
    

def start_bahamut(base_url):
    tree = etree.HTML(analyze_web(base_url))
    url_list = tree.xpath("//td[@class='b-list__main']/a/@href")

    done_list = []
    for url in url_list:
        done_url = 'https://forum.gamer.com.tw/' + str(url)
        soup = BeautifulSoup(analyze_web(done_url), 'html.parser')
        title_element = soup.find('h1', class_='c-post__header__title')
        author_element = soup.find('div', class_='c-article__content')
       

        if title_element:
            title = title_element.text
            done_list.append(title)
        else:
            done_list.append("未找到標題元素")
        if author_element:
            author = author_element.text
            done_list.append(author)
        else:
            done_list.append("未找到內容元素")

    return done_list
