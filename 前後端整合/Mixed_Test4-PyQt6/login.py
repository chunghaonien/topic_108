import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QLineEdit, QPushButton, QHBoxLayout, QLabel, QFileDialog, QSplitter, QDialog
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtCore import QTimer
from PyQt6.QtCore import QUrl, QDateTime
from PyQt6.QtGui import QIcon, QTextCursor
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('登入系統')
        self.setGeometry(200, 200, 300, 150)

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText('使用者名稱')
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('密碼')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_button = QPushButton('登入', self)
        self.register_button = QPushButton('註冊', self)

        layout = QVBoxLayout()
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

class WebBrowserWindow(QMainWindow):
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

        self.scraping_button = QPushButton("爬蟲", self)
        self.scraping_button.clicked.connect(self.scrape_data)
        self.scraping_button.setFixedSize(80, 30)

        self.back_button = QPushButton("返回", self)
        self.back_button.clicked.connect(self.browser.back)
        self.back_button.setFixedSize(80, 30)

        self.log_in_out_button = QPushButton("登入註冊", self)
        self.log_in_out_button.clicked.connect(self.show_login_dialog)
        self.log_in_out_button.setFixedSize(80, 30)

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.urlbar)
        button_layout.addWidget(self.browser)
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

        log_entry = f" 網頁: {new_url}\n"
        self.main_window.event_log.append(log_entry)
        self.main_window.append_action(log_entry)

    def log_url_change(self, url):
        if url.isValid():
            url_text = url.toString()
            timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
            log_entry = f"{timestamp}: 網頁 URL 變化 - {url_text}\n"
            self.main_window.event_log.append(log_entry)

    def handle_selection_changed(self):
        selected_text = self.browser.page().selectedText()
        if selected_text:
            self.main_window.set_selected_text_to_record(selected_text)

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
            
    @pyqtSlot(str)
    def handle_js_call(self, result):
        if self.main_window.event_log:
            selected_text = self.main_window.selected_text_to_record
            event_info = f"反白內容: {result}"
            self.main_window.event_log.append(event_info)
            self.main_window.append_action(event_info)
            xpath = result.split(',')[1][:-1]
            self.selected_xpath = xpath

    def scrape_data(self):
        if self.scraping_in_progress:
            return

        self.scraping_in_progress = True
        self.scraping_button.setEnabled(False)
        self.scraping_button.setText("正在爬蟲...")
        self.results = []

        def scrape_in_thread():
            drivers = webdriver.Chrome()
            drivers.get(self.browser.url().toString())
            eles = drivers.find_elements(By.XPATH, self.selected_xpath)
            self.results = [ele.text for ele in eles]
            print(f"爬蟲結果: {self.results}")
            drivers.quit()

            self.scraping_done_signal.emit()

            self.scraping_button.setText("爬蟲")
            self.scraping_button.setEnabled(True)

            self.scraping_in_progress = False

        self.scraping_thread = threading.Thread(target=scrape_in_thread)
        self.scraping_thread.start()

    def show_login_dialog(self):
        self.login_dialog = LoginDialog()
        result = self.login_dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            # 登入成功，執行相應操作
            pass

class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
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
        self.actions = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_display)

        self.mouse_listener = None
        self.keyboard_listener = None

        self.start_time = None

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
                if elapsed_time > 0.1:
                    self.append_action(f"滑鼠拖移：({x}, {y})，按鍵：{button_text}")
                else:
                    self.append_action(self.mouse_state)

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
                    time.sleep(0.1)
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
        options |= QFileDialog.DialogOption.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "儲存檔案", "", "文本檔案 (*.txt);;所有檔案 (*)", options=options)

        if file_name:
            with open(file_name, 'w') as file:
                for time, action in self.actions:
                    file.write(f"{time} {action}\n")

    def save_to_file(self, event_info):
        with open('event_log.txt', 'a') as file:
            file.write(event_info + '\n')

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = MainWindow()
    web_browser_window = WebBrowserWindow(main_window)

    splitter = QSplitter()
    splitter.addWidget(web_browser_window)
    splitter.addWidget(main_window)
    splitter.setSizes([600, 300])

    window = QMainWindow()
    window.setCentralWidget(splitter)
    window.setWindowTitle('Integrated Window')
    window.showMaximized()

    app.exec()
