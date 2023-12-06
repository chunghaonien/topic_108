import sys
import matplotlib
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# 设置 matplotlib 字体
matplotlib.rcParams['font.family'] = 'SimHei'
matplotlib.rcParams['font.size'] = 10
matplotlib.rcParams['axes.unicode_minus'] = False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        # 创建 matplotlib 图表
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        # 添加到布局
        layout.addWidget(self.canvas)

        # 绘制圆餅圖
        labels = 'ptt', 'case B', 'case C'
        sizes = [3, 1, 1]
        self.ax.pie(sizes, labels=labels, autopct='%1.1f%%')

        self.canvas.draw()

app = QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec())
