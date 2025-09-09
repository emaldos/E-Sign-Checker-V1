from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox, QGridLayout, QLineEdit, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
from .styles import button_style
from .signature_canvas import SignatureCanvas

class AddSignatureTab(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.owner = None
        self.title = None
        self.notes = None
        self.canvas = None
        self._build()
    def _build(self):
        layout = QVBoxLayout(self)
        info = QGroupBox("")
        g = QGridLayout(info)
        self.owner = QLineEdit(); self.owner.setPlaceholderText("Owner")
        self.title = QLineEdit(); self.title.setPlaceholderText("Title/Position")
        self.notes = QLineEdit(); self.notes.setPlaceholderText("Notes")
        g.addWidget(self.owner, 0, 0)
        g.addWidget(self.title, 0, 1)
        g.addWidget(self.notes, 0, 2)
        layout.addWidget(info)
        draw = QGroupBox("Draw Signature")
        v = QVBoxLayout(draw)
        self.canvas = SignatureCanvas(drawing_enabled=True)
        v.addWidget(self.canvas)
        row = QHBoxLayout()
        btn_clear = QPushButton("🗑️ Clear"); btn_clear.setStyleSheet(button_style("#ef4444")); btn_clear.clicked.connect(self.canvas.clear)
        btn_save = QPushButton("💾 Save"); btn_save.setStyleSheet(button_style("#22c55e")); btn_save.clicked.connect(self._save)
        row.addWidget(btn_clear); row.addStretch(); row.addWidget(btn_save)
        v.addLayout(row)
        layout.addWidget(draw)
    def _save(self):
        o = self.owner.text().strip()
        if not o: return
        t = self.title.text().strip()
        n = self.notes.text().strip()
        data = self.canvas.to_bytes()
        ok = self.db.save_signature(o, t, data, n)
        if ok:
            self.owner.clear(); self.title.clear(); self.notes.clear(); self.canvas.clear()
