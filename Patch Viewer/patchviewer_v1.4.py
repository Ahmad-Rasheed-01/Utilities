#Removed select an year option.
import sys
import re
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QTextEdit,
    QLabel,
    QDateEdit,
    QHBoxLayout,
    QMessageBox,
)
from datetime import datetime


class PatchViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.patches = []

    def initUI(self):
        layout = QVBoxLayout()

        # Load file button
        self.loadButton = QPushButton("Load Patch File")
        self.loadButton.clicked.connect(self.loadFile)
        layout.addWidget(self.loadButton)

        # File status label
        self.fileStatusLabel = QLabel("No file loaded")
        layout.addWidget(self.fileStatusLabel)

        # Date range selection
        self.rangeLabel = QLabel("Select Date Range:")
        self.startDate = QDateEdit()
        self.startDate.setCalendarPopup(True)
        self.endDate = QDateEdit()
        self.endDate.setCalendarPopup(True)
        self.rangeButton = QPushButton("Filter by Date Range")
        self.rangeButton.clicked.connect(self.showPatchesByRange)

        rangeLayout = QHBoxLayout()
        rangeLayout.addWidget(self.rangeLabel)
        rangeLayout.addWidget(self.startDate)
        rangeLayout.addWidget(self.endDate)
        rangeLayout.addWidget(self.rangeButton)
        layout.addLayout(rangeLayout)

        # Display area
        self.textArea = QTextEdit()
        self.textArea.setReadOnly(True)
        layout.addWidget(self.textArea)

        self.setLayout(layout)
        self.setWindowTitle("Patch Viewer")
        self.resize(800, 600)

    def loadFile(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(
            self,
            "Open Patch File",
            "",
            "Text Files (*.txt);;All Files (*)",
            options=options,
        )

        if filePath:
            try:
                with open(filePath, "r", encoding="utf-8") as file:
                    data = file.read()
                self.parsePatches(data)
                self.fileStatusLabel.setText(f"File Loaded: {filePath}")
            except UnicodeDecodeError:
                self.fileStatusLabel.setText("Error: File encoding issue!")
                QMessageBox.critical(self, "Error", "File encoding error! Please use UTF-8 encoded files.")

    def parsePatches(self, data):
        pattern = r"Name\s+: (.*?)\n(.*?)Description\s+: (.*?)\n(?=Name|$)"
        matches = re.findall(pattern, data, re.DOTALL)
        self.patches = []

        for match in matches:
            name = match[0].strip()
            details = match[1].strip()
            description = match[2].strip()
            install_date_match = re.search(r"Install Date:\s+(.*?)\n", details)
            install_date = install_date_match.group(1) if install_date_match else "Unknown"

            try:
                # Attempt to parse full date including timezone
                date_obj = datetime.strptime(install_date, "%a %d %b %Y %I:%M:%S %p %Z")
            except ValueError:
                date_obj = None  # If parsing fails, set date_obj as None

            self.patches.append(
                {
                    "name": name,
                    "install_date": install_date,
                    "details": details,
                    "description": description,
                    "date_obj": date_obj,
                }
            )

    def showPatchesByRange(self):
        start_date = self.startDate.date().toPyDate()
        end_date = self.endDate.date().toPyDate()
        filtered_patches = [
            patch for patch in self.patches if patch["date_obj"] and start_date <= patch["date_obj"].date() <= end_date
        ]
        self.displayPatches(filtered_patches)

    def displayPatches(self, patches):
        self.textArea.clear()
        self.textArea.append(f"Total Patches: {len(patches)}\n")
        for idx, patch in enumerate(patches, start=1):
            self.textArea.append(f"Patch {idx}:\n")
            self.textArea.append(f"Name: {patch['name']}")
            self.textArea.append(f"Install Date: {patch['install_date']}")
            self.textArea.append(f"Details:\n{patch['details']}")
            self.textArea.append(f"Description:\n{patch['description']}\n")
            self.textArea.append("-" * 50 + "\n")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = PatchViewer()
    viewer.show()
    sys.exit(app.exec_())
