from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from app import *

options = Options()
options.add_argument("--disable-notifications")

drivers = webdriver.Chrome(options)
drivers.get('')

eles = drivers.find_elements(By.XPATH, "")

result1 = [ele.text for ele in eles]
result2 = {
    'title': result1
}

results = []
for i in range(len(result1)):
    results.append(result2['title'][i])

print(results)