#Added a new method toggleFilterOptions to show/hide the filter options based on the selected filter.
#Added featue to select a filter first and then select the year or date range to filter the patches.
import sys
import re
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QTextEdit,
    QComboBox,
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
        self.years = set()

    def initUI(self):
        layout = QVBoxLayout()

        # Load file button
        self.loadButton = QPushButton("Load Patch File")
        self.loadButton.clicked.connect(self.loadFile)
        layout.addWidget(self.loadButton)
        
        # File status label
        self.fileStatusLabel = QLabel("No file loaded")
        layout.addWidget(self.fileStatusLabel)

        # Filter selection
        self.filterSelection = QComboBox()
        self.filterSelection.addItems(["Select Filter", "Filter by Year", "Filter by Range"])
        self.filterSelection.currentIndexChanged.connect(self.toggleFilterOptions)
        layout.addWidget(self.filterSelection)

        # Year selection (Initially Hidden)
        self.yearLabel = QLabel("Select Year:")
        self.yearDropdown = QComboBox()
        self.yearDropdown.currentIndexChanged.connect(self.showPatchesByYear)
        layout.addWidget(self.yearLabel)
        layout.addWidget(self.yearDropdown)

        # Date range selection (Initially Hidden)
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

        # Hide initially
        self.yearLabel.hide()
        self.yearDropdown.hide()
        self.rangeLabel.hide()
        self.startDate.hide()
        self.endDate.hide()
        self.rangeButton.hide()

        # Display area
        self.textArea = QTextEdit()
        self.textArea.setReadOnly(True)
        layout.addWidget(self.textArea)

        self.setLayout(layout)
        self.setWindowTitle("Patch Viewer")
        self.resize(800, 600)

    def toggleFilterOptions(self):
        option = self.filterSelection.currentText()
        if option == "Filter by Year":
            self.yearLabel.show()
            self.yearDropdown.show()
            self.rangeLabel.hide()
            self.startDate.hide()
            self.endDate.hide()
            self.rangeButton.hide()
        elif option == "Filter by Range":
            self.yearLabel.hide()
            self.yearDropdown.hide()
            self.rangeLabel.show()
            self.startDate.show()
            self.endDate.show()
            self.rangeButton.show()
        else:
            self.yearLabel.hide()
            self.yearDropdown.hide()
            self.rangeLabel.hide()
            self.startDate.hide()
            self.endDate.hide()
            self.rangeButton.hide()

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
        self.years.clear()

        for match in matches:
            name = match[0].strip()
            details = match[1].strip()
            description = match[2].strip()
            install_date_match = re.search(r"Install Date:\s+(.*?)\n", details)
            install_date = install_date_match.group(1) if install_date_match else "Unknown"
            try:
                install_date_cleaned = " ".join(install_date.split()[:-1])  # Remove timezone
                date_obj = datetime.strptime(install_date_cleaned, "%a %d %b %Y %I:%M:%S %p")
                year = date_obj.year
                self.years.add(year)
            except ValueError:
                year = "Unknown"

            self.patches.append(
                {
                    "name": name,
                    "install_date": install_date,
                    "details": details,
                    "description": description,
                    "year": year,
                }
            )

        self.updateYearDropdown()

    def updateYearDropdown(self):
        self.yearDropdown.clear()
        if self.years:
            self.yearDropdown.addItems(sorted(map(str, self.years)))
        else:
            self.yearDropdown.addItem("No Data")

    def showPatchesByYear(self):
        selected_year = self.yearDropdown.currentText().strip()
        if not selected_year or selected_year == "No Data":
            return
        try:
            selected_year = int(selected_year)
            filtered_patches = [p for p in self.patches if p["year"] == selected_year]
            self.displayPatches(filtered_patches)
        except ValueError:
            QMessageBox.warning(self, "Warning", "Invalid year selected.")

    def showPatchesByRange(self):
        start_date = self.startDate.date().toPyDate()
        end_date = self.endDate.date().toPyDate()
        filtered_patches = []
        for patch in self.patches:
            try:
                patch_date = datetime.strptime(
                    patch["install_date"], "%a %d %b %Y %I:%M:%S %p %Z"
                ).date()
                if start_date <= patch_date <= end_date:
                    filtered_patches.append(patch)
            except ValueError:
                continue
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
