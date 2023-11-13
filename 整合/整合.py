import sys
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QLineEdit, QPushButton, QHBoxLayout, QLabel, QFileDialog, QSplitter
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSlot, QDateTime, QTimer, QUrl
from PyQt6.QtCore import Qt
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from pynput import mouse, keyboard
from datetime import datetime
import threading
import time
from PyQt6 import QtCore
import subprocess
import os
import re


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

        # self.show()

    def update_display(self):
        # 實時更新滑鼠座標
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


class WebBrowserWindow(QMainWindow):
    scraping_done_signal = QtCore.pyqtSignal()  # 定義一個信號，用於通知爬蟲操作已完成

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.drivers = None
        self.selected_xpath = None
        self.selected_xpath = []
        self.xpath = None
        self.scraping_in_progress = False
        self.script_dir = os.path.dirname(os.path.realpath(__file__))
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
        # self.show()

        # 創建 Web 瀏覽器視窗
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('https://www.google.com.tw'))
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

        self.send_xpath_button = QPushButton("資料傳送", self)
        self.send_xpath_button.clicked.connect(self.send_xpath_to_server)  # 設定按鈕點擊事件處理函數
        self.send_xpath_button.setFixedSize(80, 30)

        # 創建返回按鈕
        self.back_button = QPushButton("返回", self)
        self.back_button.clicked.connect(self.browser.back)
        self.back_button.setFixedSize(80, 30)

        # 創建查詢資料按鈕
        self.serch_button = QPushButton("查詢資料", self)
        # self.serch_button.clicked.connect(self.browser.back)  #還沒好
        self.serch_button.setFixedSize(80, 30)

        # 創建開始爬蟲按鈕
        self.scraping_button = QPushButton("開始爬蟲", self)
        self.scraping_button.clicked.connect(self.scrape_data)  
        self.scraping_button.setFixedSize(80, 30)

        # 創建登出按鈕
        self.logout_button = QPushButton("登出", self)
        # self.logout_button.clicked.connect(self.logout_data)  #還沒好
        self.logout_button.setFixedSize(80, 30)

        # 使用者名稱      還沒好
    # ////////////////////////////////////////////////////////////
        self.account_label = QLabel('帳號:', self)
    # ////////////////////////////////////////////////////////////

        # 創建一個水平佈局並將按鈕添加到其中
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.record_highlight_button)
        button_layout.addWidget(self.send_xpath_button)
        button_layout.addWidget(self.scraping_button)
        button_layout.addWidget(self.serch_button)
        button_layout.addStretch(1) #將按鈕推到左邊
        
        button_layout.addWidget(self.account_label)
        button_layout.addWidget(self.logout_button)
        
        # 主佈局包含其他小部件和水平佈局
        layout = QVBoxLayout()
        layout.addWidget(self.urlbar)
        layout.addWidget(self.browser)
        layout.addLayout(button_layout)  

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    # 瀏覽器導向輸入的 URL
    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == '':
            q.setScheme('http')
        self.browser.setUrl(q)

    # 更新 URL 地址欄的文字
    def renew_urlbar(self, q):
        new_url = q.toString()
        self.urlbar.setText(new_url)
        self.urlbar.setCursorPosition(0)

        # 在這裡記錄新的 URL 到事件日誌文件
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

    # 處理網頁選擇文本事件
    def handle_selection_changed(self):
        selected_text = self.browser.page().selectedText()
        if selected_text:
            self.main_window.set_selected_text_to_record(selected_text)

    # 顯示反白文本的元素資訊
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
            
            selectedText + ' , {' + path + '}';
            '''
            self.browser.page().runJavaScript(js_code, self.handle_js_call)
            
    @pyqtSlot(str)
    def handle_js_call(self, result):
        if self.main_window.event_log:
            selected_text = self.main_window.selected_text_to_record
            event_info = f"反白內容: {result}"
            self.main_window.event_log.append(event_info)
            self.main_window.append_action(event_info)

            data = re.search(r'\{(.+?)\}', result)
            extracted_content = data.group(1)
            # 只顯示 XPATH 路徑
            self.selected_xpath.append(extracted_content)

    # 添加一個新方法，用於將所有抓取到的內容一次性傳送
    def send_xpath_to_server(self):
        # 將 self.selected_xpath 轉換為字符串列表
        xpath_list = [str(xpath) for xpath in self.selected_xpath]
        response = subprocess.run(['python', os.path.join(self.script_dir, 'Backend_wiring_Xpath.py'), str(xpath_list)], stdout=subprocess.PIPE)
        stdout_str = response.stdout.decode('utf-8')
        self.xpath = stdout_str.split('+')[0][:-1]
        self.selected_xpath = []

    # 執行爬蟲操作
    def scrape_data(self):
        if self.scraping_in_progress:
            return  # 如果已經有爬蟲操作在運行，則不執行新的操作

        self.scraping_in_progress = True  # 設定標誌變數，表示爬蟲操作正在進行中

        self.scraping_button.setEnabled(False)
        self.scraping_button.setText("正在爬蟲...")
        self.results = []  # 儲存爬蟲結果的列表

        def scrape_in_thread():
            drivers = webdriver.Chrome()
            drivers.get(self.browser.url().toString())
            # eles = drivers.find_elements(By.XPATH, self.get_xpath)
            # self.results = [ele.text for ele in eles]
            # print(f"爬蟲結果: {self.results}")
            # drivers.quit()

            # 初始化迴圈索引
            n = 1

            while True:
                # 構造標題的 XPATH
                xpath = self.xpath + f"[{n}]"

                try:
                    # 使用 find_element_by_xpath 找到標題元素
                    title_element = drivers.find_element(By.XPATH, xpath)

                    # 獲取標題文本
                    title_text = title_element.text

                    # 顯示標題
                    print(f"爬蟲結果 {n}: {title_text}")

                    # 增加迴圈索引
                    n += 1
                    xpath = None

                except NoSuchElementException:
                    # 找不到元素時退出迴圈
                    break

            # 爬蟲完成後，使用信號更新 UI
            self.scraping_done_signal.emit()

            self.scraping_button.setText("爬蟲")  # 恢復按鈕文字
            self.scraping_button.setEnabled(True)  # 啟用「爬蟲」按鈕

            self.scraping_in_progress = False  # 重置標誌變數，表示爬蟲操作已完成

        # 在單獨的線程中執行爬蟲操作
        self.scraping_thread = threading.Thread(target=scrape_in_thread)
        self.scraping_thread.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = MainWindow()
    web_browser_window = WebBrowserWindow(main_window)


    # 使用 QSplitter 將瀏覽器窗口放在左邊，MainWindow 放在右邊
    splitter = QSplitter()
    splitter.addWidget(web_browser_window)
    splitter.addWidget(main_window)
    splitter.setSizes([600, 300])  # 設置初始寬度比例

    window = QMainWindow()
    window.setCentralWidget(splitter)
    window.setWindowTitle('Icrawler')
    window.showMaximized()  # 最大化顯示
    web_browser_window.scraping_button.clicked.connect(web_browser_window.scrape_data)

    app.exec()