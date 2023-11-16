from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

headers = ["Scientist name", "Birthdate", "Contribution"]
rows =    [("Newton", "1643-01-04", "Classical mechanics"),
           ("Einstein", "1879-03-14", "Relativity"),
           ("Darwin", "1809-02-12", "Evolution")]

class TableModel(QAbstractTableModel):
    def rowCount(self, parent):
        # How many rows are there?
        return len(rows)
    def columnCount(self, parent):
        # How many columns?
        return len(headers)
    def data(self, index, role):
        if role != Qt.ItemDataRole.DisplayRole:
            return QVariant()
        # What's the value of the cell at the given index?
        return rows[index.row()][index.column()]
    def headerData(self, section, orientation, role):
        if role != Qt.ItemDataRole.DisplayRole or orientation != Qt.Orientation.Horizontal:
            return QVariant()
        # What's the header for the given column?
        return headers[section]

        
app = QApplication([])
model = TableModel()
view = QTableView()
view.setModel(model)
view.show()
app.exec()