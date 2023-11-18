import sys
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QLineEdit, QPushButton, QHBoxLayout, QLabel, QFileDialog, QSplitter, QDialog
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSlot, QDateTime, QTimer, QUrl ,QThread
from PyQt6.QtCore import Qt
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
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
        self.xoffset = 0
        self.yoffset = 0
        self.initUI()
        
    def initUI(self):
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('使用者動作')

        self.mouse_label = QLabel(self)
        self.keyboard_text_edit = QTextEdit(self)
        self.keyboard_text_edit.setReadOnly(True)

        self.start_button = QPushButton('開始記錄', self)
        self.start_button.clicked.connect(self.start_capture)

        self.save_buttom = QPushButton('下載', self)
        self.save_buttom.clicked.connect(self.save_data)

        vbox = QVBoxLayout()
        vbox.addWidget(self.mouse_label)
        vbox.addWidget(self.keyboard_text_edit)
        vbox.addWidget(self.start_button)
        vbox.addWidget(self.save_buttom)

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
        if button == mouse.Button.left or button == mouse.Button.right:
            button_text = "左鍵" if button == mouse.Button.left else "右鍵"
            
            if pressed:
                if self.is_capturing and not self.start_button.isChecked():  # 按下開始記錄且沒有按下開只記錄按鈕
                    self.append_action(f"滑鼠點擊：({x}, {y})，按鍵：{button_text}")
                    self.xoffset = x
                    self.yoffset = y
                    self.stop_capture()  # 停止記錄
            else:
                # 如果是松開事件，不做任何處理
                pass

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

# /////////////////////////////////////////////////////////////////////////////////

