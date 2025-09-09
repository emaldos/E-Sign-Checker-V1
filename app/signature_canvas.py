import io
from PyQt6.QtWidgets import QWidget, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPixmap
from PIL import Image, ImageDraw

class SignatureCanvas(QWidget):
    def __init__(self, drawing_enabled=True, min_size=(600, 300), max_size=(2000, 1200)):
        super().__init__()
        self.drawing_enabled = drawing_enabled
        self.pen_width = 2
        self.pen_color = "#eef2f6"
        self.bg = "#14181d"
        self.image = Image.new("RGB", min_size, self.bg)
        self.draw = ImageDraw.Draw(self.image)
        self.last_point = None
        self.drawing = False
        self.pixmap = QPixmap()
        self.setMinimumSize(*min_size)
        self.setMaximumSize(*max_size)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._update_pix()
        self.setStyleSheet("""
            SignatureCanvas {
                background-color: #14181d;
                border: 2px solid #3b82f6;
                border-radius: 12px;
            }
        """)
    def _update_pix(self):
        buf = io.BytesIO()
        self.image.save(buf, format='PNG')
        self.pixmap.loadFromData(buf.getvalue())
    def resizeEvent(self, e):
        w = max(1, e.size().width())
        h = max(1, e.size().height())
        if (w, h) != self.image.size:
            self.image = self.image.resize((w, h))
            self.draw = ImageDraw.Draw(self.image)
            self._update_pix()
            self.update()
        super().resizeEvent(e)
    def mousePressEvent(self, e):
        if not self.drawing_enabled:
            return
        if e.button() == Qt.MouseButton.LeftButton:
            self.drawing = True
            self.last_point = (int(e.position().x()), int(e.position().y()))
    def mouseMoveEvent(self, e):
        if not self.drawing_enabled:
            return
        if self.drawing and e.buttons() & Qt.MouseButton.LeftButton:
            p = (int(e.position().x()), int(e.position().y()))
            self.draw.line([self.last_point, p], fill=self.pen_color, width=self.pen_width)
            self.last_point = p
            self._update_pix()
            self.update()
    def mouseReleaseEvent(self, e):
        self.drawing = False
    def paintEvent(self, e):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap, self.pixmap.rect())
    def clear(self):
        self.image = Image.new("RGB", (self.width(), self.height()), self.bg)
        self.draw = ImageDraw.Draw(self.image)
        self._update_pix()
        self.update()
    def load_bytes(self, b: bytes):
        img = Image.open(io.BytesIO(b)).convert("RGB")
        self.image = img.resize((max(1, self.width()), max(1, self.height())))
        self.draw = ImageDraw.Draw(self.image)
        self._update_pix()
        self.update()
    def to_bytes(self) -> bytes:
        buf = io.BytesIO()
        self.image.save(buf, format='PNG')
        return buf.getvalue()
