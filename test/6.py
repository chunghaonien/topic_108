from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QDialog, QLabel, QHBoxLayout, QLineEdit
from PyQt6.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout
from PyQt6.QtGui import QFont, QPalette, QColor
from PyQt6.QtCore import Qt
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

# //////////////////////////////////////////////////註冊///////////////////////////////////////////////////
# 註冊畫面
class RegisterPage(QDialog):
    def __init__(self, loginDialog, communicator):
        super().__init__()
        self.loginDialog = loginDialog
        self.script_dir = os.path.dirname(os.path.realpath(__file__))
        self.communicator = communicator
        self.get_register_state = ""
        self.initUI()

    def initUI(self):
        self.setWindowTitle("註冊")
        self.setGeometry(100, 100, 300, 250)
        self.setFont(QFont("微軟正黑體", 10))

        # 更新顏色方案
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
        palette.setColor(QPalette.ColorRole.Button, QColor(200, 200, 200))
        self.setPalette(palette)

        layout = QVBoxLayout()

        form_layout = QFormLayout()

        # 帳號欄位
        self.account_textbox = QLineEdit(self)
        form_layout.addRow(QLabel("帳號:"), self.account_textbox)

        # 密碼欄位
        self.password_textbox = QLineEdit(self)
        self.password_textbox.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow(QLabel("密碼:"), self.password_textbox)

        # 確認密碼欄位
        self.confirm_password_textbox = QLineEdit(self)
        self.confirm_password_textbox.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow(QLabel("確認密碼:"), self.confirm_password_textbox)

        # 暱稱欄位
        self.username_textbox = QLineEdit(self)
        form_layout.addRow(QLabel("暱稱:"), self.username_textbox)

        # 註冊按鈕
        register_button = QPushButton("註冊", self)
        register_button.clicked.connect(self.onRegisterButtonClicked)
        form_layout.addRow(register_button)

        layout.addLayout(form_layout)
        self.setLayout(layout)

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
            register_confirm_password_popup = Register_confirm_password(self, self.communicator, self.account_textbox, self.password_textbox, self.username_textbox)
            register_confirm_password_popup.exec()
        else:
            response = subprocess.run(["python", os.path.join(self.script_dir, "Backend_wiring_register.py"), account, password, username], stdout=subprocess.PIPE)
            decoded1_response = response.stdout.decode()
            self.get_register_state = decoded1_response


            if self.get_register_state[0:4] == "True":
                register_success_popup = Register_yes(self, self.communicator, self.account_textbox, self.password_textbox, self.username_textbox)
                register_success_popup.exec()
            else:
                register_success_popup = Register_no(self, self.communicator, self.account_textbox, self.password_textbox, self.confirm_password_textbox, self.username_textbox)
                register_success_popup.exec()

# 判定密碼是否相同畫面
class Register_confirm_password(QDialog):
    def __init__(self, loginDialog, communicator, account_textbox, password_textbox, username_textbox):
        super().__init__()
        self.loginDialog = loginDialog
        self.script_dir = os.path.dirname(os.path.realpath(__file__))
        self.communicator = communicator
        self.account_textbox = account_textbox
        self.password_textbox = password_textbox
        self.username_textbox = username_textbox
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        log_layout = QVBoxLayout()
        self.log_label = QLabel('密碼不相同', self)
        log_layout.addWidget(self.log_label)

        buttons_layout = QHBoxLayout()
        confirm_button = QPushButton('確認', self)
        confirm_button.setFixedSize(80, 30)
        confirm_button.clicked.connect(self.onRegisterButtonClicked_password)
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(confirm_button)

        layout.addLayout(log_layout)
        layout.addLayout(buttons_layout)
        layout.addStretch()

        self.setLayout(layout)
        
        self.setGeometry(500, 100, 200, 100)
        self.setWindowTitle('密碼不相同')

    def onRegisterButtonClicked_password(self):
        self.close()
        self.loginDialog.show()

