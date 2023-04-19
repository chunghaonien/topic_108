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

def get_article(url):
        soup = BeautifulSoup(analyze_web(url), 'html.parser')
        title_element = soup.find('h3', class_='_eYtD2XCVieq6emjKBH3m')
        author_element = soup.find('div', class_='_292iotee39Lmt0MkQZ2hPV RichTextJSON-root')
        
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

if __name__ == '__main__':
    url = input("請輸入reddit網址:")
    get_article(url)