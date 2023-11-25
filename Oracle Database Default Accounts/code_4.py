import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QFileDialog, QTextBrowser, QAction, qApp, QHBoxLayout

class OracleAccountComparator(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Oracle Account Comparator")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        self.result_browser = QTextBrowser()
        layout.addWidget(self.result_browser)

        button_layout = QHBoxLayout()

        self.upload_button = QPushButton("Upload File")
        self.upload_button.clicked.connect(self.upload_file)
        button_layout.addWidget(self.upload_button)

        self.analyze_button = QPushButton("Analyze")
        self.analyze_button.clicked.connect(self.analyze_accounts)
        button_layout.addWidget(self.analyze_button)

        self.export_button = QPushButton("Export")
        self.export_button.clicked.connect(self.export_results)
        button_layout.addWidget(self.export_button)

        close_action = QPushButton("Close")
        close_action.clicked.connect(qApp.quit)
        button_layout.addWidget(close_action)

        layout.addLayout(button_layout)
        self.central_widget.setLayout(layout)

        # List of default Oracle database accounts
        self.default_accounts = [
            # ... (same as before)
        ]

        self.init_menu()

    def init_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        close_action = QAction('Close', self)
        close_action.triggered.connect(qApp.quit)
        file_menu.addAction(close_action)

    def upload_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Text File", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            self.file_path = file_name
            self.result_browser.clear()
            self.result_browser.append(f"File uploaded: {self.file_path}")

    def analyze_accounts(self):
        try:
            with open(self.file_path, 'r') as file:
                user_accounts = [line.strip() for line in file.readlines()]

            matched_accounts = set(user_accounts) & set(self.default_accounts)
            unmatched_accounts = set(user_accounts) - set(self.default_accounts)

            self.result_browser.append("\nComparison Results:")
            self.result_browser.append(f"\nMatched Accounts: {', '.join(matched_accounts)}")
            self.result_browser.append(f"\nUnmatched Accounts: {', '.join(unmatched_accounts)}")

        except Exception as e:
            self.result_browser.append(f"\nError: {str(e)}")

    def export_results(self):
        # Add the logic for exporting results to a file here
        self.result_browser.append("\nExporting results...")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OracleAccountComparator()
    window.show()
    sys.exit(app.exec_())
