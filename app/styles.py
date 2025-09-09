def adjust_color(hex_color, delta):
    h = hex_color.lstrip("#")
    r = max(0, min(255, int(h[0:2], 16) + delta))
    g = max(0, min(255, int(h[2:4], 16) + delta))
    b = max(0, min(255, int(h[4:6], 16) + delta))
    return f"#{r:02x}{g:02x}{b:02x}"

def button_style(color):
    return f"""
        QPushButton {{
            background-color: {color};
            border: none;
            color: #ffffff;
            padding: 12px 24px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: bold;
            min-width: 120px;
        }}
        QPushButton:hover {{
            background-color: {adjust_color(color, 20)};
        }}
        QPushButton:pressed {{
            background-color: {adjust_color(color, -20)};
        }}
    """

def dark_stylesheet():
    return """
        QMainWindow { background-color: #0b0f14; }
        QTabWidget::pane { border: 1px solid #1f2937; }
        QTabBar::tab { background: #0b0f14; color: #e5e7eb; padding: 8px 14px; border: 1px solid #1f2937; border-bottom: none; }
        QTabBar::tab:selected { background: #111827; }
        QFrame {
            background-color: #0f141a;
            border: 1px solid #1f2937;
            border-radius: 12px;
            margin: 5px;
        }
        QGroupBox {
            font-weight: bold;
            font-size: 16px;
            border: 2px solid #3b82f6;
            border-radius: 10px;
            margin-top: 15px;
            padding-top: 10px;
            background-color: #0f141a;
            color: #e5e7eb;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 15px;
            padding: 0 10px 0 10px;
            background-color: #3b82f6;
            color: #0b0f14;
            border-radius: 5px;
        }
        QLineEdit {
            border: 2px solid #1f2937;
            border-radius: 6px;
            padding: 8px;
            font-size: 14px;
            background-color: #0b0f14;
            color: #e5e7eb;
        }
        QLineEdit:focus { border-color: #3b82f6; }
        QTextEdit {
            border: 2px solid #1f2937;
            border-radius: 6px;
            background-color: #0b0f14;
            color: #e5e7eb;
            font-family: Consolas, "Courier New", monospace;
            font-size: 12px;
            padding: 5px;
        }
        QMenuBar {
            background-color: #0b0f14;
            color: #e5e7eb;
            border: none;
            font-weight: bold;
        }
        QMenuBar::item:selected { background-color: #1f2937; }
        QMenu {
            background-color: #0b0f14;
            border: 1px solid #1f2937;
            color: #e5e7eb;
        }
        QMenu::item:selected { background-color: #2563eb; color: white; }
        QStatusBar {
            background-color: #0b0f14;
            color: #9ca3af;
            border-top: 1px solid #1f2937;
            font-weight: bold;
        }
        QLabel { color: #e5e7eb; }

        QTableView {
            background-color: #0b0f14;
            color: #e5e7eb;
            gridline-color: #1f2937;
            selection-background-color: #2563eb;
            selection-color: #ffffff;
            border: 1px solid #1f2937;
            border-radius: 8px;
        }
        QTableView::item {
            padding: 6px;
        }
        QHeaderView::section {
            background-color: #111827;
            color: #e5e7eb;
            padding: 8px 10px;
            border: 1px solid #1f2937;
            font-weight: 600;
        }
        QTableCornerButton::section {
            background-color: #111827;
            border: 1px solid #1f2937;
        }
        QScrollBar:vertical {
            background: #0b0f14;
            width: 12px;
            margin: 0;
        }
        QScrollBar::handle:vertical {
            background: #1f2937;
            min-height: 24px;
            border-radius: 6px;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
        QScrollBar:horizontal {
            background: #0b0f14;
            height: 12px;
            margin: 0;
        }
        QScrollBar::handle:horizontal {
            background: #1f2937;
            min-width: 24px;
            border-radius: 6px;
        }
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }
    """
