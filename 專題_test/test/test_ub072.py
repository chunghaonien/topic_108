import urllib.request as req
from lxml import etree

def create_request(page):
    if(page == 1):
        url = 'https://www.youtube.com/'
    else:
        url = 'https://www.youtube.com/'

    headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 OPR/96.0.0.0'
    }      

    request = req.Request(url = url, headers = headers)

    return request

def get_content(request):
    response = req.urlopen(request)
    content = response.read().decode('utf-8')

    return content

def down_lond(content):
    tree = etree.HTML(content)

    name_list = tree.xpath('//div[@id ="contents"]//a//yt-formatted-string')
    src_list = tree.xpath('//div[@id ="contents"]//a//@src2')

    for i in range(len(name_list)):
        name = name_list[i]
        src = src[i]
        url = 'https:' + src

        req.urlretrieve(url = url, filename='./pa/' + name + '.jpg' )

 
if __name__ == '__main__':
    start_page = int(input('開始頁碼:'))
    end_page = int(input('結束頁碼:'))

    for page in range(start_page, end_page+1):
        request = create_request(page)
        content = get_content(request)
        down_lond(content)