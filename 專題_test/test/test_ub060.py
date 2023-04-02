import urllib.request
import urllib.parse

url = 'https://fanyi.baidu.com/v2transapi?from=en&to=zh'

headers = {
    'Cookie': 'BAIDUID=B6731967488FD12005AE9664F6D5C737:FG=1; BAIDUID_BFESS=B6731967488FD12005AE9664F6D5C737:FG=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1678122519; APPGUIDE_10_0_2=1; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; ab_sr=1.0.1_MWVjNmQ5MzFhZDVjYzBkMzIyZDRiODYwY2Q3NDNlZmQ3YjIyOWVhMjQ5MWFmMTNjYzFmN2QzZjZmOGM3OTE2ODE4OTVjOWE4NDdhZGRiOWNjZmM5MTE4ZTk4ZTExYjY1MGE0MDA4ZTA4Y2VkYjYxZmRlZTkxMzQwMTZlN2E0YzFhOTgzMGI0ZTZlNzg4YTUxMDhhZTFhODk4NGNiMjc3OA==; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1678122647',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
}

data = {
    'from': 'en',
    'to': 'zh',
    'query': 'love',
    'simple_means_flag': '3',
    'sign': '198772.518981',
    'token': 'a585d0d995335460690f7e152207b964',
    'domain': 'common'
}

data = urllib.parse.urlencode(data).encode('utf-8')

request = urllib.request.Request(url = url, data = data, headers= headers)

response = urllib.request.urlopen(request)

content = response.read().decode('utf-8')

import json

obj = json.loads(content)

print(obj)