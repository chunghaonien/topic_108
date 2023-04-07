import urllib.request
from lxml import etree
from bs4 import BeautifulSoup

def create_request(page):
    base_url = 'https://forum.gamer.com.tw/B.php?page='+ str(page) +'&bsn=36730'
    
    headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0'
    }

    request = urllib.request.Request(url = base_url, headers= headers)

    return request

def get_content(request):
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf-8')

    return content

def get_url(content):
    tree = etree.HTML(content)
    url_list = tree.xpath("/html/body/div[@id='BH-background']/div[@id='BH-wrapper']/div[@id='BH-master']/form/div[@class='b-list-wrap']/table[@class='b-list']/tbody/tr[@class='b-list__row']/td[@class='b-list__main']//@href")

    print(url_list)
    return url_list

def get_article(url):
    headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0'
    }

    url1 = 'https://forum.gamer.com.tw/' + url
    request = urllib.request.Request(url = url1, headers= headers)
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf-8')
        
    soup = bs4.BeautifulSoup(content, 'html.parser')
    title = soup.find('h1', class_='c-post__header__title ').text
    author = soup.find('div', class_='c-article__content').text
    print(title)
    print(author)



if __name__ == '__main__':
    start_page = int(input('輸入起始頁碼'))
    end_page = int(input('輸入結束頁碼'))

    for page in range(start_page, end_page+1):
        request = create_request(page)
        content = get_content(request)
        url_list = get_url(content)

        for url in url_list:
            get_article(url)