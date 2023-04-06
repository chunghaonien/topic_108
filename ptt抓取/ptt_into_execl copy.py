import urllib.parse
import urllib.request
import os
import pandas as pd

def create_request(page):
    base_url = 'https://www.ptt.cc/bbs/Baseball/index'

    url = base_url + str(page) + '.html'

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0'
    }

    request = urllib.request.Request(url=url, headers=headers)
    return request

def get_content(request):
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf-8')

    return content

def parse_content(content):
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(content, 'lxml')

    results = []
    for article in soup.find_all('div', class_='r-ent'):
        if article.find('div', class_='date').text.strip() == '':
            continue

        title = article.find('div', class_='title').text.strip()
        href = article.find('div', class_='title').find('a')['href']
        url = urllib.parse.urljoin('https://www.ptt.cc/', href)
        date = article.find('div', class_='date').text.strip()
        author = article.find('div', class_='author').text.strip()

        request = urllib.request.Request(url=url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(request)
        article_content = response.read().decode('utf-8')

        article_soup = BeautifulSoup(article_content, 'html.parser')

        content = article_soup.find('div', class_='bbs-screen bbs-content').text.strip()

        results.append({'Title': title, 'URL': url, 'Date': date, 'Author': author, 'Content': content})

    return results


if __name__ == '__main__':
    start_page = int(input('輸入起始頁碼：'))
    end_page = int(input('輸入結束頁碼：'))

    all_results = []

    for page in range(start_page, end_page + 1):
        request = create_request(page)
        content = get_content(request)
        results = parse_content(content)
        all_results += results

    df = pd.DataFrame(all_results)

    dir_path = os.path.dirname(os.path.abspath(__file__))

    data_dir = os.path.join(dir_path, 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    file_path = os.path.join(data_dir, 'ptt_data.xlsx')

    df.to_excel(file_path, index=False)
    
    print('数据已成功存储为Excel文件')
