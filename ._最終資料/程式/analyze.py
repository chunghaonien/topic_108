import sys
import asyncio
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHBoxLayout
from PyQt6.QtCore import QThread, pyqtSignal
from Backend_wiring_analyze import main_async
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import json
import ast

class AsyncRunner(QThread):
    def __init__(self, user_id, data_signal, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.data_signal = data_signal
        self.data = None # 新增一個屬性來儲存數據

    def run(self):
        asyncio.run(self.async_task())

    async def async_task(self):
        self.data = await main_async(self.user_id)
        self.data_signal.emit() # 只發送訊號，不傳遞數據

class MyMainWindow(QMainWindow):
    data_received = pyqtSignal() # 定義一個新的訊號

    def __init__(self, user_id):
        super().__init__()
        self.init_ui()
        self.data_received.connect(self.populate_table) # 將訊號連接到 populate_table
        self.start_async_task(user_id)

    def init_ui(self):
        self.setWindowTitle("Data Analysis Application")
        self.setGeometry(100, 100, 980, 600) # 可能需要調整大小以更好地適應內容

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # 使用水平佈局
        layout = QHBoxLayout(self.central_widget)

        # 建立表格
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['日期(月)', '網站', '次數'])
        layout.addWidget(self.table)

        # 建立 matplotlib 圖表
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # 繪製測試圓餅圖
        labels = '0'
        sizes = [1]
        self.ax.pie(sizes, labels=labels, autopct='%1.1f%%')
        self.canvas.draw()

    def start_async_task(self, user_id):
        self.async_runner = AsyncRunner(user_id, self.data_received)
        self.data_received.connect(self.populate_table) # 連結訊號
        self.async_runner.start()

    def populate_table(self):
        data = self.async_runner.data # 取得數據

        try:
            # 嘗試將字串轉換為列表
            data = ast.literal_eval(data)
        except Exception as e:
            print(f"Error converting data: {e}")
            return

        if isinstance(data,list):
            self.table.setRowCount(len(data))
            for row, (date, website, count) in enumerate(data):
                self.table.setItem(row, 0, QTableWidgetItem(date))
                self.table.setItem(row, 1, QTableWidgetItem(website))
                self.table.setItem(row, 2, QTableWidgetItem(count))
        else:
            print("Data is not a list:", data)

        # 在表格填入後繪製圓餅圖
        self.update_pie_chart()

    def update_pie_chart(self):
        # 提取網站名稱和次數
        labels = []
        sizes = []
        for row in range(self.table.rowCount()):
            website = self.table.item(row, 1).text() # 第二列是網站名
            count = int(self.table.item(row,2).text()) # 第三列是次數
            labels.append(website)
            sizes.append(count)

        # 清除現有的圖表
        self.ax.clear()

        # 繪製圓餅圖
        if sizes:
            self.ax.pie(sizes, labels=labels, autopct='%1.1f%%')

        # 重新繪製
        self.canvas.draw()
                
# 從標準輸入讀取 user_id
if __name__ == '__main__':
    app = QApplication(sys.argv)
    user_id = sys.stdin.readline().strip()
    # user_id = "1"
    mainWin = MyMainWindow(user_id)
    mainWin.show()
    sys.exit(app.exec())