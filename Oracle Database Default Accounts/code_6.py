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
            "SYS", "SYSTEM", "EBS_SYSTEM", "DBSNMP", "SYSMAN", "MGMT_VIEW", "SCOTT", "SSOSDK", "JUNK_PS", "MDSYS", "ODM_MTR",
            "OLAPSYS", "ORDPLUGINS", "ORDSYS", "OUTLN", "OWAPUB", "MGDSYS", "PORTAL30_DEMO", "PORTAL30_PUBLIC", "PORTAL30_PS",
            "PORTAL30_SSO_PUBLIC", "PORTAL30", "PORTAL30_SSO", "CTXSYS", "EDWREP", "ODM", "APPLSYSPUB", "APPLSYS", "APPS",
            "APPS_NE", "APPS_mrc", "AD_MONITOR", "EM_MONITOR", "ABM", "AHL", "AHM", "AK", "ALR", "AMF", "AMS", "AMV", "AMW",
            "AP", "AR", "ASF", "ASG", "ASL", "ASN", "ASO", "ASP", "AST", "AX", "AZ", "BEN", "BIC", "BIL", "BIM", "BIS", "BIV",
            "BIX", "BNE", "BOM", "BSC", "CCT", "CE", "CLN", "CN", "CRP", "CS", "CSC", "CSD", "CSE", "CSF", "CSI", "CSL", "CSM",
            "CSP", "CSR", "CSS", "CUA", "CUE", "CUF", "CUG", "CUI", "CUN", "CUP", "CUS", "CZ", "DDD", "DDR", "DNA", "DOM", "DPP",
            "EAA", "EAM", "EC", "ECX", "EDR", "EGO", "ENG", "ENI", "EVM", "FA", "FEM", "FII", "FLM", "FPA", "FPT", "FRM", "FTE",
            "FTP", "FUN", "FV", "GCS", "GHG", "GL", "GMA", "GMD", "GME", "GMF", "GMI", "GML", "GMO", "GMP", "GMS", "GR", "HR",
            "HRI", "HXC", "HXT", "IA", "IBA", "IBC", "IBE", "IBP", "IBU", "IBW", "IBY", "ICX", "IEB", "IEC", "IEM", "IEO", "IES",
            "IEU", "IEX", "IGC", "IGF", "IGI", "IGS", "IGW", "IMC", "IMT", "INL", "INV", "IPA", "IPD", "IPM", "ISC", "ITA", "ITG",
            "IZU", "JA", "JE", "JG", "JL", "JMF", "JTF", "JTM", "JTS", "LNS", "ME", "MFG", "MRP", "MSC", "MSD", "MSO", "MSR", "MST",
            "MTH", "MWA", "OE", "OKB", "OKC", "OKE", "OKI", "OKL", "OKO", "OKR", "OKS", "OKX", "ONT", "OPI", "OSM", "OTA", "OZF",
            "OZP", "OZS", "PA", "PFT", "PJI", "PJM", "PMI", "PN", "PO", "POA", "POM", "PON", "POS", "PRP", "PSA", "PSB", "PSP",
            "PV", "QA", "QOT", "QP", "QPR", "QRM", "RG", "RHX", "RLA", "RLM", "RRS", "SSP", "VEA", "VEH", "WIP", "WMS", "WPS",
            "WSH", "WSM", "XDO", "XDP", "XLA", "XLE", "XNB", "XNC", "XNI", "XNM", "XNP", "XNS", "XTR", "ZFA", "ZPB", "ZSA", "ZX"
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
        try:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            file_name, _ = QFileDialog.getSaveFileName(self, "Save Results", "", "Text Files (*.txt);;All Files (*)", options=options)
            if file_name:
                with open(file_name, 'w') as file:
                    file.write("Comparison Results:\n")
                    file.write(f"\nMatched Accounts: {', '.join(matched_accounts)}\n")
                    file.write(f"\nUnmatched Accounts: {', '.join(unmatched_accounts)}\n")

                self.result_browser.append(f"\nResults exported to: {file_name}")

        except Exception as e:
            self.result_browser.append(f"\nError exporting results: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OracleAccountComparator()
    window.show()
    sys.exit(app.exec_())
