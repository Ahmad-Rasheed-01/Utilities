import sys
import re
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QTextEdit, QLabel, QComboBox, QMessageBox, QHBoxLayout

class PatchAnalyzer(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Patch Analyzer")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # Load File Button
        self.loadButton = QPushButton("Load Patch File")
        self.loadButton.clicked.connect(self.loadFile)
        layout.addWidget(self.loadButton)

        # Dropdown for Year Selection
        self.yearDropdown = QComboBox()
        self.yearDropdown.setEnabled(False)  # Disabled until file is loaded
        self.yearDropdown.currentIndexChanged.connect(self.showYearPatches)
        layout.addWidget(QLabel("Select Year:"))
        layout.addWidget(self.yearDropdown)

        # Button to Select Date Range
        self.rangeButton = QPushButton("Select Date Range")
        self.rangeButton.setEnabled(False)
        self.rangeButton.clicked.connect(self.selectDateRange)
        layout.addWidget(self.rangeButton)

        # Patch Count Display
        self.patchCountLabel = QLabel("Total Patches: 0")
        layout.addWidget(self.patchCountLabel)

        # Patch Details Display
        self.textArea = QTextEdit()
        self.textArea.setReadOnly(True)
        layout.addWidget(self.textArea)

        self.setLayout(layout)

        # Store parsed patches
        self.patches = []
        self.years = set()

    def loadFile(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Patch File", "", "Text Files (*.txt);;All Files (*)", options=options)
        
        if filePath:
            try:
                with open(filePath, "r", encoding="utf-8") as file:  # Read file using UTF-8
                    data = file.read()
                self.processData(data)
            except UnicodeDecodeError:
                QMessageBox.critical(self, "Error", "File encoding error! Please ensure the file is UTF-8 encoded.")

    def processData(self, data):
        self.patches = []
        self.years = set()

        patch_blocks = re.split(r'(?=^Name\s*:)', data, flags=re.MULTILINE)

        for block in patch_blocks:
            match = re.search(r'Install Date:\s*(\w+\s\d+\s\d+)', block)
            if match:
                date_str = match.group(1)
                year = date_str.split()[-1]
                self.years.add(year)
                self.patches.append((year, block.strip()))

        if self.patches:
            self.yearDropdown.clear()
            self.yearDropdown.addItems(sorted(self.years))
            self.yearDropdown.setEnabled(True)
            self.rangeButton.setEnabled(True)
            self.showYearPatches()

    def showYearPatches(self):
        selected_year = self.yearDropdown.currentText()
        if not selected_year:
            return

        filtered_patches = [p[1] for p in self.patches if p[0] == selected_year]

        self.patchCountLabel.setText(f"Total Patches: {len(filtered_patches)}")

        display_text = ""
        for idx, patch in enumerate(filtered_patches, 1):
            display_text += f"Patch {idx}:\n{patch}\n\n"

        self.textArea.setText(display_text)

    def selectDateRange(self):
        QMessageBox.information(self, "Feature Not Implemented", "Date range selection will be implemented soon.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PatchAnalyzer()
    window.show()
    sys.exit(app.exec_())
