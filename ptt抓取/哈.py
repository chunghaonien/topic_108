import urllib.request
from lxml import etree
from bs4 import BeautifulSoup

def analyze_web(start_page, end_page):
    for page in range(start_page, end_page+1):
        base_url = 'https://forum.gamer.com.tw/B.php?page='+ str(page) +'&bsn=36730'

        headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0'
        }

        request = urllib.request.Request(url = base_url, headers= headers)
        response = urllib.request.urlopen(request)
        content = response.read().decode('utf-8')

    return content
    
def get_url(content):
    tree = etree.HTML(content)
    url_list = tree.xpath("//td[@class='b-list__main']/a/@href")

    return url_list

def get_article(url_list):
    for url in url_list:
        done_url = 'https://forum.gamer.com.tw/' + str(url)
        soup = BeautifulSoup(analyze_web(done_url), 'html.parser')
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



if __name__ == '__main__':
    start_page = int(input('輸入起始頁碼'))
    end_page = int(input('輸入結束頁碼'))
    
    get_article(get_url(analyze_web(start_page, end_page)))