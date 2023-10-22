from selenium import webdriver
from selenium.webdriver.common.by import By
from package import *
import time

drivers = None  # 定義全局變數

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    web_browser_window = WebBrowserWindow(main_window)
    
    def handle_url(url):
        print(f"回傳的 URL: {url}")
        global drivers  # 使用全局的 drivers 變數
        drivers = webdriver.Chrome()
        drivers.get(url)
    
    def handle_path(path):
        print(f"回傳的路徑: {path}")
        if drivers:
            # 使用 drivers 查找元素
            eles = drivers.find_elements(By.XPATH, path)
            results = [ele.text for ele in eles]
            print(results)
    
    web_browser_window.return_url_signal.connect(handle_url)
    web_browser_window.return_path_signal.connect(handle_path)
    
    app.exec_()

    if drivers:
        drivers.quit()  # 關閉瀏覽器