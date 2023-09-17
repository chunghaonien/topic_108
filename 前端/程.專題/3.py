import sys
import os
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLineEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import pyqtSlot, QUrl
from PyQt5.QtGui import QIcon, QTextCursor
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from datetime import datetime  # 引入datetime模組

class EventTrackingWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.event_log = []

        self.mouse_start_pos = None
        self.mouse_end_pos = None

        self.chrome_driver_path = ChromeDriverManager().install()

    def init_ui(self):
        self.setWindowTitle('Event Tracking and Web Page')
        self.setWindowIcon(QIcon('icons/penguin.png'))
        self.resize(800, 600)

        layout = QVBoxLayout()

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)

        self.urlbar = QLineEdit()
        self.urlbar.setFixedHeight(40)
        layout.addWidget(self.urlbar)

        go_button = QPushButton('Go')
        go_button.clicked.connect(self.navigate_to_url)
        layout.addWidget(go_button)

        extract_button = QPushButton('提取標籤')
        extract_button.clicked.connect(self.extract_tags)
        layout.addWidget(extract_button)

        self.browser = QWebEngineView()
        layout.addWidget(self.browser)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # 使用create_log_file()方法創建唯一的事件記錄檔案名稱
        self.log_file_path = self.create_log_file()

    def create_log_file(self):
        now = datetime.now()
        file_name = now.strftime("event_log_%Y-%m-%d_%H-%M-%S.txt")
        return file_name

    def log_event(self, event_info):
        self.event_log.append(event_info)
        self.update_label()
        self.save_to_file()

    def update_label(self):
        self.result_text.setPlainText("\n".join(self.event_log))
        # 滾動到最底部
        cursor = self.result_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.result_text.setTextCursor(cursor)
    
    def save_to_file(self):
        with open(self.log_file_path, "w") as f:
            f.write("\n".join(self.event_log))

    def keyPressEvent(self, event):
        key = event.key()
        self.log_event(f"Key pressed: {key}")

    def wheelEvent(self, event):
        delta = event.angleDelta().y() / 120
        self.log_event(f"Mouse wheel scrolled: {delta}")

    def mouseMoveEvent(self, event):
        if self.mouse_start_pos:
            self.mouse_end_pos = event.pos()

    def mousePressEvent(self, event):
        x = event.x()
        y = event.y()
        buttons = event.buttons()
        self.log_event(f"Mouse pressed at ({x}, {y}) - Buttons: {buttons}")
        self.mouse_start_pos = event.pos()

    def mouseReleaseEvent(self, event):
        x = event.x()
        y = event.y()
        buttons = event.buttons()
        self.log_event(f"Mouse released at ({x}, {y}) - Buttons: {buttons}")
        if self.mouse_start_pos and self.mouse_end_pos:
            self.log_event(f"Mouse drag from {self.mouse_start_pos} to {self.mouse_end_pos}")
        self.mouse_start_pos = None
        self.mouse_end_pos = None

    @pyqtSlot()
    def navigate_to_url(self):
        url = self.urlbar.text()
        self.browser.setUrl(QUrl(url))

    @pyqtSlot()
    def extract_tags(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--ignore-certificate-errors')
        service = Service(self.chrome_driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        try:
            current_url = self.browser.url().toString()
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

class MainApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)

        self.main_window = EventTrackingWindow()
        self.main_window.show()

if __name__ == "__main__":
    app = MainApp(sys.argv)
    sys.exit(app.exec_())
