from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from app import *
import time

def handle_return_value(returned_value):
    print(f"回傳的值: {returned_value}")
    return returned_value

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    web_browser_window = WebBrowserWindow(main_window)
    web_browser_window.return_url_signal.connect(handle_return_value)
    web_browser_window.return_path_signal.connect(handle_return_value)
    app.exec_()

url = handle_return_value('')  # 传递一个空字符串作为占位符

drivers = webdriver.Chrome()
drivers.get(url)
time.sleep(10)

# eles = drivers.find_elements(By.XPATH, "")

# result1 = [ele.text for ele in eles]
# result2 = {
#     'title': result1
# }

# results = []
# for i in range(len(result1)):
#     results.append(result2['title'][i])

# print(results)