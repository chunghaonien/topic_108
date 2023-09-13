import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

class EventTrackingWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.event_log = []

        self.mouse_start_pos = None
        self.mouse_end_pos = None

    def init_ui(self):
        self.label = QLabel("Events will be displayed here.")
        layout = QVBoxLayout()
        layout.addWidget(self.label)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle("Event Tracking Example")

    def log_event(self, event_info):
        self.event_log.append(event_info)
        self.update_label()
        self.save_to_file()

    def update_label(self):
        self.label.setText("\n".join(self.event_log))

    def save_to_file(self):
        with open("event_log.txt", "w") as f:
            f.write("\n".join(self.event_log))

    def keyPressEvent(self, event):
        key = event.key()
        self.log_event(f"Key pressed: {Qt.Key(key)}")

    def wheelEvent(self, event):
        delta = event.angleDelta().y() / 120
        self.log_event(f"Mouse wheel scrolled: {delta}")

    def mouseMoveEvent(self, event):
        if self.mouse_start_pos:
            self.mouse_end_pos = event.pos()

    def mousePressEvent(self, event):
        x = event.x()
        y = event.y()
        buttons = event.buttons()
        self.log_event(f"Mouse pressed at ({x}, {y}) - Buttons: {buttons}")
        self.mouse_start_pos = event.pos()

    def mouseReleaseEvent(self, event):
        x = event.x()
        y = event.y()
        buttons = event.buttons()
        self.log_event(f"Mouse released at ({x}, {y}) - Buttons: {buttons}")
        if self.mouse_start_pos and self.mouse_end_pos:
            self.log_event(f"Mouse drag from {self.mouse_start_pos} to {self.mouse_end_pos}")
        self.mouse_start_pos = None
        self.mouse_end_pos = None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EventTrackingWindow()
    window.show()
    sys.exit(app.exec_())
