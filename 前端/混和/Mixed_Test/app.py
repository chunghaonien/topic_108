import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QLineEdit, QPushButton, QHBoxLayout, QLabel, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import pyqtSignal
from datetime import datetime
from PyQt5.QtCore import QTimer, QDateTime
from pynput import mouse, keyboard
import threading
import time

# 定義一個用於追蹤事件的類別
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.event_log = []
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
        if button == mouse.Button.left:
            button_text = "左鍵"
        elif button == mouse.Button.right:
            button_text = "右鍵"
        else:
            button_text = "其他按鍵"

        if pressed:
            self.mouse_state = f"按住點擊：({x}, {y})，按鍵：{button_text}"
            self.last_mouse_action_time = datetime.now()
        else:
            if self.mouse_state:
                elapsed_time = (datetime.now() - self.last_mouse_action_time).total_seconds()
                if elapsed_time > 0.1:  # 超過0.1秒視為一個新事件
                    self.append_action(f"滑鼠拖移：({x}, {y})，按鍵：{button_text}")
                else:
                    self.append_action(self.mouse_state)  # 合併連續事件

            self.mouse_state = None

    def on_scroll(self, x, y, dx, dy):
        self.append_action(f"滾輪滾動，水平：{dx}，垂直：{dy}")

    def set_selected_text_to_record(self, selected_text):
        self.selected_text_to_record = selected_text


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

    def save_to_file(self, event_info):
        # 在這裡實現將事件信息保存到文件的邏輯
        with open('event_log.txt', 'a') as file:
            file.write(event_info + '\n')

# 定義瀏覽器窗口類別
class WebBrowserWindow(QMainWindow):
    return_url_signal = pyqtSignal(str)
    return_path_signal = pyqtSignal(str)

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        # 設置窗口標題和圖示
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

        # 創建 Web 瀏覽器視窗
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('https://www.google.com'))
        self.setCentralWidget(self.browser)

        # 設置 URL 地址欄
        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)

        # 監聽網頁 URL 變化事件
        self.browser.urlChanged.connect(self.renew_urlbar)

        # 創建用於顯示選擇的文本的文本編輯框
        self.selected_text_editor = QTextEdit(self)
        self.selected_text_editor.setReadOnly(True)
        self.selected_text_editor.setFixedHeight(100)

        # 監聽網頁選擇文本事件
        self.browser.selectionChanged.connect(self.handle_selection_changed)

        # 添加以下代碼以記錄 URL 變化事件
        self.browser.urlChanged.connect(self.log_url_change)

        # 創建記錄反白文本和元素資訊的按鈕
        self.record_highlight_button = QPushButton("反白元素", self)
        self.record_highlight_button.clicked.connect(self.show_element_info)
        self.record_highlight_button.setFixedSize(80, 30)

        # 創建返回按鈕
        self.back_button = QPushButton("返回", self)
        self.back_button.clicked.connect(self.browser.back)
        self.back_button.setFixedSize(80, 30)

        # 創建一個水平佈局並將按鈕添加到其中
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.record_highlight_button)
        button_layout.addStretch(1) #將按鈕推到左邊

        # 主佈局包含其他小部件和水平佈局
        layout = QVBoxLayout()
        layout.addWidget(self.urlbar)
        layout.addWidget(self.browser)
        layout.addLayout(button_layout)  

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    # 將瀏覽器導向輸入的 URL
    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == '':
            q.setScheme('http')
        self.browser.setUrl(q)

    # 上面URL 地址欄的文字
    def renew_urlbar(self, q):
        new_url = q.toString()
        self.urlbar.setText(new_url)
        self.urlbar.setCursorPosition(0)

        # 記錄新的 URL 到日誌文件
        log_entry = f" 網頁: {new_url}\n"
        self.main_window.event_log.append(log_entry)
        self.main_window.append_action(log_entry)

    # 記錄網頁 URL 變化事件(點擊連結)
    def log_url_change(self, url):
        if url.isValid():
            url_text = url.toString()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"{timestamp}: 網頁 URL 變化 - {url_text}\n"
            self.main_window.event_log.append(log_entry)
            self.return_url_signal.emit(url_text)  
        # url_text 就是 URL 的文字表示

    # 定義 handle_selection_changed 方法，用於處理網頁選擇文本事件
    def handle_selection_changed(self):
        selected_text = self.browser.page().selectedText()
        if selected_text:
            self.main_window.set_selected_text_to_record(selected_text)

    # 定義 show_element_info 方法，用於顯示反白文本的元素資訊
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
            
    # 定義 handle_js_call 方法，用於處理 JavaScript 呼叫並將反白內容存入事件追蹤器
    @pyqtSlot(str)
    def handle_js_call(self, result):
        if self.main_window.event_log:
            selected_text = self.main_window.selected_text_to_record
            event_info = f"反白內容: {result}"
            self.main_window.event_log.append(event_info)
            self.main_window.append_action(event_info)
            #只顯示XPATH路徑
            xpath = result.split(',')[1][:-1]
            self.return_path_signal.emit(xpath)