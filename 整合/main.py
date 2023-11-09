from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QDialog, QLabel, QHBoxLayout, QLineEdit
import sys
import websockets
import asyncio
from PyQt6.QtCore import QTimer
from PyQt6.QtCore import QObject, pyqtSignal
import subprocess
import os

class Communicate(QObject):
    RegisterSignal = pyqtSignal(str, str, str)
    LoginSignal = pyqtSignal(str, str)

class RegisterPage(QDialog):
    def __init__(self, loginDialog, communicator):
        super().__init__()
        self.loginDialog = loginDialog
        self.script_dir = os.path.dirname(os.path.realpath(__file__))
        self.communicator = communicator
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 帳號欄位
        account_layout = QHBoxLayout()
        self.account_label = QLabel('帳號', self)
        self.account_textbox = QLineEdit(self)
        account_layout.addWidget(self.account_label)
        account_layout.addWidget(self.account_textbox)
        layout.addLayout(account_layout)

        # 密碼欄位
        password_layout = QHBoxLayout()
        self.password_label = QLabel('密碼', self)
        self.password_textbox = QLineEdit(self)
        password_layout.addWidget(self.password_label)
        password_layout.addWidget(self.password_textbox)
        layout.addLayout(password_layout)

        # 確認密碼欄位
        confirm_password_layout = QHBoxLayout()
        self.confirm_password_label = QLabel('確認密碼', self)
        self.confirm_password_textbox = QLineEdit(self)
        confirm_password_layout.addWidget(self.confirm_password_label)
        confirm_password_layout.addWidget(self.confirm_password_textbox)
        layout.addLayout(confirm_password_layout)

        # 暱稱欄位
        username_layout = QHBoxLayout()
        self.username_label = QLabel('暱稱', self)
        self.username_textbox = QLineEdit(self)
        username_layout.addWidget(self.username_label)
        username_layout.addWidget(self.username_textbox)
        layout.addLayout(username_layout)
        
        # 水平布局來放置返回按鈕和確定按鈕
        buttons_layout = QHBoxLayout()

        # 確定按鈕
        yes_button = QPushButton('確定', self)
        yes_button.setFixedSize(80, 30)
        yes_button.clicked.connect(self.onRegisterButtonClicked)  # 連接到新的方法

        # 將兩個按鈕放入水平佈局中
        buttons_layout.addWidget(yes_button)
        buttons_layout.addStretch(1)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)
        self.setGeometry(500, 100, 500, 300)  # 設視窗大小及位置
        self.setWindowTitle('註冊')
        self.show()

    def return_to_login(self):
        self.close()
        self.loginDialog.show()

    def onRegisterButtonClicked(self):
        account = self.account_textbox.text()
        password = self.password_textbox.text()
        confirm_password = self.confirm_password_textbox.text()
        username = self.username_textbox.text()
        
        #驗證密碼是否相同
        if (password != confirm_password):
            print("密碼不相同")
            self.open_register_page()
        else:
            self.communicator.RegisterSignal.emit(account, password, username)
            subprocess.Popen(["python", os.path.join(self.script_dir, "Backend_wiring_register.py"), account, password, username])
            self.return_to_login()

class LoginDialog(QDialog):
    def __init__(self, communicator):
        super().__init__()
        self.initUI()
        self.communicator = communicator
        self.script_dir = os.path.dirname(os.path.realpath(__file__))  # 在這裡定義 script_dir

        
    def initUI(self):
        layout = QVBoxLayout()

        # 帳號欄位
        account_layout = QHBoxLayout()
        self.account_label = QLabel('帳號', self)
        self.account_textbox = QLineEdit(self)
        account_layout.addWidget(self.account_label)
        account_layout.addWidget(self.account_textbox)
        layout.addLayout(account_layout)

        # 密碼欄位
        password_layout = QHBoxLayout()
        self.password_label = QLabel('密碼', self)
        self.password_textbox = QLineEdit(self)
        password_layout.addWidget(self.password_label)
        password_layout.addWidget(self.password_textbox)
        layout.addLayout(password_layout)
        
        # 水平布局來放置返回按鈕和確定按鈕
        buttons_layout = QHBoxLayout()

        # 登入按鈕
        login_button = QPushButton('登入', self)
        login_button.setFixedSize(80, 30)
        login_button.clicked.connect(self.onLoginButtonClicked)  # 使用包裝後的函數

        # 註冊按鈕
        register_button = QPushButton('註冊', self)
        register_button.clicked.connect(self.open_register_page)
        register_button.setFixedSize(80, 30)

        # 將兩個按鈕放入水平佈局中
        buttons_layout.addWidget(login_button)
        buttons_layout.addWidget(register_button)
        buttons_layout.addStretch(1)

        layout.addLayout(buttons_layout)
        layout.addWidget(register_button)

        self.setLayout(layout)
        self.setGeometry(500, 100, 500, 300)  # 設視窗大小及位置
        self.setWindowTitle('登入')
        self.show()
    
    def open_register_page(self):
        register_page = RegisterPage(self, self.communicator)
        register_page.exec()
    
    def onLoginButtonClicked(self):
        account = self.account_textbox.text()
        password = self.password_textbox.text()

        self.communicator.LoginSignal.emit(account, password)
        subprocess.Popen(["python", os.path.join(self.script_dir, "Backend_wiring_login.py"), account, password])

    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    communicator = Communicate()
    login_dialog = LoginDialog(communicator)  # 將 communicator 傳遞給 LoginDialog 的構造函式


    app.exec()

