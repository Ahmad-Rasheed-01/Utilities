# Feature added to show total number of patches applied.
# Feature added to show total number of patches applied correctly. Still not working.
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

        # Patch count label
        self.patchCountLabel = QLabel("Total Patches Found: 0")
        layout.addWidget(self.patchCountLabel)

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
                    lines = file.readlines()
                self.parsePatches(lines)
                self.fileStatusLabel.setText(f"File Loaded: {filePath}")
                self.patchCountLabel.setText(f"Total Patches Found: {len(self.patches)}")  # Update count label
            except UnicodeDecodeError:
                self.fileStatusLabel.setText("Error: File encoding issue!")
                QMessageBox.critical(self, "Error", "File encoding error! Please use UTF-8 encoded files.")

    def parsePatches(self, lines):
        self.patches = []
        current_patch = None  # Start with no active patch

        for line in lines:
            line = line.strip()

            if line.startswith("Name :"):  # Patch starts
                if current_patch:  # Save previous patch before starting a new one
                    self.patches.append(current_patch)

                current_patch = {"name": line.split(":", 1)[1].strip(), "details": [], "install_date": "Unknown", "date_obj": None}

            elif current_patch:  # Inside a patch block
                if line.startswith("Description :"):  # Patch ends
                    current_patch["description"] = line.split(":", 1)[1].strip()
                    self.patches.append(current_patch)  # Save final patch
                    current_patch = None  # Reset

                else:
                    current_patch["details"].append(line)

                    if "Install Date:" in line:  # Extract install date
                        install_date = line.split(":", 1)[1].strip()
                        current_patch["install_date"] = install_date

                        try:
                            date_obj = datetime.strptime(install_date, "%a %d %b %Y %I:%M:%S %p %Z")
                            current_patch["date_obj"] = date_obj
                        except ValueError:
                            current_patch["date_obj"] = None  # If parsing fails

        if current_patch:  # Append last patch if it wasn't saved
            self.patches.append(current_patch)

    def showPatchesByRange(self):
        start_date = self.startDate.date().toPyDate()
        end_date = self.endDate.date().toPyDate()
        filtered_patches = [
            patch for patch in self.patches if patch["date_obj"] and start_date <= patch["date_obj"].date() <= end_date
        ]
        self.displayPatches(filtered_patches)

    def displayPatches(self, patches):
        self.textArea.clear()
        self.textArea.append(f"Total Patches in Selected Date Range: {len(patches)}\n")
        for idx, patch in enumerate(patches, start=1):
            self.textArea.append(f"Patch {idx}:\n")
            self.textArea.append(f"Name: {patch['name']}")
            self.textArea.append(f"Install Date: {patch.get('install_date', 'Unknown')}")
            self.textArea.append("Details:")
            self.textArea.append("\n".join(patch["details"]))
            self.textArea.append(f"Description:\n{patch['description']}\n")
            self.textArea.append("-" * 50 + "\n")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = PatchViewer()
    viewer.show()
    sys.exit(app.exec_())
