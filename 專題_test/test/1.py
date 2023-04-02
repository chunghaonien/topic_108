import urllib.request as req

url = 'https://seeuu.cc/forum.php?mod=forumdisplay&fid=118'
headers = {
    ":authority": "stats.g.doubleclick.net",
    ':method': 'POST',
    ':path': '/j/collect?t=dc&aip=1&_r=3&v=1&_v=j99&tid=UA-157807446-1&cid=363726736.1675457207&jid=312329185&gjid=1675825087&_gid=719670150.1679924842&_u=SCCAAUACQAAAACAAI~&z=86522089',
    ':scheme': 'https',
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-length': '0',
    'content-type': 'text/plain',
    'cookie': 'DSID=AGJ6mWk2KGFQwXkY4CXDKAw6h4rMn_OEtdsaW4HRyBX-SFRLOyV7faXhjU0_X4aerLXcKjZ9NPFyEzEhsTvNWSSBJviSzlhTQkp-TG-e5tjKNFz6PLaSV5M5qZkCRDSQT8HchX5l9RZIRNdNJGox3_HhkQaMOcd46FpiZ5MBLlAyI9kh8KNWlMmsdBCvPkWoZhlFUJpTYjUoe2XrIzy1RFAiz-b2y9_XIq62R8pRv1QzecWwyE3rpoSvpErPn0LCAi2yq8t-JCBVNp44Bl8-dEnQ6qxRXLmTLQ; IDE=AHWqTUk1rRAOOiFyPXOzpglaoVrEZ21QedkUidII6jWigxtGswGjSnwncvEXVqtlUd0',
    'origin': 'https://seeuu.cc',
    'referer': 'https://seeuu.cc/',
    'sec-ch-ua': '"Not=A?Brand";v="8", "Chromium";v="110", "Opera";v="96"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 OPR/96.0.0.0'
}

request = req.Request(url, headers=headers)
response = req.urlopen(request)
content = response.read()
print(content)
