import sys, logging, os
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QStatusBar
from PyQt6.QtCore import Qt
from .styles import dark_stylesheet
from .signature_db import SignatureDatabase
from .home_tab import HomeTab
from .add_signature_tab import AddSignatureTab
from .check_signature_tab import CheckSignatureTab

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(ROOT_DIR, "electronic_signatures.db")
LOG_PATH = os.path.join(ROOT_DIR, "signature_app.log")

logging.basicConfig(filename=LOG_PATH, level=logging.INFO, format="%(asctime)s - %(message)s")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = SignatureDatabase(DB_PATH)
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.home_tab = HomeTab(self.db)
        self.add_tab = AddSignatureTab(self.db)
        self.check_tab = CheckSignatureTab(self.db)
        self.tabs.addTab(self.home_tab, "Home")
        self.tabs.addTab(self.add_tab, "Add Signature")
        self.tabs.addTab(self.check_tab, "Check Signature")
        self.setStyleSheet(dark_stylesheet())
        self.setWindowTitle("Electronic Signature Manager")
        scr = self.screen() or QApplication.primaryScreen()
        r = scr.availableGeometry()
        w = int(r.width() * 0.8)
        h = int(r.height() * 0.8)
        self.resize(w, h)
        self.move(r.x() + (r.width() - w) // 2, r.y() + (r.height() - h) // 2)
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Ready")

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Electronic Signature Manager")
    app.setApplicationVersion("6.2")
    w = MainWindow()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
