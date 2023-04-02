import urllib.request
import urllib.parse


base_url = 'https://www.baidu.com/s?'

date={
    'wd' : '周杰倫',
    'sex' : '男'
}

new_date = urllib.parse.urlencode(date)

url = base_url + new_date

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0'
}

request = urllib.request.Request(url = url, headers= headers)

response = urllib.request.urlopen(request)

content = response.read().decode('utf-8')

print(content)