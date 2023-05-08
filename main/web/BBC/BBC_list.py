import urllib.request
from lxml import etree
from bs4 import BeautifulSoup

def get_options(options_list):
    done_list = []
    for options in options_list:
        if options == 'world':
            done_list.append('https://www.bbc.com/zhongwen/trad/topics/c83plve5vmjt?')
        elif options == 'china':
            done_list.append('https://www.bbc.com/zhongwen/trad/topics/c9wpm0e5zv9t?')
        elif options == 'UA':
            done_list.append('https://www.bbc.com/zhongwen/trad/topics/c1ez1k4emn0t?')
        elif options == 'technology':
            done_list.append('https://www.bbc.com/zhongwen/trad/topics/c32p4kj2yzqt?')
        elif options == 'financial':
            done_list.append('https://www.bbc.com/zhongwen/trad/topics/cq8nqywy37yt?')
    
    return done_list

def analyze_web(url):
        headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0'
        }

        request = urllib.request.Request(url = url, headers= headers)
        response = urllib.request.urlopen(request)
        content = response.read().decode('utf-8')

        return content
    

def start_bbc(base_url):
    tree = etree.HTML(analyze_web(base_url))
    url_list = tree.xpath("//div[@class='promo-text']//a/@href")

    done_list = []
    for url in url_list:
        soup = BeautifulSoup(analyze_web(url), 'html.parser')
        title_element = soup.find('h1', class_='bbc-1tk77pb e1p3vdyi0')
        author_element = soup.find('div', class_='bbc-19j92fr ebmt73l0')
       

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
