from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QDialog, QLabel, QHBoxLayout, QLineEdit
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
        
        self.resize(400, 300)
        self.show()

    def login_clicked(self):
        self.hide()
        if self.main_window is None:
            self.main_window = LoggedInPage()
        self.main_window.setWindowTitle('登入')
        self.main_window.show()

    def register_clicked(self):
        self.hide()
        if self.main_window is None:
            self.main_window = RegisterPage()
        self.main_window.setWindowTitle('註冊')
        self.main_window.show()

class LoggedInPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 帳號欄位
        account_layout = QHBoxLayout()
        account_label = QLabel('帳號', self)
        account_textbox = QLineEdit(self)
        account_layout.addWidget(account_label)
        account_layout.addWidget(account_textbox)
        layout.addLayout(account_layout)

        # 密碼欄位
        password_layout = QHBoxLayout()
        password_label = QLabel('密碼', self)
        password_textbox = QLineEdit(self)
        password_layout.addWidget(password_label)
        password_layout.addWidget(password_textbox)
        layout.addLayout(password_layout)
        
        # 返回按鈕
        return_button = QPushButton('返回', self)
        return_button.clicked.connect(self.return_to_login)
        return_button.setFixedSize(80, 30)
        layout.addWidget(return_button)
        
        self.setLayout(layout)
        self.setGeometry(500, 100, 500, 500)  # 設視窗大小及位置

    def return_to_login(self):
        self.hide()
        login_dialog.show()

class RegisterPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 帳號欄位
        account_layout = QHBoxLayout()
        account_label = QLabel('帳號', self)
        account_textbox = QLineEdit(self)
        account_layout.addWidget(account_label)
        account_layout.addWidget(account_textbox)
        layout.addLayout(account_layout)

        # 密碼欄位
        password_layout = QHBoxLayout()
        password_label = QLabel('密碼', self)
        password_textbox = QLineEdit(self)
        password_layout.addWidget(password_label)
        password_layout.addWidget(password_textbox)
        layout.addLayout(password_layout)

        # 返回按鈕
        return_button = QPushButton('返回', self)
        return_button.clicked.connect(self.return_to_register)
        return_button.setFixedSize(80, 30)
        layout.addWidget(return_button)

        self.setLayout(layout)
        self.setGeometry(500, 100, 500, 500)  # 設視窗大小及位置

    def return_to_register(self):
        self.hide()
        login_dialog.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    login_dialog = LoginDialog()
    login_dialog.setWindowTitle('登入與註冊')
    
    app.exec()
