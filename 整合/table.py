from PyQt6.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt, QAbstractTableModel, QVariant
import sys
import subprocess


headers = ["user_id", "scrap_time", "scrap_data", "url"]
rows = []

class TableModel(QAbstractTableModel): 
    def rowCount(self, parent):
        return len(rows)         
    def columnCount(self, parent):        
        return len(headers)    
    def data(self, index, role):        
        if role != Qt.ItemDataRole.DisplayRole:            
            return QVariant()
        return rows[index.row()][index.column()]        
        
    def headerData(self, section, orientation, role):        
        if role != Qt.ItemDataRole.DisplayRole or orientation != Qt.Orientation.Horizontal:            
            return QVariant()        
        return headers[section]

class MainWindow(QMainWindow):
    def __init__(self, username, user_id):
        super().__init__()

        self.setWindowTitle("資料表")
        self.setGeometry(500, 100, 1000, 800)
        self.username = username
        self.user_id = user_id

        model = TableModel()
        table_view = QTableView()
        table_view.setModel(model)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        # 垂直佈局包裹水平佈局和按鈕
        v_layout = QVBoxLayout()
        v_layout.addWidget(table_view)

        select_button = QPushButton("查詢")
        select_button.setFixedSize(80, 30)
        select_button.clicked.connect(self.select_button_clicked)

        # 新增下載按鈕
        download_button = QPushButton("下載")
        download_button.setFixedSize(80, 30)
        download_button.clicked.connect(self.download_button_clicked)

        account_label = QLabel(f'用戶名 : {username}', self)
        user_id_label = QLabel(f'用戶id : {user_id}', self)
        
        # 將按鈕添加到水平佈局
        h_layout = QHBoxLayout()
        h_layout.addWidget(account_label)
        h_layout.addWidget(user_id_label)
        h_layout.addStretch(1)  #將按鈕推到右邊
        h_layout.addWidget(select_button)
        h_layout.addWidget(download_button)
        
        # 添加水平佈局到垂直佈局
        v_layout.addLayout(h_layout)

        layout.addLayout(v_layout)
        self.setCentralWidget(central_widget)

    def download_button_clicked(self):  
        print("下載按鈕被點擊了！")

    def select_button_clicked(self): 
        response = subprocess.run(["python", os.path.join(self.script_dir, "Backend_wiring_select.py"),user_id], stdout=subprocess.PIPE)
        print(response.stdout.decode("utf-8"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    user_data = sys.stdin.read().strip()
    username = user_data.split(",")[0]
    user_id = user_data.split(",")[1]

    window = MainWindow(username, user_id)
    window.show()
    app.exec()
