import urllib.parse
import urllib.request
import os
from bs4 import BeautifulSoup
import xlwt
import xlrd
from xlutils.copy import copy

def create_request(page):
    base_url = 'https://www.ptt.cc/bbs/Baseball/index'

    url = base_url + str(page) + '.html'

    headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0'
    }

    request = urllib.request.Request(url = url, headers= headers)
    return request


def get_content(request):
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf-8')

    return content

def down_load(page, content):
    dir_path = os.path.dirname(os.path.abspath(__file__))

    html_dir = os.path.join(dir_path, 'html')
    if not os.path.exists(html_dir):
        os.makedirs(html_dir)

    file_path = os.path.join(html_dir, 'ptt' + str(page) + '.html')

    with open(file_path, 'w', encoding='utf-8') as fp:
        fp.write(content)

def parse_content(content):
    soup = BeautifulSoup(content, 'html.parser')
    posts = soup.find_all('div', class_='r-ent')

    results = []

    for post in posts:
        title = post.find('div', class_='title').find('a').text
        link = post.find('div', class_='title').find('a').get('href')
        link = urllib.parse.urljoin('https://www.ptt.cc/', link)
        author = post.find('div', class_='author').text.strip()
        date = post.find('div', class_='date').text.strip()

        request = urllib.request.Request(url=link, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(request)
        content = response.read().decode('utf-8')

        post_soup = BeautifulSoup(content, 'html.parser')
        post_content = post_soup.find('div', id='main-content').text.strip()
        post_content = post_content.split('※ 發信站')[0]

        result = {
            'title': title,
            'link': link,
            'author': author,
            'date': date,
            'content': post_content
        }
        results.append(result)

    return results

def write_excel(data):
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet('sheet 1')
        for i in range(len(data)):
            for j in range(len(data[i])):
                sheet.write(i, j, data[i][j])
        wbk.save('data.xls')

if __name__ == '__main__':
    start_page = int(input('輸入起始頁碼'))
    end_page = int(input('輸入結束頁碼'))

    results = []

    for page in range(start_page, end_page+1):
        request = create_request(page)
        content = get_content(request)
        down_load(page, content)

        page_results = parse_content(content)
        results.extend(page_results)