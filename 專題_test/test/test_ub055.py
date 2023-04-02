import urllib.request

url = 'https://seeuu.cc/forum.php?mod=forumdisplay&fid=118'

response = urllib.request.urlopen(url)

# print(type(response))

content = response.readlines()
print(content)