from PyQt6.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt, QAbstractTableModel, QVariant

headers = ["user_id", "scrap_time", "scrap_data", "url"]
rows = [("1", "2021-10-01", "data", "https://www.google.com/"), ("2", "2021-10-02", "data", "https://www.google.com/"), ("3", "2021-10-03", "data", "https://www.google.com/")]

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
    def __init__(self):
        super().__init__()

        self.setWindowTitle("資料表")
        self.setGeometry(500, 100, 1000, 800)

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

        # 將按鈕添加到水平佈局
        h_layout = QHBoxLayout()
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


        response = subprocess.run(["python", os.path.join(self.script_dir, "Backend_wiring_login.py"),user_id], stdout=subprocess.PIPE)
        print(response.stdout.decode("utf-8"))


if __name__ == "__main__":
    app = QApplication([])
    # username = username = sys.stdin.read().strip()

    window = MainWindow()
    window.show()
    app.exec()
