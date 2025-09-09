import math, datetime
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QLabel as QL
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from .styles import button_style

PAGE_SIZE = 10

class HomeTab(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.search = None
        self.table = None
        self.prev_btn = None
        self.next_btn = None
        self.page_edit = None
        self.total_label = None
        self.refresh_btn = None
        self.total_pages = 1
        self.current_page = 1
        self._build()
        self._reload()
    def _build(self):
        layout = QVBoxLayout(self)
        top = QHBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search...")
        self.search.returnPressed.connect(self._go_first)
        top.addWidget(self.search)
        layout.addLayout(top)
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["ID","Owner","Title","Created","Notes","Signature"])
        self.table.setSelectionBehavior(self.table.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(self.table.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)
        bottom = QHBoxLayout()
        self.prev_btn = QPushButton("◀ Prev")
        self.prev_btn.setStyleSheet(button_style("#6b7280"))
        self.prev_btn.clicked.connect(self._prev)
        self.next_btn = QPushButton("Next ▶")
        self.next_btn.setStyleSheet(button_style("#6b7280"))
        self.next_btn.clicked.connect(self._next)
        self.page_edit = QLineEdit("1")
        self.page_edit.setFixedWidth(60)
        self.page_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.page_edit.returnPressed.connect(self._goto)
        self.total_label = QL("- 1")
        self.total_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.setStyleSheet(button_style("#3b82f6"))
        self.refresh_btn.clicked.connect(self._reload)
        bottom.addWidget(self.prev_btn)
        bottom.addWidget(self.next_btn)
        bottom.addSpacing(12)
        bottom.addWidget(QL("Page"))
        bottom.addWidget(self.page_edit)
        bottom.addWidget(self.total_label)
        bottom.addStretch()
        bottom.addWidget(self.refresh_btn)
        layout.addLayout(bottom)
    def _go_first(self):
        self.current_page = 1
        self._reload()
    def _prev(self):
        if self.current_page > 1:
            self.current_page -= 1
            self._reload()
    def _next(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self._reload()
    def _goto(self):
        try:
            p = int(self.page_edit.text().strip())
        except:
            p = self.current_page
        p = max(1, min(self.total_pages, p))
        self.current_page = p
        self._reload()
    def _reload(self):
        q = (self.search.text() or "").strip()
        total = self.db.count(q)
        self.total_pages = max(1, math.ceil(total / PAGE_SIZE))
        self.current_page = max(1, min(self.current_page, self.total_pages))
        self.page_edit.setText(str(self.current_page))
        self.total_label.setText(f"- {self.total_pages}")
        offset = (self.current_page - 1) * PAGE_SIZE
        rows = self.db.page(q, PAGE_SIZE, offset)
        self.table.setRowCount(0)
        for sig_id, owner, title, date, notes, blob in rows:
            r = self.table.rowCount()
            self.table.insertRow(r)
            self.table.setItem(r, 0, QTableWidgetItem(str(sig_id)))
            self.table.setItem(r, 1, QTableWidgetItem(owner or ""))
            self.table.setItem(r, 2, QTableWidgetItem(title or ""))
            dt = datetime.datetime.fromisoformat(date).strftime("%Y-%m-%d %H:%M")
            self.table.setItem(r, 3, QTableWidgetItem(dt))
            self.table.setItem(r, 4, QTableWidgetItem(notes or ""))
            thumb = QL()
            pm = QPixmap()
            pm.loadFromData(blob)
            pm = pm.scaled(120, 60, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            thumb.setPixmap(pm)
            thumb.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setCellWidget(r, 5, thumb)
            self.table.setRowHeight(r, 68)
