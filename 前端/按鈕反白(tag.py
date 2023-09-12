from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
import sys


class WebEnginePage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        pass

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('我的瀏覽器')
        self.setWindowIcon(QIcon('icons/penguin.png'))
        self.resize(1200, 800)
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
        self.browser.setUrl(QUrl(url))
        self.setCentralWidget(self.browser)

        # 新增頂部導航列
        navigation_bar = QToolBar('導航')
        navigation_bar.setIconSize(QSize(16, 16))
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

        # 新增底部状态栏
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)

        # 新增按鈕
        self.get_tag_button = QPushButton('獲取反白區域的標籤')
        self.get_tag_button.clicked.connect(self.show_element_info)
        status_bar.addWidget(self.get_tag_button)

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == '':
            q.setScheme('http')
        self.browser.setUrl(q)

    def renew_urlbar(self, q):
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    def handle_selection_changed(self):
        self.selected_text = self.browser.page().selectedText()

    def show_element_info(self):
        if self.selected_text:
            js_code = '''
            function getPathTo(element) {
                if (element.id !== '')
                    return 'id("' + element.id + '")';
                if (element === document.body)
                    return element.tagName;

                var ix = 0;
                var siblings = element.parentNode.childNodes;
                for (var i = 0; i < siblings.length; i++) {
                    var sibling = siblings[i];
                    if (sibling === element)
                        return getPathTo(element.parentNode) + '/' + element.tagName + '[' + (ix + 1) + ']';
                    if (sibling.nodeType === 1 && sibling.tagName === element.tagName)
                        ix++;
                }
            }

            var span = document.createElement('span');
            var range = window.getSelection().getRangeAt(0);
            range.surroundContents(span);

            var path = getPathTo(span);
            span.outerHTML = span.innerHTML;

            path;
            '''
            self.browser.page().runJavaScript(js_code, self.handle_js_call)

    @pyqtSlot(str)
    def handle_js_call(self, result):
        if self.selected_text:
            print('選取的元素標籤：', result)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec_()
