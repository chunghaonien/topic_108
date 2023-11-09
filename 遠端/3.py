import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
import subprocess

class Communicate(QObject):
    mySignal = pyqtSignal()

class MyWindow(QWidget):
    def __init__(self, communicator):
        super().__init__()

        self.communicator = communicator
        self.script_dir = os.path.dirname(os.path.realpath(__file__))  # 在這裡定義 script_dir

        button = QPushButton("按我！", self)
        button.clicked.connect(self.onButtonClicked)

    def onButtonClicked(self):
        self.communicator.mySignal.emit()

        # 使用 self.script_dir
        subprocess.run(["python", os.path.join(self.script_dir, "4.py")])

if __name__ == "__main__":
    app = QApplication(sys.argv)

    communicator = Communicate()

    window1 = MyWindow(communicator)

    window1.show()

    sys.exit(app.exec())
