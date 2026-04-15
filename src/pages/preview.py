import sys, os, csv

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy,
    QLabel, QFrame, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QScrollArea, QApplication, QMainWindow
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

from src.utils.font import Fonts
from src.utils.layout import AppLayout  

CSV_PATH = r"src/contents/dataset.csv"


def load_data():
    rows_2018, rows_2021 = [], []
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            country = row['Country'].strip()
            def v(key, r=row):
                try: return float(r[key])
                except: return None
            rows_2018.append([
                country,
                f"{v('All individuals (2018)'):.1f}" if v('All individuals (2018)') is not None else "—",
                f"{v('Individuals - GenY (2018)'):.1f}" if v('Individuals - GenY (2018)') is not None else "—",
                f"{v('Individuals - GenX (2018)'):.1f}" if v('Individuals - GenX (2018)') is not None else "—",
            ])
            rows_2021.append([
                country,
                f"{v('All individuals (2021)'):.1f}" if v('All individuals (2021)') is not None else "—",
                f"{v('Individuals - GenY (2021)'):.1f}" if v('Individuals - GenY (2021)') is not None else "—",
                f"{v('Individuals - GenX (2021)'):.1f}" if v('Individuals - GenX (2021)') is not None else "—",
            ])
    all_rows = []
    for a, b in zip(rows_2018, rows_2021):
        def avg_str(va, vb):
            try: return f"{(float(va) + float(vb)) / 2:.1f}"
            except: return va if va != "—" else vb
        all_rows.append([a[0], avg_str(a[1],b[1]), avg_str(a[2],b[2]), avg_str(a[3],b[3])])
    return {"2018": rows_2018, "2021": rows_2021, "All": all_rows}


class DataTable(QTableWidget):
    """QTableWidget dengan kolom rata dan scroll vertikal."""
    COLUMNS = ["Country", "All Ind", "Gen Y", "Gen X"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColumnCount(len(self.COLUMNS))
        self.setHorizontalHeaderLabels(self.COLUMNS)

        # ── Tampilan umum ──
        self.setShowGrid(False)
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.verticalHeader().setVisible(False)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # ── Lebar kolom rata (stretch semua) ──
        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))

        # ── Tinggi baris ──
        self.verticalHeader().setDefaultSectionSize(42)

        # ── Scroll hanya vertikal, horizontal disembunyikan ──
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # ── Stylesheet ──
        self.setStyleSheet("""
            QTableWidget {
                background-color: #FFFFFF;
                border: none;
                border-radius: 10px;
                font-family: 'Segoe UI';
                font-size: 10pt;
                color: #1A2A4A;
                outline: none;
            }
            QTableWidget::item {
                padding: 8px 12px;
                border-bottom: 1px solid #EEF1F6;
            }
            QTableWidget::item:selected {
                background-color: #EBF4FF;
                color: #1A2A4A;
            }
            QHeaderView::section {
                background-color: #F4F7FB;
                color: #4A5568;
                padding: 10px 12px;
                border: none;
                border-bottom: 2px solid #DDE4EF;
                font-weight: bold;
                font-size: 10pt;
            }
            QScrollBar:vertical {
                background: #F4F7FB;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #BCC8DC;
                border-radius: 4px;
                min-height: 30px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QTableWidget::item:alternate {
                background-color: #F9FAFB;
            }
        """)

    def set_rows(self, rows: list):
        self.setRowCount(len(rows))
        for r_idx, row in enumerate(rows):
            for c_idx, val in enumerate(row):
                item = QTableWidgetItem(str(val))
                # Country rata kiri, angka rata tengah
                if c_idx == 0:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
                else:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.setItem(r_idx, c_idx, item)


class YearFilterRow(QWidget):
    def __init__(self, on_change, parent=None):
        super().__init__(parent)
        self.on_change = on_change
        self.current = "All"

        hl = QHBoxLayout(self)
        hl.setContentsMargins(0, 0, 0, 0)
        hl.setSpacing(6)
        hl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.buttons = {}
        for label in ("2018", "2021", "All"):
            btn = QPushButton(label)
            btn.setFixedHeight(34)
            btn.setMinimumWidth(72)
            btn.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _, l=label: self._select(l))
            self.buttons[label] = btn
            hl.addWidget(btn)

        self._refresh_styles()

    def _refresh_styles(self):
        for label, btn in self.buttons.items():
            if label == self.current:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #2E86DE;
                        color: white;
                        border: 1.5px solid #2E86DE;
                        border-radius: 7px;
                        font-weight: 700;
                        padding: 0 14px;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #FFFFFF;
                        color: #555;
                        border: 1.5px solid #BCC8DC;
                        border-radius: 7px;
                        font-weight: 500;
                        padding: 0 14px;
                    }
                    QPushButton:hover { background-color: #F0F5FF; }
                """)

    def _select(self, year):
        self.current = year
        self._refresh_styles()
        self.on_change(year)


class Preview(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.data = load_data()
        self._build_ui()

    def _build_ui(self):
        self.setStyleSheet("background-color: #DDE4EF;")

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        # ── Card putih ──
        card = QFrame()
        card.setObjectName("card")
        card.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        card.setStyleSheet("""
            QFrame#card {
                background-color: #FFFFFF;
                border-radius: 16px;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(28, 24, 28, 24)
        card_layout.setSpacing(0)

        # Judul
        title = QLabel("2. Data Preview")
        title.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        title.setStyleSheet("color: #1A2A4A; background: transparent;")
        card_layout.addWidget(title)
        card_layout.addSpacing(18)

        # Filter tahun
        self.filter_row = YearFilterRow(on_change=self._apply_filter)
        card_layout.addWidget(self.filter_row, alignment=Qt.AlignmentFlag.AlignCenter)
        card_layout.addSpacing(16)

        # ── Tabel dengan scroll ──
        self.table = DataTable()
        self.table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        card_layout.addWidget(self.table, stretch=1)
        card_layout.addSpacing(20)

        # Tombol Back / Next
        nav = QHBoxLayout()
        btn_back = QPushButton("Back")
        btn_back.setFixedSize(92, 36)
        btn_back.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_back.setStyleSheet("""
            QPushButton {
                background: white; color: #2E86DE;
                border: 1.5px solid #2E86DE;
                border-radius: 8px; font-weight: 600;
            }
            QPushButton:hover { background: #EBF4FF; }
        """)
        btn_next = QPushButton("Next")
        btn_next.setFixedSize(92, 36)
        btn_next.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))
        btn_next.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_next.setStyleSheet("""
            QPushButton {
                background: #2E86DE; color: white;
                border: none; border-radius: 8px; font-weight: 600;
            }
            QPushButton:hover { background: #1A72C8; }
        """)
        nav.addWidget(btn_back)
        nav.addStretch()
        nav.addWidget(btn_next)
        card_layout.addLayout(nav)

        outer.addWidget(card)
        self._apply_filter("All")

    def _apply_filter(self, year: str):
        self.table.set_rows(self.data[year])

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1000, 750)

        self.app_layout = AppLayout(current_step=2)

        isi = Preview()
        self.app_layout.set_content(isi)

        self.setCentralWidget(self.app_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    Fonts().load_fonts()

    win = MainWindow()
    win.show()
    sys.exit(app.exec())