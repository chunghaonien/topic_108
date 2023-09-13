import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QAction, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLineEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import sys
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl, pyqtSlot
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup  

class TagExtractorApp(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle('標籤提取工具')
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

            page_source = driver.page_source  # 取得網頁原始碼

            soup = BeautifulSoup(page_source, 'html.parser')  # 使用BeautifulSoup解析HTML
            tags = soup.find_all('div')  # 找出所有的<div>標籤

            tag_html = [tag.prettify() for tag in tags]  # 取得標籤的HTML
            self.result_text.setPlainText('\n'.join(tag_html))
        except Exception as e:
            self.result_text.setPlainText(f'錯誤：{str(e)}')

        driver.quit()

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('網頁瀏覽與標籤提取工具')
        self.setWindowIcon(QIcon('icons/penguin.png'))
        self.resize(1200, 800)
        self.setStyleSheet('''  
            QMainWindow {
                background-color: #f0f0f0;
            }
            QToolBar {
                background-color: #333;
                color: white;
            }
            QPushButton {
                background-color: #008CBA;
                color: white;
                border: none;
                padding: 5px 10px;
                margin: 2px;
            }
            QLineEdit {
                background-color: white;
                border: 1px solid #ccc;
                padding: 5px;
            }
        ''')
        self.show()

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('https://www.google.com'))  # 初始頁面設為 Google
        self.setCentralWidget(self.browser)

        navigation_bar = QToolBar('導航')
        navigation_bar.setIconSize(QSize(16, 16))
        self.addToolBar(navigation_bar)

        back_button = QPushButton('返回')
        next_button = QPushButton('前進')
        reload_button = QPushButton('重新載入')

        back_button.clicked.connect(self.browser.back)
        next_button.clicked.connect(self.browser.forward)
        reload_button.clicked.connect(self.browser.reload)

        navigation_bar.addWidget(back_button)
        navigation_bar.addWidget(next_button)
        navigation_bar.addWidget(reload_button)

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)

        navigation_bar.addSeparator()
        navigation_bar.addWidget(self.urlbar)

        self.browser.urlChanged.connect(self.renew_urlbar)

        self.tag_extractor = TagExtractorApp(self)
        extract_tags_action = QAction('提取標籤', self)
        extract_tags_action.triggered.connect(self.show_tag_extractor)
        
        tools_menu = self.menuBar().addMenu('工具')
        tools_menu.addAction(extract_tags_action)

        self.tag_extractor.hide()

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == '':
            q.setScheme('http')
        self.browser.setUrl(q)

    def renew_urlbar(self, q):
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    def show_tag_extractor(self):
        self.tag_extractor.extract_tags()
        self.tag_extractor.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec_()
