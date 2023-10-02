import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QFileDialog
from PyQt5.QtCore import Qt, pyqtSlot
import threading
import time


class ActionPlayer(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 400, 300)
        self.setWindowTitle('Action Player')

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)

        self.load_button = QPushButton('讀取文件', self)
        self.load_button.clicked.connect(self.load_file)

        self.start_button = QPushButton('開始', self)
        self.start_button.clicked.connect(self.start_execution)

        self.clear_button = QPushButton('清除', self)
        self.clear_button.clicked.connect(self.clear_text)

        self.stop_button = QPushButton('停止', self)
        self.stop_button.clicked.connect(self.stop_execution)

        vbox = QVBoxLayout()
        vbox.addWidget(self.text_edit)
        vbox.addWidget(self.load_button)
        vbox.addWidget(self.start_button)
        vbox.addWidget(self.clear_button)
        vbox.addWidget(self.stop_button)

        self.setLayout(vbox)

        self.actions = []  # 存放動作的列表
        self.is_executing = False
        self.execution_thread = None

        self.show()

    def load_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "讀取文件", "", "文本檔案 (*.txt);;所有檔案 (*)", options=options)

        if file_name:
            with open(file_name, 'r') as file:
                self.actions = [line.strip() for line in file.readlines()]
                self.display_actions()

    def display_actions(self):
        self.text_edit.clear()
        for action in self.actions:
            self.text_edit.append(action)

    def start_execution(self):
        if not self.is_executing:
            self.is_executing = True
            self.execution_thread = threading.Thread(target=self.execute_actions)
            self.execution_thread.start()

    def execute_actions(self):
        for action in self.actions:
            if not self.is_executing:
                break

            # 根據需要執行動作，這裡只是暫停一段時間模擬執行
            self.highlight_action(action, 'blue')
            time.sleep(1)  # 可以根據實際需求調整
            self.clear_highlight()

        self.is_executing = False

    def stop_execution(self):
        self.is_executing = False
        if self.execution_thread:
            self.execution_thread.join()  # 等待執行緒結束
            self.execution_thread = None

    def clear_text(self):
        self.text_edit.clear()

    def highlight_action(self, action, color):
        # 在 HTML 文本中使用 span 標籤來設置顏色
        colored_action = f'<span style="color:{color}">{action}</span>'
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertHtml(colored_action)

    def clear_highlight(self):
        # 將文字框的內容轉換為純文本
        plain_text = self.text_edit.toPlainText()
        self.text_edit.clear()
        self.text_edit.append(plain_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = ActionPlayer()
    sys.exit(app.exec_())
