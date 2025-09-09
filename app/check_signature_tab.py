import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSplitter, QGroupBox, QVBoxLayout, QPushButton, QHBoxLayout, QFileDialog, QSlider, QDialog, QLineEdit, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from .styles import button_style
from .signature_canvas import SignatureCanvas
from .similarity import combined_similarity

class SelectFromDBDialog(QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Select Signature")
        self.resize(800, 500)
        v = QVBoxLayout(self)
        top = QHBoxLayout()
        self.search = QLineEdit(); self.search.setPlaceholderText("Search...")
        find_btn = QPushButton("Search"); find_btn.setStyleSheet(button_style("#3b82f6")); find_btn.clicked.connect(self.reload)
        top.addWidget(self.search); top.addWidget(find_btn)
        v.addLayout(top)
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["ID","Owner","Title","Created","Preview"])
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(self.table.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(self.table.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(True)
        v.addWidget(self.table)
        btns = QHBoxLayout()
        ok = QPushButton("Select"); ok.setStyleSheet(button_style("#22c55e")); ok.clicked.connect(self.accept)
        cancel = QPushButton("Cancel"); cancel.setStyleSheet(button_style("#6b7280")); cancel.clicked.connect(self.reject)
        btns.addStretch(); btns.addWidget(ok); btns.addWidget(cancel)
        v.addLayout(btns)
        self.reload()
    def selected_id(self):
        sel = self.table.selectionModel().selectedRows()
        if not sel: return None
        return int(self.table.item(sel[0].row(), 0).text())
    def reload(self):
        q = (self.search.text() or "").strip()
        rows = self.db.page(q, 25, 0)
        self.table.setRowCount(0)
        for sig_id, owner, title, date, notes, blob in rows:
            r = self.table.rowCount()
            self.table.insertRow(r)
            self.table.setItem(r, 0, QTableWidgetItem(str(sig_id)))
            self.table.setItem(r, 1, QTableWidgetItem(owner or ""))
            self.table.setItem(r, 2, QTableWidgetItem(title or ""))
            self.table.setItem(r, 3, QTableWidgetItem(date.replace("T"," ")[:16]))
            lab = QLabel()
            pm = QPixmap(); pm.loadFromData(blob)
            pm = pm.scaled(120, 60, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            lab.setPixmap(pm); lab.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setCellWidget(r, 4, lab)
            self.table.setRowHeight(r, 68)

class CheckSignatureTab(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.ref_canvas = None
        self.cand_canvas = None
        self.result = None
        self.threshold = None
        self.th_label = None
        self._build()
    def _build(self):
        layout = QVBoxLayout(self)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        left = QGroupBox("Old (Reference)")
        lv = QVBoxLayout(left)
        self.ref_canvas = SignatureCanvas(drawing_enabled=False)
        lv.addWidget(self.ref_canvas)
        lc = QHBoxLayout()
        b1 = QPushButton("📁 Load File"); b1.setStyleSheet(button_style("#8b5cf6")); b1.clicked.connect(self._load_ref_file)
        bdb = QPushButton("📚 Select From DB"); bdb.setStyleSheet(button_style("#3b82f6")); bdb.clicked.connect(self._select_ref_db)
        b2 = QPushButton("🧹 Clear"); b2.setStyleSheet(button_style("#6b7280")); b2.clicked.connect(self.ref_canvas.clear)
        lc.addWidget(b1); lc.addWidget(bdb); lc.addWidget(b2)
        lv.addLayout(lc)
        right = QGroupBox("New (Candidate)")
        rv = QVBoxLayout(right)
        self.cand_canvas = SignatureCanvas(drawing_enabled=True)
        rv.addWidget(self.cand_canvas)
        rc = QHBoxLayout()
        b3 = QPushButton("📁 Load File"); b3.setStyleSheet(button_style("#9ca3af")); b3.clicked.connect(self._load_cand_file)
        b4 = QPushButton("🗑️ Clear"); b4.setStyleSheet(button_style("#ef4444")); b4.clicked.connect(self.cand_canvas.clear)
        rc.addWidget(b3); rc.addWidget(b4)
        rv.addLayout(rc)
        splitter.addWidget(left); splitter.addWidget(right)
        layout.addWidget(splitter)
        th_row = QHBoxLayout()
        self.th_label = QLabel("Threshold: 90%")
        self.threshold = QSlider(Qt.Orientation.Horizontal); self.threshold.setMinimum(50); self.threshold.setMaximum(99); self.threshold.setValue(90)
        self.threshold.valueChanged.connect(lambda v: self.th_label.setText(f"Threshold: {v}%"))
        th_row.addWidget(self.th_label); th_row.addWidget(self.threshold)
        layout.addLayout(th_row)
        vrow = QHBoxLayout()
        btn = QPushButton("🔍 Verify"); btn.setStyleSheet(button_style("#f59e0b")); btn.clicked.connect(self._verify)
        vrow.addStretch(); vrow.addWidget(btn); vrow.addStretch()
        layout.addLayout(vrow)
        self.result = QLabel("No verification performed")
        self.result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result.setStyleSheet("""
            QLabel {
                background-color: #0f172a;
                border: 2px solid #334155;
                border-radius: 8px;
                padding: 15px;
                font-size: 16px;
                font-weight: bold;
                color: #e5e7eb;
                margin: 10px;
            }
        """)
        layout.addWidget(self.result)
    def set_reference_bytes(self, b: bytes):
        self.ref_canvas.load_bytes(b)
    def _select_ref_db(self):
        dlg = SelectFromDBDialog(self.db, self)
        if dlg.exec():
            sid = dlg.selected_id()
            if sid:
                data = self.db.get_signature(sid)
                if data:
                    self.ref_canvas.load_bytes(data)
    def _load_ref_file(self):
        fn, _ = QFileDialog.getOpenFileName(self, "Load Reference", "", "PNG Files (*.png)")
        if fn:
            with open(fn, "rb") as f:
                self.ref_canvas.load_bytes(f.read())
    def _load_cand_file(self):
        fn, _ = QFileDialog.getOpenFileName(self, "Load Candidate", "", "PNG Files (*.png)")
        if fn:
            with open(fn, "rb") as f:
                self.cand_canvas.load_bytes(f.read())
    def _verify(self):
        rb = self.ref_canvas.to_bytes()
        cb = self.cand_canvas.to_bytes()
        if not rb or not cb:
            return
        s = combined_similarity(rb, cb)
        t = self.threshold.value()
        if s >= t:
            self.result.setText(f"✅ VERIFIED • {s:.1f}%")
            self.result.setStyleSheet("""
                QLabel {
                    background-color: #0f2e1c;
                    border: 2px solid #22c55e;
                    border-radius: 8px;
                    padding: 15px;
                    font-size: 18px;
                    font-weight: bold;
                    color: #d1fae5;
                    margin: 10px;
                }
            """)
        else:
            self.result.setText(f"❌ INVALID • {s:.1f}%")
            self.result.setStyleSheet("""
                QLabel {
                    background-color: #3a0d10;
                    border: 2px solid #ef4444;
                    border-radius: 8px;
                    padding: 15px;
                    font-size: 18px;
                    font-weight: bold;
                    color: #fecaca;
                    margin: 10px;
                }
            """)
