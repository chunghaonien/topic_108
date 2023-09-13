import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTextEdit, QLineEdit, QToolBar
from PyQt5.QtCore import Qt, QSize, QUrl, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QObject

class EventTracker(QObject):
    mouse_clicked = pyqtSignal(int, int, int)
    mouse_released = pyqtSignal(int, int, int)
    mouse_drag = pyqtSignal(int, int, int, int, int)
    mouse_wheel = pyqtSignal(int)
    key_pressed = pyqtSignal(int)
    key_released = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.mouse_start_pos = None
        self.mouse_end_pos = None

    def track_mouse_click(self, x, y, buttons):
        self.mouse_clicked.emit(x, y, buttons)

    def track_mouse_release(self, x, y, buttons):
        self.mouse_released.emit(x, y, buttons)

    def track_mouse_drag(self, x_start, y_start, x_end, y_end, buttons):
        self.mouse_drag.emit(x_start, y_start, x_end, y_end, buttons)

    def track_mouse_wheel(self, delta):
        self.mouse_wheel.emit(delta)

    def track_key_press(self, key):
        self.key_pressed.emit(key)

    def track_key_release(self, key):
        self.key_released.emit(key)

class EventTrackerWindow(QMainWindow):
    def __init__(self, event_tracker):
        super().__init__()
        self.event_tracker = event_tracker
        self.init_ui()
        self.event_log = []

    def init_ui(self):
        self.setWindowTitle('事件追蹤工具')
        self.setWindowIcon(QIcon('icons/penguin.png'))
        self.resize(300, 300)
        self.setStyleSheet('''  
            QMainWindow {
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #008CBA;
                color: white;
                border: none;
                padding: 5px 10px;
                margin: 2px;
            }
        ''')
        self.show()

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.log_text)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.event_tracker.mouse_clicked.connect(self.track_mouse_click)
        self.event_tracker.mouse_released.connect(self.track_mouse_release)
        self.event_tracker.mouse_drag.connect(self.track_mouse_drag)
        self.event_tracker.mouse_wheel.connect(self.track_mouse_wheel)
        self.event_tracker.key_pressed.connect(self.track_key_press)
        self.event_tracker.key_released.connect(self.track_key_release)

    def track_mouse_click(self, x, y, buttons):
        self.event_log.append(f"Mouse clicked at ({x}, {y}) - Buttons: {buttons}")
        self.update_log()

    def track_mouse_release(self, x, y, buttons):
        self.event_log.append(f"Mouse released at ({x}, {y}) - Buttons: {buttons}")
        self.update_log()

    def track_mouse_drag(self, x_start, y_start, x_end, y_end, buttons):
        self.event_log.append(f"Mouse drag from ({x_start}, {y_start}) to ({x_end}, {y_end}) - Buttons: {buttons}")
        self.update_log()

    def track_mouse_wheel(self, delta):
        self.event_log.append(f"Mouse wheel scrolled: {delta}")
        self.update_log()

    def track_key_press(self, key):
        self.event_log.append(f"Key pressed: {Qt.Key(key)}")
        self.update_log()

    def track_key_release(self, key):
        self.event_log.append(f"Key released: {Qt.Key(key)}")
        self.update_log()

    def update_log(self):
        self.log_text.setPlainText('\n'.join(self.event_log))

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

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('https://www.google.com'))
        self.setCentralWidget(self.browser)

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

        # 在這裡連接滑鼠事件
        self.browser.mousePressEvent = self.mousePressEvent
        self.browser.mouseReleaseEvent = self.mouseReleaseEvent
        self.browser.mouseMoveEvent = self.mouseMoveEvent
        self.browser.wheelEvent = self.wheelEvent

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

    def mousePressEvent(self, event):
        x = event.x()
        y = event.y()
        buttons = event.buttons()
        self.event_tracker.track_mouse_click(x, y, buttons)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        x = event.x()
        y = event.y()
        buttons = event.buttons()
        self.event_tracker.track_mouse_release(x, y, buttons)
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self.event_tracker.mouse_start_pos:
            x_start = self.event_tracker.mouse_start_pos.x()
            y_start = self.event_tracker.mouse_start_pos.y()
            x_end = event.x()
            y_end = event.y()
            buttons = event.buttons()
            self.event_tracker.track_mouse_drag(x_start, y_start, x_end, y_end, buttons)
        super().mouseMoveEvent(event)

    def wheelEvent(self, event):
        delta = event.angleDelta().y() / 120
        self.event_tracker.track_mouse_wheel(delta)
        super().wheelEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    event_tracker = EventTracker()
    event_tracker_window = EventTrackerWindow(event_tracker)
    web_browser_window = WebBrowserWindow(event_tracker)
    app.exec_()
