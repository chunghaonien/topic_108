from PyQt6.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QLabel, QHeaderView, QInputDialog, QMessageBox, QLineEdit, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt, QAbstractTableModel, QVariant
import sys
import subprocess
import os
import datetime
import json  
import csv
from subprocess import Popen, PIPE, STDOUT
import ast
import asyncio
from Backend_wiring_select import main_async
import re

headers = ["user_id", "scrape_time", "scrape_data"]
rows = []

class Analyze(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("分析資料")
        self.setGeometry(100, 100, 800, 600)
        self.show()

        # 創建主視窗的水平佈局
        main_layout = QHBoxLayout()

        # 創建左側的表格部分
        table_widget = QTableWidget()
        table_widget.setColumnCount(3)
        table_widget.setRowCount(5)

        for row in range(5):
            for col in range(3):
                item = QTableWidgetItem(f"第 {row} 列, 第 {col} 行")
                table_widget.setItem(row, col, item)

        # 創建右側的圖表部分
        chart_view = QGraphicsView()
        chart_scene = QGraphicsScene()

        # 在圖表部分添加一個簡單的圓形
        chart_scene.addEllipse(0, 0, 100, 100)

        chart_view.setScene(chart_scene)

        # 將表格和圖表添加到主佈局中
        main_layout.addWidget(table_widget)
        main_layout.addWidget(chart_view)

        # 創建中央窗口並設置主佈局
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

class TableModel(QAbstractTableModel): 
    def rowCount(self, parent):
        return len(rows)

    def columnCount(self, parent):
        return len(headers)

    def data(self, index, role):
        if role != Qt.ItemDataRole.DisplayRole:
            return QVariant()

        row = index.row()
        col = index.column()

        if row < len(rows):
            item = rows[row]

            if col < len(item):
                value = item[col]

                # 特別處理 scrap_time 欄位，將 datetime.date 物件轉換為字串
                if isinstance(value, datetime.date):
                    return value.strftime("%Y-%m-%d")

                return value

        return QVariant()

    def headerData(self, section, orientation, role):
        if role != Qt.ItemDataRole.DisplayRole or orientation != Qt.Orientation.Horizontal:
            return QVariant()
        return headers[section]

class MainWindow(QMainWindow):
    def __init__(self, username, user_id):
        super().__init__()

        self.setWindowTitle("資料表")
        self.setGeometry(500, 100, 1200, 800)
        self.username = username
        self.user_id = user_id
        self.script_dir = os.path.dirname(os.path.realpath(__file__))

        self.setStyleSheet('''
            QPushButton {
                background-color: #008CBA;
                color: white;
            }
        ''')

        self.model = TableModel()
        table_view = QTableView()
        # 設置水平標題為等寬模式
        table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        table_view.setModel(self.model)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        # 垂直佈局包裹水平佈局和按鈕
        v_layout = QVBoxLayout()
        v_layout.addWidget(table_view)

        self.select_button = QPushButton("查詢")
        self.select_button.setFixedSize(80, 30)
        self.select_button.setStyleSheet("background-color: #008CBA;")
        self.select_button.clicked.connect(self.select_button_clicked)

        self.filter_button = QPushButton("篩選")
        self.filter_label = QLabel('輸入篩選值', self)
        self.filter_textbox = QLineEdit(self)
        self.filter_button.setFixedSize(80, 30)
        self.filter_button.clicked.connect(self.filter_button_clicked)
        self.filter_button.setEnabled(False)  # 初始狀態設為不可用
        self.filter_button.setStyleSheet("background-color: #CCCCCC; color: #555555;")  # 灰色樣式

        # 新增下載按鈕
        self.download_button = QPushButton("下載")
        self.download_button.setFixedSize(80, 30)
        self.download_button.setEnabled(False)  # 初始狀態設為不可用
        self.download_button.setStyleSheet("background-color: #CCCCCC; color: #555555;")
        self.download_button.clicked.connect(self.download_button_clicked)

        account_label = QLabel(f'用戶名 : {username}', self)
        user_id_label = QLabel(f'用戶id : {user_id}', self)

        # #設置一個選擇時間的下拉式選單按鈕
        # self.time_button = QPushButton('選擇時間', self)
        # self.time_button.setStyleSheet("background-color: #008CBA;")
        # self.time_button.setFixedSize(80, 30)
        # self.time_button.clicked.connect(self.filter_by_time)

        # 新增分析按鈕
        self.analyze_button = QPushButton("分析")
        self.analyze_button.setFixedSize(80, 30)
        self.analyze_button.setEnabled(False)  # 初始狀態設為不可用
        self.analyze_button.setStyleSheet("background-color: #CCCCCC; color: #555555;")
        self.analyze_button.clicked.connect(self.analyze_button_clicked)

        # 將按鈕添加到水平佈局
        h_layout = QHBoxLayout()
        h_layout.addWidget(account_label)
        h_layout.addWidget(user_id_label)
        h_layout.addWidget(self.analyze_button)
        h_layout.addStretch(1)  #將按鈕推到右邊
        # h_layout.addWidget(self.time_button)
        h_layout.addWidget(self.filter_label)
        h_layout.addWidget(self.filter_textbox)
        h_layout.addWidget(self.filter_button)
        h_layout.addWidget(self.select_button)
        h_layout.addWidget(self.download_button)
        

        # 添加水平佈局到垂直佈局
        v_layout.addLayout(h_layout)

        layout.addLayout(v_layout)
        self.setCentralWidget(central_widget)

    # 下載功能
    def download_button_clicked(self):
        global rows

        # 詢問使用者輸入檔案名稱
        while True:
            file_name, ok_pressed = QInputDialog.getText(self, "輸入檔案名稱", "請輸入檔案名稱:")
            if not ok_pressed:
                return  # 使用者按下取消，終止下載

            if not file_name:
                print("檔案名稱不能為空")
                continue  # 檔案名稱為空，重新詢問

            # 加上 .csv 副檔名
            csv_filename = f"{file_name}.csv"

            if os.path.exists(csv_filename):
                # 使用 QMessageBox 提醒使用者
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setText(f"檔案 '{csv_filename}' 已存在，請選擇其他名稱。")
                msg.setWindowTitle("檔案已存在")
                msg.exec()
            else:
                break  # 檔案不存在，退出迴圈

        try:
            with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)

                # 寫入標題
                csv_writer.writerow(headers)

                # 寫入資料
                csv_writer.writerows(rows)

            print(f"資料已成功下載到 {csv_filename}")

        except Exception as e:
            print(f"下載資料時發生錯誤: {e}")

    # 查詢功能
    def select_button_clicked(self):
        global rows

        response = asyncio.run(main_async(self.user_id))
        # 定義正則表達式，用於匹配 datetime.date 對象
        date_pattern = re.compile(r"datetime\.date\((\d+), (\d+), (\d+)\)")

        # 替换 datetime.date 字符串為 '"YYYY-MM-DD"' 格式
        def date_replacer(match):
            year, month, day = match.groups()
            return f'"{year}-{month}-{day}"'

        # 將 response 中的 datetime.date 對象替换字符
        response_with_dates_as_strings = date_pattern.sub(date_replacer, response)
    
        if response_with_dates_as_strings == "False":
            QMessageBox.warning(self, "警告", "沒有資料可顯示。")
            return
        else:
            try:
                # 使用 ast.literal_eval 將修改的字串轉換列表
                rows_temp = ast.literal_eval(response_with_dates_as_strings)

                # 將日期字符串轉換回 datetime.date 對象
                rows = [(user_id, datetime.datetime.strptime(date_string, "%Y-%m-%d").date(), data)
                        for user_id, date_string, data in rows_temp]
                

            except Exception as e:
                print(f"An error occurred while parsing the response: {e}")
                rows = []

        self.model.layoutAboutToBeChanged.emit()
        self.model.layoutChanged.emit()

        self.download_button.setEnabled(True)
        self.download_button.setStyleSheet("")
        # 在查詢按鈕觸發後，將篩選按鈕設置為可用
        self.filter_button.setEnabled(True)     #資料傳送
        self.filter_button.setStyleSheet("")    # 移除樣式，恢復預設外觀
        self.analyze_button.setEnabled(True)     #資料傳送
        self.analyze_button.setStyleSheet("")    # 移除樣式，恢復預設外觀

    # 篩選功能
    def filter_button_clicked(self):
        global rows

        # 取得篩選值
        filter_value = self.filter_textbox.text()

        if not filter_value:
            QMessageBox.warning(self, "警告", "請輸入篩選值。")
            return

        # 使用 filter() 函數篩選資料
        rows = list(filter(lambda row: filter_value in row[2], rows))

        self.model.layoutAboutToBeChanged.emit()
        self.model.layoutChanged.emit()

        self.download_button.setEnabled(True)
        self.download_button.setStyleSheet("")


    #分析爬取的資料介面
    def analyze_button_clicked(self):
        script_path = os.path.join(self.script_dir, "analyze.py")
        input_data = f"{self.user_id}".encode('utf-8')
        process = subprocess.Popen(["python", script_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(input=input_data)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    user_data = sys.stdin.read().strip()
    # user_data = "David,1"
    username = user_data.split(",")[0]
    user_id = user_data.split(",")[1]

    window = MainWindow(username, user_id)
    window.show()

    app.exec()