# 註冊成功畫面          
class Register_yes(QDialog):
    def __init__(self, loginDialog, communicator, account_textbox, password_textbox, username_textbox):
        super().__init__()
        self.loginDialog = loginDialog
        self.script_dir = os.path.dirname(os.path.realpath(__file__))
        self.communicator = communicator
        self.account_textbox = account_textbox
        self.password_textbox = password_textbox
        self.username_textbox = username_textbox
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        log_layout = QVBoxLayout()
        self.log_label = QLabel('註冊成功', self)
        log_layout.addWidget(self.log_label)

        buttons_layout = QHBoxLayout()
        login_button = QPushButton('確認', self)
        login_button.setFixedSize(80, 30)
        login_button.clicked.connect(self.onRegisterButtonClicked_yes)
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(login_button)

        layout.addLayout(log_layout)
        layout.addLayout(buttons_layout)
        layout.addStretch()

        self.setLayout(layout)
        
        self.setGeometry(500, 100, 200, 100)
        self.setWindowTitle('註冊成功')
        self.show()

    def onRegisterButtonClicked_yes(self):
        QApplication.closeAllWindows()
        login_dialog.show()
        

# 註冊失敗畫面
class Register_no(QDialog):
    def __init__(self, loginDialog, communicator, account_textbox, password_textbox, confirm_password_textbox, username_textbox):
        super().__init__()
        self.loginDialog = loginDialog
        self.registerPage = RegisterPage
        self.script_dir = os.path.dirname(os.path.realpath(__file__))
        self.communicator = communicator
        self.account_textbox = account_textbox
        self.password_textbox = password_textbox
        self.confirm_password_textbox = confirm_password_textbox
        self.username_textbox = username_textbox
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        log_layout = QVBoxLayout()
        self.log_label = QLabel('註冊失敗', self)
        log_layout.addWidget(self.log_label)

        buttons_layout = QHBoxLayout()
        login_button = QPushButton('確認', self)
        login_button.setFixedSize(80, 30)
        login_button.clicked.connect(self.onRegisterButtonClicked_no)
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(login_button)

        layout.addLayout(log_layout)
        layout.addLayout(buttons_layout)
        layout.addStretch()

        self.setLayout(layout)
        
        self.setGeometry(500, 100, 200, 100)
        self.setWindowTitle('註冊失敗')
        self.show()

    def onRegisterButtonClicked_no(self):
        self.account_textbox.setText('')
        self.password_textbox.setText('')
        self.confirm_password_textbox.setText('')
        self.username_textbox.setText('')
        self.close()


# /////////////////////////////////////////////////登入////////////////////////////////////////////////////////

# 初始登入畫面
class LoginDialog(QDialog):
    def __init__(self, communicator):
        super().__init__()
        self.communicator = communicator
        self.script_dir = os.path.dirname(os.path.realpath(__file__))  # 在這裡定義 script_dir
        self.get_login_state = ""
        self.initUI()
        self.username = ""

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

    #有可能有亂碼
    def onLoginButtonClicked(self):
        account = self.account_textbox.text()
        password = self.password_textbox.text()
        
        if account == "" or password == "":
            login_success_popup = login_password(self, self.communicator, self.account_textbox, self.password_textbox)
            login_success_popup.exec()
            return
        
        response = subprocess.run(["python", os.path.join(self.script_dir, "Backend_wiring_login.py"), account, password], stdout=subprocess.PIPE)

        try:
            decoded2_response = response.stdout.decode('gbk')
        except UnicodeDecodeError:
            decoded2_response = response.stdout.decode('utf-8', errors='replace')

        evaluated_data = eval(decoded2_response)
        
        if evaluated_data == False:
            self.get_login_state = "False"
        else:
            if isinstance(evaluated_data, tuple) and len(evaluated_data) == 2:
                result = [str(evaluated_data[0])]
                sublist = evaluated_data[1]
                if sublist and len(sublist) > 0:
                    inner_tuple = sublist[0]
                    result.extend(map(str, inner_tuple))

            self.get_login_state = result

        if self.get_login_state[0] == "True":

            self.username = self.get_login_state[1]
            self.user_id = self.get_login_state[2]

            login_success_popup = login_yes(self, self.communicator, self.account_textbox, self.password_textbox, self.username, self.user_id)
            login_success_popup.exec()
        else:
            login_success_popup = login_no(self, self.communicator, self.account_textbox, self.password_textbox)
            login_success_popup.exec()

