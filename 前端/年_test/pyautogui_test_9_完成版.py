import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTextEdit, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtCore import QTimer, QDateTime
from pynput import mouse, keyboard
import threading
import time


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('實時顯示使用者動作')

        self.mouse_label = QLabel(self)
        self.keyboard_text_edit = QTextEdit(self)
        self.keyboard_text_edit.setReadOnly(True)

        self.stop_button = QPushButton('停止', self)
        self.stop_button.clicked.connect(self.stop_capture)

        self.start_button = QPushButton('開始記錄', self)
        self.start_button.clicked.connect(self.start_capture)

        self.pause_button = QPushButton('暫停記錄', self)
        self.pause_button.clicked.connect(self.pause_capture)

        self.save_button = QPushButton('儲存', self)
        self.save_button.clicked.connect(self.save_data)

        vbox = QVBoxLayout()
        vbox.addWidget(self.mouse_label)
        vbox.addWidget(self.keyboard_text_edit)
        vbox.addWidget(self.start_button)
        vbox.addWidget(self.pause_button)
        vbox.addWidget(self.stop_button)
        vbox.addWidget(self.save_button)

        self.setLayout(vbox)

        self.is_capturing = False
        self.actions = []  # 存放行動的列表
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_display)

        self.mouse_listener = None
        self.keyboard_listener = None

        self.start_time = None

        self.show()

    def update_display(self):
        # 實時更新滑鼠座標
        x, y = mouse.Controller().position
        mouse_text = f"滑鼠座標：({x}, {y})"
        self.mouse_label.setText(mouse_text)

    def on_click(self, x, y, button, pressed):
        if pressed:
            button_text = "左鍵" if button == mouse.Button.left else "右鍵"
            self.append_action(f"滑鼠點擊：({x}, {y})，按鍵：{button_text}")

    def on_scroll(self, x, y, dx, dy):
        self.append_action(f"滾輪滾動，水平：{dx}，垂直：{dy}")

    def on_press(self, key):
        try:
            key_text = f"按下按鍵：{key.char}"
            self.append_action(key_text)
        except AttributeError:
            # 如果是特殊按鍵（非字母或數字），直接顯示按鍵名稱
            key_text = f"按下按鍵：{key.name}"
            self.append_action(key_text)

    def append_action(self, action):
        if self.start_time is None:
            self.start_time = time.time()

        elapsed_time = time.time() - self.start_time
        current_time = QDateTime.fromMSecsSinceEpoch(int(elapsed_time * 1000)).toString("mm:ss")

        self.actions.append((current_time, action))
        self.keyboard_text_edit.append(f"{current_time} {action}")

    def capture_events(self):
        self.mouse_listener = mouse.Listener(on_click=self.on_click, on_scroll=self.on_scroll)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)

        with self.mouse_listener as ml, self.keyboard_listener as kl:
            try:
                while self.is_capturing:
                    time.sleep(0.1)  # 0.1秒間隔，可以根據需要調整
            except KeyboardInterrupt:
                pass

    def start_capture(self):
        self.is_capturing = True
        self.start_time = time.time()  # 重新設定起始時間
        self.timer.start(100)

        self.event_thread = threading.Thread(target=self.capture_events)
        self.event_thread.start()

    def pause_capture(self):
        self.is_capturing = False
        self.timer.stop()

    def stop_capture(self):
        self.is_capturing = False
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()

    def save_data(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "儲存檔案", "", "文本檔案 (*.txt);;所有檔案 (*)", options=options)

        if file_name:
            with open(file_name, 'w') as file:
                for time, action in self.actions:
                    file.write(f"{time} {action}\n")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
