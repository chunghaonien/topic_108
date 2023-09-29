import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QLineEdit, QPushButton
import pyautogui
import time
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class BrowserRecorder(QMainWindow):
    def __init__(self):
        super().__init__()

        self.browser = QWebEngineView(self)
        self.browser.setGeometry(0, 0, 800, 600)

        self.record_button = QPushButton('開始錄製', self)
        self.record_button.setGeometry(10, 610, 100, 30)
        self.record_button.clicked.connect(self.start_recording)

        self.stop_button = QPushButton('停止錄製', self)
        self.stop_button.setGeometry(120, 610, 100, 30)
        self.stop_button.clicked.connect(self.stop_recording)
        self.stop_button.setEnabled(False)

        self.recording = False
        self.script = []

    def start_recording(self):
        self.recording = True
        self.record_button.setEnabled(False)
        self.stop_button.setEnabled(True)

        while self.recording:
            time.sleep(0.1)  # 等待0.1秒
            x, y = pyautogui.position()
            action = f"pyautogui.moveTo({x}, {y}, duration=0.25)"
            self.script.append(action)

    def stop_recording(self):
        self.recording = False
        self.record_button.setEnabled(True)
        self.stop_button.setEnabled(False)

        with open('recorded_script.py', 'w') as f:
            f.write('\n'.join(self.script))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    browser_recorder = BrowserRecorder()
    browser_recorder.browser.load(QUrl('https://www.google.com'))  # 載入預設網頁
    browser_recorder.show()
    sys.exit(app.exec_())
