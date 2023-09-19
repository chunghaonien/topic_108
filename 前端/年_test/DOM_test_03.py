import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtCore import QUrl
from datetime import datetime

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

class WebBrowserWindow(QMainWindow):
    def __init__(self, event_tracker):
        super().__init__()
        self.event_tracker = event_tracker
        self.selected_element_xpath = ""  # 將成員變數移到 __init__ 方法中
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

        layout = QVBoxLayout()
        layout.addWidget(self.urlbar)
        layout.addWidget(self.browser)
        layout.addWidget(self.record_highlight_button)

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
                    if (element.id) {
                        name += '[@id="' + element.id + '"]';
                        path.unshift(name);
                        break;
                    } else {
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
                }
                return 'html/' + path.join('/');
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    event_tracker = EventTracker()
    web_browser_window = WebBrowserWindow(event_tracker)
    app.exec_()
