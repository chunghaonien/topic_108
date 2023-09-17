import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtCore import QUrl
from datetime import datetime 

class EventTracker(QObject):
    mouse_wheel = pyqtSignal(int)
    key_pressed = pyqtSignal(int)
    key_released = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.event_log = []
        self.current_log_file = self.create_log_file()  

    def create_log_file(self):  
        now = datetime.now()
        file_name = now.strftime("event_log_%Y-%m-%d_%H-%M-%S.txt")
        return file_name

    def save_to_file(self, event_info):
        with open(self.current_log_file, "a") as f:  # 使用当前日志文件
            f.write(event_info + "\n")

    def update_log(self):
        pass

    def track_key_press(self, key):
        event_info = f"Key pressed: {Qt.Key(key)}"
        self.event_log.append(event_info)
        self.update_log()
        self.save_to_file(event_info)

    def track_key_release(self, key):
        event_info = f"Key released: {Qt.Key(key)}"
        self.event_log.append(event_info)
        self.update_log()
        self.save_to_file(event_info)

    def track_mouse_wheel(self, delta):
        event_info = f"Mouse wheel scrolled: {delta}"
        self.event_log.append(event_info)
        self.update_log()
        self.save_to_file(event_info)

class WebBrowserWindow(QMainWindow):
    def __init__(self, event_tracker):
        super().__init__()
        self.event_tracker = event_tracker
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('網頁瀏覽器')
        self.setWindowIcon(QIcon('icons/penguin.png'))
        self.resize(1200, 800)

        self.show()

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('https://www.google.com'))
        self.setCentralWidget(self.browser)

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)

        self.browser.urlChanged.connect(self.renew_urlbar)

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == '':
            q.setScheme('http')
        self.browser.setUrl(q)

    def renew_urlbar(self, q):
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    def keyPressEvent(self, event):
        key = event.key()
        self.event_tracker.track_key_press(key)
        super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        key = event.key()
        self.event_tracker.track_key_release(key)
        super().keyReleaseEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    event_tracker = EventTracker()
    web_browser_window = WebBrowserWindow(event_tracker)
    app.exec_()
