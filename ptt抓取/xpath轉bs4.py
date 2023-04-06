from bs4 import BeautifulSoup

def xpath_to_bs4(xpath):
    xpath = xpath.replace("'", "\"")
    xpath = xpath.replace("/", ".")
    xpath = xpath.replace("@", ".attrs.get(")
    xpath = xpath.replace("[", "](") + ")"

    bs4_code = f"soup.{xpath}"
    return bs4_code

# 測試
xpath = "/html/body/div[@class='container']/p[@id='content']"
bs4_code = xpath_to_bs4(xpath)
print(bs4_code)
