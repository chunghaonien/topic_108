import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QLineEdit, QPushButton, QHBoxLayout, QLabel, QFileDialog
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from datetime import datetime
from PyQt5.QtCore import QTimer, QDateTime
from pynput import mouse, keyboard
import threading
import time

class MainWindow(QWidget):
    def __init__(self):
        super().__init()
        self.event_log = []
        self.selected_text_to_record = None  # 添加这个变量以保存选定文本
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('使用者動作')

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
        self.start_time = time.time()
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

    def save_to_file(self, event_info):
        with open('event_log.txt', 'a') as file:
            file.write(event_info + '\n')

class WebBrowserWindow(QMainWindow):
    text_selected = pyqtSignal(str)

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('網頁瀏覽器')
        self.setWindowIcon(QIcon('icons/penguin.png'))
        self.resize(1200, 800)
        self.setStyleSheet('''
            QPushButton {
                background-color: #008CBA;
                color: white;
                border: none;
                padding: 5px 10px;
                margin: 2px;
            }
        ''')
        self.show()

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('https://www.google.com'))
        self.setCentralWidget(self.browser)

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        self.browser.urlChanged.connect(self.renew_urlbar)

        self.selected_text_editor = QTextEdit(self)
        self.selected_text_editor.setReadOnly(True)
        self.selected_text_editor.setFixedHeight(100)

        self.browser.selectionChanged.connect(self.handle_selection_changed)

        self.browser.urlChanged.connect(self.log_url_change)

        self.record_highlight_button = QPushButton("反白元素", self)
        self.record_highlight_button.clicked.connect(self.show_element_info)
        self.record_highlight_button.setFixedSize(80, 30)

        self.back_button = QPushButton("返回", self)
        self.back_button.clicked.connect(self.browser.back)
        self.back_button.setFixedSize(80, 30)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.record_highlight_button)
        button_layout.addStretch(1)

        layout = QVBoxLayout()
        layout.addWidget(self.urlbar)
        layout.addWidget(self.browser)
        layout.addLayout(button_layout)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == '':
            q.setScheme('http')
        self.browser.setUrl(q)

    def renew_urlbar(self, q):
        new_url = q.toString()
        self.urlbar.setText(new_url)
        self.urlbar.setCursorPosition(0)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp}: 網頁: {new_url}\n"
        self.main_window.event_log.append(log_entry)

    def log_url_change(self, url):
        if url.isValid():
            url_text = url.toString()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"{timestamp}: 網頁 URL 變化 - {url_text}\n"
            self.main_window.event_log.append(log_entry)

    def handle_selection_changed(self):
        selected_text = self.browser.page().selectedText()
        if selected_text:
            self.text_selected.emit(selected_text)

    def show_element_info(self):
        selected_text = self.main_window.selected_text_to_record
        if selected_text:
            js_code = '''
            function getPathTo(element) {
                var path = [];
                while (element !== null && element.nodeType === 1) {
                    var name = element.tagName.toLowerCase();
                    var siblings = element.parentNode.childNodes;
                    var index = 1;
                    for (var i = 0; i < siblings.length; i++) {
                        var sibling = siblings[i];
                        if (sibling === element) {
                            path.unshift(name + '[' + index + ']');
                            break;
                        }
                        if (sibling.nodeType === 1 && sibling.tagName.toLowerCase() === name) {
                            index++;
                        }
                    }
                    element = element.parentNode;
                }
                return path.join('/');
            }

            var selectedText = window.getSelection().toString();
            var element = window.getSelection().anchorNode.parentElement;
            var path = getPathTo(element);
            
            '(' + selectedText + ',' + path + ')';
            '''
            self.browser.page().runJavaScript(js_code, self.handle_js_call)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    web_browser_window = WebBrowserWindow(main_window)
    web_browser_window.text_selected.connect(main_window.handle_js_call)
    app.exec_()
