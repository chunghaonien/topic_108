
import urllib.request as req

url = 'https://www.google.com/'

response = req.urlopen(url)

content = response.read().decode('UTF-8')

print(content)