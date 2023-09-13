import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor

class SecondaryWindow(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('副視窗')
        self.setGeometry(100, 100, 400, 300)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        self.log_text = QTextEdit()
        layout.addWidget(self.log_text)

        self.show()

    def track_mouse_event(self, event):
        if self.main_window:
            self.log_text.append(f"Mouse event in Main Window - Pos: {event.pos()} - Buttons: {event.buttons()}")

    def track_key_event(self, event):
        if self.main_window:
            self.log_text.append(f"Key event in Main Window - Key: {event.key()}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.secondary_window = None

    def init_ui(self):
        self.setWindowTitle('主視窗')
        self.setGeometry(200, 200, 400, 300)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.open_secondary_button = QPushButton('打開副視窗')
        layout.addWidget(self.open_secondary_button)

        self.open_secondary_button.clicked.connect(self.open_secondary_window)

    def open_secondary_window(self):
        if not self.secondary_window:
            self.secondary_window = SecondaryWindow(self)
            self.secondary_window.show()

    def mousePressEvent(self, event):
        if self.secondary_window:
            self.secondary_window.track_mouse_event(event)
        super().mousePressEvent(event)

    def keyPressEvent(self, event):
        if self.secondary_window:
            self.secondary_window.track_key_event(event)
        super().keyPressEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
