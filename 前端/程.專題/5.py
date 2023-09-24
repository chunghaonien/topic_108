import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QLineEdit, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import QFile
from datetime import datetime

# 定義一個用於追蹤事件的類別
class EventTracker(QObject):
    mouse_wheel = pyqtSlot(int)
    key_pressed = pyqtSlot(int)
    key_released = pyqtSlot(int)

    def __init__(self):
        super().__init__()
        self.event_log = []
        self.current_log_file = self.create_log_file()
        self.selected_text_to_record = ""

    def create_log_file(self):
        now = datetime.now()
        file_name = now.strftime("event_log_%Y-%m-%d_%H-%M-%S.txt")
        return file_name

    def save_to_file(self, event_info):
        with open(self.current_log_file, "a", encoding="utf-8") as f:
            f.write(event_info + "\n")

    def update_log(self):
        pass

    # 追蹤按鍵按下事件
    def track_key_press(self, key):
        event_info = f"Key pressed: {Qt.Key(key)}"
        self.event_log.append(event_info)
        self.update_log()
        self.save_to_file(event_info)

    # 追蹤按鍵釋放事件
    def track_key_release(self, key):
        event_info = f"Key released: {Qt.Key(key)}"
        self.event_log.append(event_info)
        self.update_log()
        self.save_to_file(event_info)

    # 追蹤滾輪滾動事件
    def track_mouse_wheel(self, delta):
        event_info = f"Mouse wheel scrolled: {delta}"
        self.event_log.append(event_info)
        self.update_log()
        self.save_to_file(event_info)

    def set_selected_text_to_record(self, text):
        self.selected_text_to_record = text

    def record_selected_text(self):
        if self.selected_text_to_record:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"{timestamp}: 選擇的文字: {self.selected_text_to_record}\n"
            self.event_log.append(log_entry)
            self.save_to_file(log_entry)
            self.selected_text_to_record = ""

# 定義瀏覽器窗口類別
class WebBrowserWindow(QMainWindow):
    def __init__(self, event_tracker):
        super().__init__()
        self.event_tracker = event_tracker
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

        # 創建記錄反白文本和元素資訊的按鈕
        self.record_highlight_button = QPushButton("反白元素", self)
        self.record_highlight_button.clicked.connect(self.show_element_info)
        self.record_highlight_button.setFixedSize(80, 30)
        # 創建獲取網址的按鈕
        self.get_url_button = QPushButton("獲取網址", self)
        self.get_url_button.clicked.connect(self.get_current_url)
        self.get_url_button.setFixedSize(80, 30)

        # 創建返回按鈕
        self.back_button = QPushButton("返回", self)
        self.back_button.clicked.connect(self.browser.back)
        self.back_button.setFixedSize(80, 30)

        # 創建一個水平佈局並將按鈕添加到其中
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.record_highlight_button)
        button_layout.addWidget(self.get_url_button)
        button_layout.addStretch(1) #將按鈕推到左邊

        # 主佈局包含其他小部件和水平佈局
        layout = QVBoxLayout()
        layout.addWidget(self.urlbar)
        layout.addWidget(self.browser)
        layout.addLayout(button_layout)  

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    # 定義 navigate_to_url 方法，用於將瀏覽器導向輸入的 URL
    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == '':
            q.setScheme('http')
        self.browser.setUrl(q)

    # 定義 renew_urlbar 方法，用於更新 URL 地址欄的文字
    def renew_urlbar(self, q):
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    # 定義 keyPressEvent 方法，用於追蹤按鍵按下事件並呼叫 event_tracker
    def keyPressEvent(self, event):
        key = event.key()
        self.event_tracker.track_key_press(key)
        super().keyPressEvent(event)

    # 定義 keyReleaseEvent 方法，用於追蹤按鍵釋放事件並呼叫 event_tracker
    def keyReleaseEvent(self, event):
        key = event.key()
        self.event_tracker.track_key_release(key)
        super().keyReleaseEvent(event)

    # 定義 handle_selection_changed 方法，用於處理網頁選擇文本事件
    def handle_selection_changed(self):
        selected_text = self.browser.page().selectedText()
        if selected_text:
            self.event_tracker.set_selected_text_to_record(selected_text)

    # 定義 show_element_info 方法，用於顯示反白文本的元素資訊
    def show_element_info(self):
        selected_text = self.event_tracker.selected_text_to_record
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
        if self.event_tracker.selected_text_to_record:
            selected_text = self.event_tracker.selected_text_to_record
            event_info = f"反白內容: {result}"
            print(event_info)
            self.event_tracker.save_to_file(event_info)

    # 定義 get_current_url 方法，用於獲取當前網頁的網址並記錄到 event_log.txt 中
    def get_current_url(self):
        current_url = self.browser.url().toString()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp}: 當前網址: {current_url}\n"
        self.event_tracker.event_log.append(log_entry)
        self.event_tracker.save_to_file(log_entry)

    # 定義 load_js_file 方法，用於載入並執行指定的 JavaScript 檔案
    def load_js_file(self, file_path):
        # 創建 QFile 實例
        js_file = QFile(file_path)

        # 打開文件
        if js_file.open(QFile.ReadOnly | QFile.Text):
            # 讀取JavaScript文件並將其載入到瀏覽器中
            js_code = str(js_file.readAll(), encoding='utf-8')
            self.browser.page().runJavaScript(js_code)
            # 關閉文件
            js_file.close()
        else:
            print(f"無法打開JavaScript文件: {js_file.errorString()}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    event_tracker = EventTracker()
    web_browser_window = WebBrowserWindow(event_tracker)

    # 載入JavaScript文件
    js_file_path = 'run_recorded_events.js'
    web_browser_window.load_js_file(js_file_path)

    app.exec_()
