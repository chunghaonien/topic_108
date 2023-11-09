import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QMessageBox
import requests

class LoginWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.login_button = QPushButton("Login")
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        self.setLayout(layout)

class MyApp(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        
        self.setStyle("fusion")  # 设置应用程序的样式为"fusion"
        
        self.login_widget = LoginWidget()
        self.login_widget.login_button.clicked.connect(self.login)
        self.login_widget.show()

    def login(self):
        username = self.login_widget.username_input.text()
        password = self.login_widget.password_input.text()
        
        # 向Flask应用发送HTTP POST请求以进行登录验证
        url = "http://127.0.0.1:5000/login"
        data = {"username": username, "password": password}
        response = requests.post(url, data=data)
        
        if response.status_code == 200:
            QMessageBox.information(self.login_widget, "Login Successful", f"Welcome, {username}!")
        else:
            QMessageBox.critical(self.login_widget, "Login Failed", "Invalid username or password. Please try again.")

if __name__ == "__main__":
    app = MyApp(sys.argv)
    app.exec()
