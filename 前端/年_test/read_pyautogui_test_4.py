import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtCore import QTimer
import threading
import time
import pyautogui
from pynput import mouse, keyboard

class PlayBackWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('動作還原')

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)

        self.load_button = QPushButton('讀取文件', self)
        self.load_button.clicked.connect(self.load_file)

        self.start_button = QPushButton('開始', self)
        self.start_button.clicked.connect(self.start_playback)

        self.clear_button = QPushButton('清除', self)
        self.clear_button.clicked.connect(self.clear_text)

        self.stop_button = QPushButton('停止', self)
        self.stop_button.clicked.connect(self.stop_playback)

        vbox = QVBoxLayout()
        vbox.addWidget(self.text_edit)
        vbox.addWidget(self.load_button)
        vbox.addWidget(self.start_button)
        vbox.addWidget(self.clear_button)
        vbox.addWidget(self.stop_button)

        self.setLayout(vbox)

        self.actions = []  # 存放還原的行動
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.playback_action)
        self.playback_thread = None  # 還原動作的執行緒

        self.show()

    def load_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "讀取檔案", "", "文本檔案 (*.txt);;所有檔案 (*)", options=options)

        if file_name:
            with open(file_name, 'r') as file:
                self.actions = [line.strip() for line in file.readlines()]

            self.text_edit.setPlainText('\n'.join(self.actions))

    def playback_action(self):
        if not self.actions:
            self.stop_playback()  # 如果動作列表為空，停止還原
            return

        action = self.actions.pop(0)
        self.text_edit.setPlainText('\n'.join(self.actions))  # 更新文字框顯示

        parts = action.split(" ")
        if "滑鼠點擊：" in action and len(parts) > 3:
            x, y = map(int, parts[3].strip("()，").split(","))
            self.simulate_mouse_click(x, y)
        elif "按下按鍵：" in action and len(parts) > 2:
            key = parts[2]
            self.simulate_key_press(key)
        elif "滾輪滾動：" in action and len(parts) > 3:
            dx, dy = map(int, parts[3].split("，"))
            self.simulate_mouse_scroll(dx, dy)

    def simulate_mouse_click(self, x, y):
        # 模擬滑鼠點擊事件
        pyautogui.click(x, y)

    def simulate_key_press(self, key):
        # 模擬按下按鍵事件
        pyautogui.press(key)

    def simulate_mouse_scroll(self, dx, dy):
        # 模擬滑鼠滾動事件
        pyautogui.scroll(dy)

    def start_playback(self):
        if not self.actions or self.playback_thread and self.playback_thread.is_alive():
            return

        self.playback_thread = threading.Thread(target=self.run_playback)
        self.playback_thread.start()

    def run_playback(self):
        for action in self.actions:
            time.sleep(0.1)  # 可以調整等待時間
            self.timer.timeout.emit()  # 觸發還原動作

    def clear_text(self):
        self.actions = []
        self.text_edit.clear()

    def stop_playback(self):
        if self.playback_thread and self.playback_thread.is_alive():
            self.playback_thread.join()  # 等待還原動作的執行緒完成
        self.timer.stop()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    playback_window = PlayBackWindow()
    sys.exit(app.exec_())