# 登入成功畫面
class login_yes(QDialog):
    def __init__(self, loginDialog, communicator, account_textbox, password_textbox, username, user_id):
        super().__init__()
        self.loginDialog = loginDialog
        self.script_dir = os.path.dirname(os.path.realpath(__file__))
        self.communicator = communicator
        self.account_textbox = account_textbox
        self.password_textbox = password_textbox
        self.username = username
        self.user_id = user_id
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        log_layout = QVBoxLayout()
        self.log_label = QLabel(f'登入成功，用戶名:{self.username}', self)
        log_layout.addWidget(self.log_label)

        buttons_layout = QHBoxLayout()
        login_button = QPushButton('確認', self)
        login_button.setFixedSize(80, 30)
        login_button.clicked.connect(self.onLoginButtonClicked_yes)
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(login_button)

        layout.addLayout(log_layout)
        layout.addLayout(buttons_layout)
        layout.addStretch()

        self.setLayout(layout)
        
        self.setGeometry(500, 100, 200, 100)
        self.setWindowTitle('登入成功')
        self.show()

    def onLoginButtonClicked_yes(self):
        self.close()
        QApplication.closeAllWindows()
        
        script_path = os.path.join(self.script_dir, "整合.py")
        input_data = f"{self.username},{self.user_id}".encode('gbk')
        process = subprocess.Popen(["python", script_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(input=input_data)

# 沒輸入帳號密碼畫面
class login_password(QDialog):
    def __init__(self, loginDialog, communicator, account_textbox, password_textbox):
        super().__init__()
        self.loginDialog = loginDialog
        self.script_dir = os.path.dirname(os.path.realpath(__file__))
        self.communicator = communicator
        self.account_textbox = account_textbox
        self.password_textbox = password_textbox
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        log_layout = QVBoxLayout()
        self.log_label = QLabel('請輸入帳號密碼', self)
        log_layout.addWidget(self.log_label)

        buttons_layout = QHBoxLayout()
        login_button = QPushButton('確認', self)
        login_button.setFixedSize(80, 30)
        login_button.clicked.connect(self.onLoginButtonClicked)
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(login_button)

        layout.addLayout(log_layout)
        layout.addLayout(buttons_layout)
        layout.addStretch()

        self.setLayout(layout)
        
        self.setGeometry(500, 100, 200, 100)
        self.setWindowTitle('請輸入帳號密碼')
        self.show()

    def onLoginButtonClicked(self):
        self.close()
        self.loginDialog.show()

# 登入失敗畫面
class login_no(QDialog):
    def __init__(self, loginDialog, communicator, account_textbox, password_textbox):
        super().__init__()
        self.loginDialog = loginDialog
        self.script_dir = os.path.dirname(os.path.realpath(__file__))
        self.communicator = communicator
        self.account_textbox = account_textbox
        self.password_textbox = password_textbox
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        log_layout = QVBoxLayout()
        self.log_label = QLabel('登入失敗', self)
        log_layout.addWidget(self.log_label)

        buttons_layout = QHBoxLayout()
        login_button = QPushButton('確認', self)
        login_button.setFixedSize(80, 30)
        login_button.clicked.connect(self.onLoginButtonClicked)
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(login_button)

        layout.addLayout(log_layout)
        layout.addLayout(buttons_layout)
        layout.addStretch()

        self.setLayout(layout)
        
        self.setGeometry(500, 100, 200, 100)
        self.setWindowTitle('登入失敗')
        self.show()

    def onLoginButtonClicked(self):
        self.close()
        self.loginDialog.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    communicator = Communicate()
    login_dialog = LoginDialog(communicator)  # 將 communicator 傳遞給 LoginDialog 的構造函式

    app.exec()