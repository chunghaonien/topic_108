from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
import sys
import json

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('我的瀏覽器')
        self.setWindowIcon(QIcon('icons/penguin.png'))
        self.resize(1200, 800)  # 調整視窗大小
        self.setStyleSheet('''
            QMainWindow {
                background-color: #f0f0f0;
            }
            QToolBar {
                background-color: #333;
                color: white;
            }
            QPushButton {
                background-color: #008CBA;
                color: white;
                border: none;
                padding: 5px 10px;
                margin: 2px;
            }
            QLineEdit {
                background-color: white;
                border: 1px solid #ccc;
                padding: 5px;
            }
        ''')
        self.show()

        # 新增瀏覽器
        self.browser = QWebEngineView()
        url = 'https://www.google.com'
        # 指定要開啟的網頁 URL
        self.browser.setUrl(QUrl(url))
        # 將瀏覽器加入視窗中心
        self.setCentralWidget(self.browser)

        # 新增頂部導航列
        navigation_bar = QToolBar('導航')
        # 設定圖示大小
        navigation_bar.setIconSize(QSize(16, 16))
        # 將導航列加入視窗中
        self.addToolBar(navigation_bar)

        back_button = QPushButton('返回')
        next_button = QPushButton('前進')
        reload_button = QPushButton('重新載入')

        back_button.clicked.connect(self.browser.back)
        next_button.clicked.connect(self.browser.forward)
        reload_button.clicked.connect(self.browser.reload)

        navigation_bar.addWidget(back_button)
        navigation_bar.addWidget(next_button)
        navigation_bar.addWidget(reload_button)

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)

        navigation_bar.addSeparator()
        navigation_bar.addWidget(self.urlbar)

        self.browser.urlChanged.connect(self.renew_urlbar)
        self.browser.selectionChanged.connect(self.handle_selection_changed)
        self.start_pos = None
        self.end_pos = None
        self.selected_text = None

        

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == '':
            q.setScheme('http')
        self.browser.setUrl(q)

    def renew_urlbar(self, q):
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    # 處理滑鼠點擊事件
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_pos = event.pos()
            self.end_pos = None

    # 處理滑鼠釋放事件
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.end_pos = event.pos()
            self.show_element_info()

    # 解析元素資訊
    def show_element_info(self):
        if self.start_pos and self.end_pos:
            rect = QRect(self.start_pos, self.end_pos).normalized()
            js_code = f'''
            var elem = document.elementFromPoint({rect.center().x()}, {rect.center().y()});
            if (elem) {{
                var rect = elem.getBoundingClientRect();
                var elementInfo = {{
                    tag: elem.tagName,
                    id: elem.id,
                    class: elem.className,
                    x: rect.left,
                    y: rect.top,
                    width: rect.width,
                    height: rect.height
                }};
                window.pyqtBoundFunction(JSON.stringify(elementInfo));
            }}
            '''
            self.browser.page().runJavaScript(js_code)

    # 處理 JavaScript 呼叫的函式
    @pyqtSlot(str)
    def handle_js_call(self, result):
        element_info = json.loads(result)
        print('點擊的元素：')
        print(f'標籤：{element_info["tag"]}')
        print(f'ID：{element_info["id"]}')
        print(f'類別：{element_info["class"]}')
        print(f'位置：({element_info["x"]}, {element_info["y"]})')
        print(f'大小：{element_info["width"]} x {element_info["height"]}')

    # 處理選取的文字事件
    def handle_selection_changed(self):
        selected_text = self.browser.page().selectedText()
        if selected_text:
            print(f'選取的文字：{selected_text}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec_()
