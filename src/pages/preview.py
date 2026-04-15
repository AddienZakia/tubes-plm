import sys, os, csv

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy,
    QLabel, QFrame, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QScrollArea, QApplication, QMainWindow
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

from src.components.button import Button
from src.components.layout import HBox, VBox
from src.components.pagination_table import PaginationTable
from src.components.typography import Typography
from src.components.colors import Colors
from src.utils.font import Fonts
from src.utils.layout import AppLayout  
from .result import MainWindow as ResultPage

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


class Preview(QWidget):
    def __init__(self, router, parent=None):
        super().__init__(parent)
        self.router   = router
        self._data    = {"2018": [], "2021": [], "All": []}
        self._csv_path = None
        self._build_ui()
 
    def _build_ui(self):
        root = VBox(spacing=16)
        self.setLayout(root)
 
        # Header
        text_header = HBox(spacing=4)
        num   = Typography("2.", variant='p', weight="bold", color=Colors.primary_active)
        title = Typography("Data Preview", variant='p', weight="bold", color=Colors.neutral_black)
        text_header.addWidget(num)
        text_header.addWidget(title)
        text_header.setAlignment(Qt.AlignmentFlag.AlignLeft)
 
        # Filter tombol
        filter_row = HBox(spacing=8, align=Qt.AlignmentFlag.AlignCenter)
        self._filter_buttons = {}
        self._active_year = "All"
        for label in ("2018", "2021", "All"):
            btn = Button(label, variant="outline_blue" if label != "All" else "primary", size="sm")
            btn.clicked.connect(lambda _, l=label: self._apply_filter(l))
            self._filter_buttons[label] = btn
            filter_row.addWidget(btn)
 
        # Tabel
        self.table = PaginationTable(
            columns=["Country", "All Ind", "Gen Y", "Gen X"],
            rows=[],
            page_size=10,
        )
 
        # Tombol nav
        nav = HBox(spacing=12)
        btn_back = Button("Back", variant="outline_blue", size="md")
        btn_next = Button("Next", variant="primary",      size="md")
        nav.addWidget(btn_back)
        nav.addStretch()
        nav.addWidget(btn_next)
 
        root.addLayout(text_header)
        root.addLayout(filter_row)
        root.addWidget(self.table, stretch=1)
        root.addLayout(nav)
 
        btn_back.clicked.connect(self.router.show_upload_b)
        btn_next.clicked.connect(self._run_clustering)
 
    def load_csv(self, path: str):
        self._csv_path = path
        rows_2018, rows_2021 = [], []
 
        try:
            with open(path, newline='', encoding='utf-8') as f:
                reader = __import__('csv').DictReader(f, delimiter=';')
                for row in reader:
                    country = row.get('Country', '').strip()
                    def v(k, r=row):
                        try: return float(r[k])
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
                all_rows.append([a[0], avg_str(a[1], b[1]), avg_str(a[2], b[2]), avg_str(a[3], b[3])])
 
            self._data = {"2018": rows_2018, "2021": rows_2021, "All": all_rows}
            self._apply_filter(self._active_year)
 
        except Exception as e:
            print(f"[PreviewPage] Gagal baca CSV: {e}")
 
    def _apply_filter(self, year: str):
        self._active_year = year
        # Update gaya tombol
        for label, btn in self._filter_buttons.items():
            btn.set_variant("primary" if label == year else "outline_blue")
        self.table.set_rows(self._data.get(year, []))
 
    def _run_clustering(self):
        """Jalankan FCM lalu pindah ke halaman result."""
        if not self._csv_path:
            return
        try:
            from src.utils.model import FCM
            model = FCM(C=3, m=2, path=self._csv_path)
            model.fit()
            columns, rows = model.result()
            stats = {
                "cluster":  model.C,
                "iterasi":  len(model.history_J),
                "m":        model.m,
                "history_J": model.history_J,
            }
            result_page = self.router.page_result.findChild(ResultPage)
            if result_page:
                result_page.load_result(columns, rows, stats)
        except Exception as e:
            print(f"[PreviewPage] FCM gagal: {e}")
 
        self.router.go_to(4)

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setFixedSize(1000, 750)

#         self.app_layout = AppLayout(current_step=2)

#         isi = Preview()
#         self.app_layout.set_content(isi)

#         self.setCentralWidget(self.app_layout)


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     app.setStyle("Fusion")
#     Fonts().load_fonts()

#     win = MainWindow()
#     win.show()
#     sys.exit(app.exec())