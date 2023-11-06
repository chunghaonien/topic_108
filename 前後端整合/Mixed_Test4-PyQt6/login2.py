from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QDialog
import sys

class LoginDialog(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()
        
    def initUI(self):
        self.login_button = QPushButton('登入', self)
        self.login_button.clicked.connect(self.login_clicked)

        self.register_button = QPushButton('註冊', self)
        self.register_button.clicked.connect(self.register_clicked)

        self.init_function_ui(visible=False)

        layout = QVBoxLayout()
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)
        self.setLayout(layout)
        
        self.show()

    def init_function_ui(self, visible=False):
        # Initialize function UI elements here
        pass

    def login_clicked(self):
        self.init_function_ui(visible=True)
        self.hide()
        self.main_window.show()

    def register_clicked(self):
        self.init_function_ui(visible=True)
        self.hide()
        self.main_window.show()

    def start_capture(self):
        # Implement start capture functionality
        pass

    def pause_capture(self):
        # Implement pause capture functionality
        pass

    def stop_capture(self):
        # Implement stop capture functionality
        pass

    def save_data(self):
        # Implement save data functionality
        pass
    
        
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.event_log = []
        self.initUI()

    def initUI(self):
        # Initialize the main window UI here
        pass
        self.show()    
if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = MainWindow()
    login_dialog = LoginDialog(main_window)

    main_window.setWindowTitle('使用者動作')
    main_window.setGeometry(100, 100, 400, 300)

    app.exec()
