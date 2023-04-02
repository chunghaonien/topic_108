import urllib.request
from bs4 import BeautifulSoup


def html(url):
    headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0'
    }

    request = urllib.request.Request(url = url, headers= headers)

    try:
        response = urllib.request.urlopen(request)
        content = response.read().decode('utf-8')
        return content
    except urllib.error.HTTPError as e:
        return e.code

def bs4(url):

    return '1'