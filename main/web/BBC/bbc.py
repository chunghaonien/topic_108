# url = https://www.bbc.com/zhongwen/trad/topics/c83plve5vmjt?
# 取得BBC國際分類的文章連結

# url = https://www.bbc.com/zhongwen/trad/topics/c9wpm0e5zv9t?
# 取得BBC兩岸分類的文章連結

# url = https://www.bbc.com/zhongwen/trad/topics/c1ez1k4emn0t?
# 取得BBC英國分類的文章連結

# url = https://www.bbc.com/zhongwen/trad/topics/c32p4kj2yzqt?
# 取得BBC科技分類的文章連結

# url = https://www.bbc.com/zhongwen/trad/topics/cq8nqywy37yt?
# 取得BBC財經分類的文章連結

from lxml import etree
from bs4 import BeautifulSoup
import urllib.parse
import urllib.request

def sorted(sort):
    if sort == '國際':
        sorted_url = 'https://www.bbc.com/zhongwen/trad/topics/c83plve5vmjt?'
    elif sort == '兩岸':
        sorted_url = 'https://www.bbc.com/zhongwen/trad/topics/c9wpm0e5zv9t?'
    elif sort == '英國':
        sorted_url = 'https://www.bbc.com/zhongwen/trad/topics/c1ez1k4emn0t?'
    elif sort == '科技':
        sorted_url = 'https://www.bbc.com/zhongwen/trad/topics/c32p4kj2yzqt?'
    elif sort == '財經':
        sorted_url = 'https://www.bbc.com/zhongwen/trad/topics/cq8nqywy37yt?'
    else:
        print('請輸入正確的分類')
        return
    return sorted_url

def create_request(sorted_url, page):
    base_url = str(sorted_url)

    data = {
        'page': page
    }

    data = urllib.parse.urlencode(data)

    url = base_url + data
    
    headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0'
    }

    request = urllib.request.Request(url = url, headers= headers)

    return request

def get_content(request):
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf-8')

    return content

def get_url(content):
    tree = etree.HTML(content)
    url_list = tree.xpath('//body/div/div/div/main/div/div/ul/li//a/@href')

    return url_list

def get_article(url_list):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0'
    }

    for url in url_list:
        url1 = url
        request = urllib.request.Request(url = url1, headers= headers)
        response = urllib.request.urlopen(request)
        content = response.read().decode('utf-8')
        soup = BeautifulSoup(content, 'html.parser')
        title_element = soup.find('h1', class_='bbc-1tk77pb e1p3vdyi0')

        if title_element:
            title = title_element.text
            print(title)
        else:
            print("未找到標題元素")

        tree = etree.HTML(content)
        article = tree.xpath('//body/div/div/div/div/div/main/div[@dir="ltr"]/p/text()')
        if article != []:
            print(article)
        else:
            print("未找到文章元素")
        

if __name__ == '__main__':
    sort = input('輸入分類：')
    start_page = int(input('輸入起始頁碼：'))
    end_page = int(input('輸入結束頁碼：'))
    for page in range(start_page, end_page+1):
        url = sorted(sort)
        request = create_request(url, page)
        content = get_content(request)
        url_list = get_url(content)
        get_article(url_list)