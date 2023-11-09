from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QDialog
import sys

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.main_window = None
        self.initUI()
        
    def initUI(self):
        self.login_button = QPushButton('登入', self)
        self.login_button.clicked.connect(self.login_clicked)

        self.register_button = QPushButton('註冊', self)
        self.register_button.clicked.connect(self.register_clicked)

        layout = QVBoxLayout()
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)
        self.setLayout(layout)
        
        self.show()

    def login_clicked(self):
        self.hide()
        if self.main_window is None:
            self.main_window = MainWindow()
        self.main_window.show()

    def register_clicked(self):
        self.hide()
        if self.main_window is None:
            self.main_window = MainWindow()
        self.main_window.show()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.event_log = []
        self.initUI()

    def initUI(self):
        pass
        self.setGeometry(100, 100, 400, 300)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    login_dialog = LoginDialog()
    login_dialog.setWindowTitle('登入')
    
    app.exec()
