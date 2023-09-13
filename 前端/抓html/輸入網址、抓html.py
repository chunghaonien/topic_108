import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLineEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from PyQt5.QtCore import pyqtSlot, QUrl
from PyQt5.QtGui import QIcon
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

class TagExtractorApp(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle('Tag')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)

        layout.addWidget(self.result_text)

        self.setLayout(layout)

        self.chrome_driver_path = ChromeDriverManager().install()

    @pyqtSlot()
    def extract_tags(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--ignore-certificate-errors')
        service = Service(self.chrome_driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        try:
            current_url = self.main_window.browser.url().toString()
            driver.get(current_url)

            tags = driver.find_elements(By.XPATH, '//div')  # 使用 XPath 獲取所有 div 標籤

            tag_html = [tag.get_attribute('outerHTML') for tag in tags]
            self.result_text.setPlainText('\n'.join(tag_html))
        except WebDriverException as e:
            self.result_text.setPlainText(f'Selenium Error: {str(e)}')
        except Exception as e:
            self.result_text.setPlainText(f'Error: {str(e)}')
        finally:
            driver.quit()

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('Tag Extractor')
        self.setWindowIcon(QIcon('icons/penguin.png'))
        self.resize(800, 600)

        self.urlbar = QLineEdit()
        self.urlbar.setFixedHeight(40)  # 設置高度

        layout = QVBoxLayout()
        layout.addWidget(self.urlbar)

        go_button = QPushButton('Go')  # 新增的按鈕
        go_button.clicked.connect(self.navigate_to_url)
        layout.addWidget(go_button)

        extract_button = QPushButton('提取標籤')
        extract_button.clicked.connect(self.show_tag_extractor)
        layout.addWidget(extract_button)

        # 初始化 'browser'
        self.browser = QWebEngineView()
        layout.addWidget(self.browser)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.tag_extractor = TagExtractorApp(self)

    def navigate_to_url(self):
        url = self.urlbar.text()
        self.browser.setUrl(QUrl(url))  # 修正此處，使用 self.browser 設置 URL

    def show_tag_extractor(self):
        self.tag_extractor.extract_tags()
        self.tag_extractor.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
