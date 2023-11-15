from PyQt6.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt, QAbstractTableModel, QVariant

headers = ["user_id", "scrap_time", "scrap_data", "url"]

class TableModel(QAbstractTableModel):          
           
    def columnCount(self, parent):        
        return len(headers)    
    def data(self, index, role):        
        if role != Qt.ItemDataRole.DisplayRole:            
            return QVariant()        
        
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

        # 新增下載按鈕
        download_button = QPushButton("下載")
        download_button.setFixedSize(80, 30)
        download_button.clicked.connect(self.download_button_clicked)

        # 將按鈕添加到水平佈局
        h_layout = QHBoxLayout()
        h_layout.addStretch(1)  #將按鈕推到右邊
        h_layout.addWidget(download_button)

        # 添加水平佈局到垂直佈局
        v_layout.addLayout(h_layout)

        layout.addLayout(v_layout)
        self.setCentralWidget(central_widget)

    def download_button_clicked(self):  
        print("下載按鈕被點擊了！")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