class WebBrowserWindow(QMainWindow):
    def __init__(self, main_window, username, user_id):
        super().__init__()
        self.main_window = main_window
        self.drivers = None
        self.selected_xpath = None
        self.selected_xpath = []
        self.selected_button_xpath = None
        self.xpath = None
        self.scraping_in_progress = False
        self.script_dir = os.path.dirname(os.path.realpath(__file__))
        self.init_ui()
        self.username = username
        self.user_id = user_id

    def init_ui(self):
        # 設置窗口標題和圖示
        self.setWindowTitle('網頁瀏覽器')
        # self.setWindowIcon(QIcon('icons/penguin.png'))
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
        self.record_highlight_button = QPushButton("反白文字", self)
        self.record_highlight_button.clicked.connect(self.show_element_info)
        self.record_highlight_button.setFixedSize(80, 30)

        # 創建傳送資料按鈕
        self.send_xpath_button = QPushButton("反白比對", self)
        self.send_xpath_button.clicked.connect(self.send_xpath_to_server)  # 設定按鈕點擊事件處理函數
        self.send_xpath_button.setFixedSize(80, 30)
        self.send_xpath_button.setEnabled(False)  # 初始狀態設為不可用
        self.send_xpath_button.setStyleSheet("background-color: #CCCCCC; color: #555555;")  # 灰色樣式

        # 創建返回按鈕
        self.back_button = QPushButton("返回上頁", self)
        self.back_button.clicked.connect(self.browser.back)
        self.back_button.setFixedSize(80, 30)

        # 創建查詢資料按鈕
        self.serch_button = QPushButton("查詢資料", self)
        self.serch_button.clicked.connect(self.open_table)  
        self.serch_button.setFixedSize(80, 30)

        # 創建開始爬蟲按鈕
        self.scraping_button = QPushButton("開始爬蟲", self)
        self.scraping_button.clicked.connect(ScrapingDialog)
        self.scraping_button.setFixedSize(80, 30)
        self.scraping_button.setEnabled(False)  # 初始狀態設為不可用
        self.scraping_button.setStyleSheet("background-color: #CCCCCC; color: #555555;")  # 灰色樣式

        # 創建登出按鈕
        self.logout_button = QPushButton("登出", self)
        self.logout_button.clicked.connect(self.logout) 
        self.logout_button.setFixedSize(80, 30)

        # 用戶名標籤
        self.account_label = QLabel(f'用戶名:{username}', self)
        self.user_id = QLabel(f'用戶id:{user_id}', self)

        # 創建一個水平佈局並將按鈕添加到其中
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.record_highlight_button)
        button_layout.addWidget(self.send_xpath_button)
        button_layout.addWidget(self.scraping_button)
        button_layout.addStretch(1) #將按鈕推到左邊

        button_layout.addWidget(self.user_id)
        button_layout.addWidget(self.account_label)
        button_layout.addWidget(self.serch_button)
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

    def open_table(self):
        # self.close()
        # QApplication.closeAllWindows()
        
        # 創建 searchDialog 實例，傳入 main_window 參數
        dialog_instance = SearchDialog(main_window=self)

        # 呼叫顯示對話框的方法
        dialog_instance.exec()

        script_path = os.path.join(self.script_dir, "table.py")
        input_data = f"{self.username},{self.user_id}".encode('gbk')
        process = subprocess.Popen(["python", script_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(input=input_data)


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

    # 登出
    def logout(self):
        self.close()
        QApplication.closeAllWindows()    
        subprocess.Popen(["python", os.path.join(self.script_dir, "main.py")])

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
            
            # 在反白按鈕觸發後，將查詢資料和開始爬蟲按鈕設置為可用
            self.send_xpath_button.setEnabled(True)     #資料傳送
            self.send_xpath_button.setStyleSheet("")    # 移除樣式，恢復預設外觀
            
            
    @pyqtSlot(str)
    def handle_js_call(self, result):
        if self.main_window.event_log:
            selected_text = self.main_window.selected_text_to_record
            event_info = f"反白內容: {result}"
            self.main_window.event_log.append(event_info)
            self.main_window.append_action(event_info)

            data = re.search(r'\{(.+?)\}', result)
            extracted_content = data.group(1)
            self.selected_xpath.append(extracted_content)

    # 添加一個新方法，用於將所有抓取到的內容一次性傳送
    def send_xpath_to_server(self):
        # 將 self.selected_xpath 轉換為字符串列表
        xpath_list = [str(xpath) for xpath in self.selected_xpath]
        response = subprocess.run(['python', os.path.join(self.script_dir, 'Backend_wiring_Xpath.py'), str(xpath_list)], stdout=subprocess.PIPE)
        if response.stdout is not None:
            stdout_str = response.stdout.decode('utf-8')
            self.xpath = stdout_str.split('+')[0][0:-1]
        else:
            print('Error')
            
        self.selected_xpath = []

        self.scraping_button.setEnabled(True)       #開始爬蟲按鈕
        self.scraping_button.setStyleSheet("")      # 移除樣式，恢復預設外觀

# ////////////////////////////////////////////////////////////////////////////

# 爬蟲需求畫面
class ScrapingDialog(QDialog):
    scraping_done_signal = QtCore.pyqtSignal()  # 定義一個信號，用於通知爬蟲操作已完成\

    def __init__(self, main_window, browser_window = None):
        super().__init__()
        self.browser_window = browser_window
        self.main_window = main_window
        self.scraped_data = []
        self.script_dir = os.path.dirname(os.path.realpath(__file__))
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        scraping_layout = QVBoxLayout()
        self.scraping_label = QLabel('需要爬幾頁:', self)
        self.scraping_textbox = QLineEdit(self)

        scraping_layout.addWidget(self.scraping_label)
        scraping_layout.addWidget(self.scraping_textbox)

        buttons_layout = QHBoxLayout()
        scraping_button = QPushButton('確認', self)
        scraping_button.setFixedSize(80, 30)
        scraping_button.clicked.connect(self.scrape_data)
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(scraping_button)

        layout.addLayout(scraping_layout)
        layout.addLayout(buttons_layout)
        layout.addStretch()

        self.setLayout(layout)
        
        self.setGeometry(500, 100, 200, 100)
        self.setWindowTitle('爬取需求')

    # 執行爬蟲操作
    def scrape_data(self):
        self.close()
        repeat_count = int(self.scraping_textbox.text())

        if self.browser_window.scraping_in_progress:
            return  # 如果已經有爬蟲操作在運行，則不執行新的操作

        self.browser_window.scraping_in_progress = True  # 設定標誌變數，表示爬蟲操作正在進行中

        self.browser_window.scraping_button.setEnabled(False)
        self.browser_window.scraping_button.setText("正在爬蟲...")

        self.browser_window.drivers = webdriver.Chrome()
        self.browser_window.drivers.maximize_window()
        self.browser_window.drivers.get(self.browser_window.browser.url().toString())

        def scrape_in_thread():
            # 初始化迴圈索引
            n = 1
            while True:
                if self.browser_window.drivers is None:
                    break  # WebDriver 會話已經關閉，退出迴圈
                
                # 構造標題的 XPATH
                xpath = self.browser_window.xpath + f"[{n}]"

                try:
                    # 將 xpath 字符串轉換為 By.XPATH 對象
                    xpath_locator = (By.XPATH, xpath)
                    # 使用 find_element_by_xpath 找到標題元素
                    title_element = self.browser_window.drivers.find_element(*xpath_locator)

                    # 獲取標題文本
                    title_text = title_element.text
                    # 顯示標題
                    self.scraped_data.append(f"第{n}筆: {title_text}")

                    # 增加迴圈索引
                    n += 1

                except NoSuchElementException:
                    # 找不到元素時退出迴圈
                    break
                except StaleElementReferenceException:
                    # 元素過時，重新查找元素
                    continue
        # 開始重複執行爬取
        try:
            for i in range(1, repeat_count+1):
                # 在單獨的線程中執行爬蟲操作
                self.scraped_data.append(f"第{i}頁: ")
                self.scraping_thread = threading.Thread(target=scrape_in_thread)
                self.scraping_thread.start()

                try:
                    #滾動至頁面最底
                    self.scroll_to_bottom()
                    try:
                        # 尋找並點擊下一頁按鈕
                        actions = ActionChains(self.browser_window.drivers)
                        actions.move_by_offset((int(self.main_window.xoffset) + 300), (int(self.main_window.yoffset) - 50)).click().perform()
                        # 初始滑鼠座標至(0, 0)
                        actions.move_by_offset(-(int(self.main_window.xoffset) + 300), -(int(self.main_window.yoffset) - 50)).perform()
                    except:
                        pass

                    i += 1
                except:
                    pass
        except Exception as e:
            print(f"發生錯誤：{e}")
        finally:
            # 關閉瀏覽器
            with self.browser_window.drivers as driver:
                driver.quit()
            # 爬蟲結果上傳DB
            self.upload_result()
            # 爬蟲完成後，使用信號更新 UI
            self.scraping_done_signal.emit()
            self.browser_window.scraping_button.setText("爬蟲完成")
            time.sleep(4)
            self.browser_window.scraping_button.setText("開始爬蟲")  # 恢復按鈕文字
            self.browser_window.scraping_button.setEnabled(True)  # 啟用「爬蟲」按鈕

            self.browser_window.scraping_in_progress = False  # 重置標誌變數，表示爬蟲操作已完成

    def scroll_to_bottom(self):
        # 使用 JavaScript 模擬滾輪滑動到底部
        self.browser_window.drivers.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # 等待一段時間，讓新資料加載完成

    def upload_result(self):
        subprocess.run(['python', os.path.join(self.script_dir, 'Backend_wiring_upload.py'), str(self.browser_window.user_id), str(self.scraped_data)], stdout=subprocess.PIPE)
        self.scraped_data = []

#////////////////////////////////////////////////////////////////////////////

class SearchDialog(QDialog):
    def __init__(self, main_window, browser_window = None):
        super().__init__()
        self.browser_window = browser_window
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        serch_layout = QVBoxLayout()
        self.serch_label = QLabel('進入後先按下查詢，就可獲得資料', self)
        
        serch_layout.addWidget(self.serch_label)
        
        buttons_layout = QHBoxLayout()
        serch_button = QPushButton('確認', self)
        serch_button.setFixedSize(80, 30)
        serch_button.clicked.connect(self.serch_close)
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(serch_button)

        layout.addLayout(serch_layout)
        layout.addLayout(buttons_layout)
        layout.addStretch()

        self.setLayout(layout)
        
        self.setGeometry(800, 500, 300, 100)
        self.setWindowTitle('使用手冊')

    def serch_close(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    
    # user_data = sys.stdin.read().strip()
    user_data = "test,1"

    username = user_data.split(',')[0]
    user_id = user_data.split(',')[1]

    main_window = MainWindow()
    browser_window = WebBrowserWindow(main_window, username, user_id)

    # 使用 QSplitter 將瀏覽器窗口放在左邊，MainWindow 放在右邊
    splitter = QSplitter()
    splitter.addWidget(browser_window)
    splitter.addWidget(main_window)
    splitter.setSizes([600, 300])  # 設置初始寬度比例

    window = QMainWindow()
    window.setCentralWidget(splitter)
    window.setWindowTitle('iCrawler')
    window.showMaximized()  # 最大化顯示
    browser_window.scraping_button.clicked.connect(lambda: ScrapingDialog(main_window, browser_window).exec())

    app.exec()