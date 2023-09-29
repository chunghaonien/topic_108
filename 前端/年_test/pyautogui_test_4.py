import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QLineEdit, QPushButton
from PyQt5.QtCore import Qt, QObject, pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from datetime import datetime
import pyautogui

class EventTracker(QObject):
    def __init__(self):
        super().__init__()
        self.event_log = []
        self.current_log_file = self.create_log_file()
        self.selected_text_to_record = ""
        self.recording = False

    def create_log_file(self):
        now = datetime.now()
        file_name = now.strftime("event_log_%Y-%m-%d_%H-%M-%S.txt")
        return file_name

    def save_to_file(self, event_info):
        with open(self.current_log_file, "a", encoding="utf-8") as f:
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

    def set_selected_text_to_record(self, text):
        self.selected_text_to_record = text

    def record_selected_text(self):
        if self.selected_text_to_record:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"{timestamp}: 選擇的文字: {self.selected_text_to_record}\n"
            self.event_log.append(log_entry)
            self.save_to_file(log_entry)
            self.selected_text_to_record = ""

    def start_recording(self):
        self.recording = True
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp}: 開始錄製\n"
        self.save_to_file(log_entry)

    def stop_recording(self):
        if self.recording:
            self.recording = False
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"{timestamp}: 結束錄製\n"
            self.save_to_file(log_entry)
            self.update_log()

    def record_mouse_click(self, x, y):
        if self.recording:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"{timestamp}: 滑鼠點擊 - X: {x}, Y: {y}\n"
            self.save_to_file(log_entry)
            self.mouse_click_positions.append((x, y))
            pyautogui.click(x, y)  # 在滑鼠點擊的同時實際執行滑鼠點擊

class WebBrowserWindow(QMainWindow):
    def __init__(self, event_tracker):
        super().__init__()
        self.event_tracker = event_tracker
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

        self.record_highlight_button = QPushButton("記錄反白和元素資訊", self)
        self.record_highlight_button.clicked.connect(self.show_element_info)

        self.start_record_button = QPushButton("開始錄製", self)
        self.start_record_button.clicked.connect(self.start_recording)

        self.stop_record_button = QPushButton("結束錄製", self)
        self.stop_record_button.clicked.connect(self.stop_recording)

        layout = QVBoxLayout()
        layout.addWidget(self.urlbar)
        layout.addWidget(self.browser)
        layout.addWidget(self.selected_text_editor)
        layout.addWidget(self.record_highlight_button)
        layout.addWidget(self.start_record_button)
        layout.addWidget(self.stop_record_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

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

    def handle_selection_changed(self):
        selected_text = self.browser.page().selectedText()
        if selected_text:
            self.event_tracker.set_selected_text_to_record(selected_text)

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

    @pyqtSlot(str)
    def handle_js_call(self, result):
        if self.event_tracker.selected_text_to_record:
            selected_text = self.event_tracker.selected_text_to_record
            event_info = f"反白內容: {result}"
            print(event_info)
            self.event_tracker.save_to_file(event_info)

    def start_recording(self):
        self.event_tracker.start_recording()

    def stop_recording(self):
        self.event_tracker.stop_recording()

    def mousePressEvent(self, event):
        if self.event_tracker.recording:
            x, y = event.x(), event.y()
            self.event_tracker.record_mouse_click(x, y)
            pyautogui.click(x, y)  # 在滑鼠點擊的同時實際執行滑鼠點擊
        super().mousePressEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    event_tracker = EventTracker()
    web_browser_window = WebBrowserWindow(event_tracker)
    app.exec_()

