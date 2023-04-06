import urllib.parse
import urllib.request
import os

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
    # 获取脚本所在的目录路径
    dir_path = os.path.dirname(os.path.abspath(__file__))

    # 创建一个名为"html"的文件夹（如果不存在）
    html_dir = os.path.join(dir_path, 'html')
    if not os.path.exists(html_dir):
        os.makedirs(html_dir)

    # 指定文件路径和文件名
    file_path = os.path.join(html_dir, 'ptt' + str(page) + '.html')

    # 将HTML内容写入指定的文件中
    with open(file_path, 'w', encoding='utf-8') as fp:
        fp.write(content)
    

if __name__ == '__main__':
    start_page = int(input('輸入起始頁碼'))
    end_page = int(input('輸入結束頁碼'))

    for page in range(start_page, end_page+1):
        request = create_request(page)
        content = get_content(request)
        down_load(page, content)
