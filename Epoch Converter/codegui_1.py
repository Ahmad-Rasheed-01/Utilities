import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QFileDialog, QTextBrowser, QAction, qApp, QHBoxLayout, QLineEdit

from datetime import datetime

class TimestampConverter(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Timestamp Converter")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        self.timestamp_input = QLineEdit(self)
        self.timestamp_input.setPlaceholderText("Enter timestamp in nanoseconds")
        layout.addWidget(self.timestamp_input)

        self.result_browser = QTextBrowser()
        layout.addWidget(self.result_browser)

        button_layout = QHBoxLayout()

        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.convert_timestamp)
        button_layout.addWidget(self.convert_button)

        close_action = QPushButton("Close")
        close_action.clicked.connect(qApp.quit)
        button_layout.addWidget(close_action)

        layout.addLayout(button_layout)
        self.central_widget.setLayout(layout)

    def convert_timestamp(self):
        timestamp_input = self.timestamp_input.text()

        try:
            # Convert input to a float (assuming it's in nanoseconds)
            timestamp = float(timestamp_input) / 1e9
            human_readable_date = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S UTC')
            self.result_browser.clear()
            self.result_browser.append(f"Human-readable date and time: {human_readable_date}")

        except ValueError:
            self.result_browser.clear()
            self.result_browser.append("Invalid input. Please enter a valid numeric timestamp.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TimestampConverter()
    window.show()
    sys.exit(app.exec_())
