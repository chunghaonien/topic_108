import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTableWidget, QTableWidgetItem, QWidget, QSplitter, QSizePolicy, QHeaderView
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# PyQt6 主視窗包含表格的類別
class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 設置主視窗的大小和標題
        self.setGeometry(500, 100, 1200, 800)
        self.setWindowTitle('PyQt6 表格和圖表範例')

        # 創建主佈局
        main_layout = QVBoxLayout()

        # 創建表格
        table = QTableWidget(self)
        table.setColumnCount(3)
        table.setRowCount(5)
        table.setHorizontalHeaderLabels(['列 1', '列 2', '列 3'])
        
        # 在表格中添加示例數據
        for row in range(5):
            for col in range(3):
                item = QTableWidgetItem(f'項目 {row + 1}-{col + 1}')
                item.setTextAlignment(0x0004 | 0x0080)  # AlignCenter | AlignVCenter
                table.setItem(row, col, item)

        # 設置表格的大小策略，Expanding表示表格會擴展以填滿所有可用空間
        table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # 將表格列的寬度設置為Stretch，使其平均分擔可用的寬度
        for col in range(3):
            table.horizontalHeader().setSectionResizeMode(col, QHeaderView.ResizeMode.Stretch)

        # 將表格添加到主佈局，同時設置stretch以使表格擁有可用空間
        main_layout.addWidget(table, stretch=1)

        # 創建一個 QWidget 作為主視窗的中央部件
        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)

        # 將中央部件設置為主視窗的中央部件
        self.setCentralWidget(central_widget)


# 設置 matplotlib 字體
matplotlib.rcParams['font.family'] = 'SimHei'
matplotlib.rcParams['font.size'] = 10
matplotlib.rcParams['axes.unicode_minus'] = False

# Matplotlib 主視窗包含圓餅圖的類別
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        # 創建 matplotlib 圖表
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        # 添加到佈局
        layout.addWidget(self.canvas)

        # 繪製圓餅圖
        labels = 'ptt', '案例 B', '案例 C'
        sizes = [3, 1, 1]
        self.ax.pie(sizes, labels=labels, autopct='%1.1f%%')

        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # 創建兩個主視窗
    main_window = MyMainWindow()
    wwindow = MainWindow()
    
    # 使用 QSplitter 將兩個視窗組合在一起
    splitter = QSplitter()
    splitter.addWidget(main_window)
    splitter.addWidget(wwindow)
    splitter.setSizes([500, 400])  # 設置初始寬度比例

    # 創建一個新的主視窗，將 QSplitter 設置為中央部件
    window = QMainWindow()
    window.setCentralWidget(splitter)
    window.setWindowTitle('iCrawler')
    window.showMaximized()  # 最大化顯示
    app.exec()
