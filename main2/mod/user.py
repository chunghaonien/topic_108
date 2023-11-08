import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QStackedWidget, QMessageBox
import mysql.connector

# ...（之前的代码）

class MyApp(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        
        self.setStyle("fusion")  # 设置应用程序的样式为"fusion"
        
        self.stack = QStackedWidget()
        self.login_widget = LoginWidget()
        self.main_window = MainWindow()
        self.stack.addWidget(self.login_widget)
        self.stack.addWidget(self.main_window)
        
        self.stack.setCurrentWidget(self.login_widget)
        
        self.login_widget.login_button.clicked.connect(self.switch_to_main_window)

    def switch_to_main_window(self):
        # 获取输入的用户名和密码
        username = self.login_widget.username_input.text()
        password = self.login_widget.password_input.text()
        
        # 调用登录验证函数
        if login(username, password):
            self.stack.setCurrentWidget(self.main_window)
            self.main_window.show()  # 显示主窗口
        else:
            QMessageBox.critical(self.main_window, "Login Failed", "Invalid username or password. Please try again.")

if __name__ == "__main__":
    app = MyApp(sys.argv)
    app.exec()
