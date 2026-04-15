from PyQt6.QtWidgets import QApplication, QMainWindow
import sys

from src.utils.font import Fonts
from src.utils.layout import AppLayout  


# ================== MAIN WINDOW ==================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1000, 750)

        self.app_layout = AppLayout(current_step=1)

        # isi konten dengan halaman Upload
        page = UploadPage()
        self.app_layout.set_content(page)

        self.setCentralWidget(self.app_layout)


# ================== IMPORT UI ==================
from PyQt6.QtWidgets import (
    QWidget, QFileDialog, QSizePolicy, QFrame,
    QScrollArea, QHBoxLayout, QLabel
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QColor

from src.components.typography import Typography
from src.components.button import Button
from src.components.pagination_table import PaginationTable
from src.components.layout import VBox, HBox
from src.components.colors import Colors


# ================== FILE CARD ==================
class FileInfoCard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet(f"""
            FileInfoCard {{
                border: 1px solid {Colors.neutral_30};
                border-radius: 10px;
                background: {Colors.neutral_white};
            }}
        """)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        root = HBox(spacing=12, margin=(16, 14, 16, 14),  align=Qt.AlignmentFlag.AlignVCenter)
        self.setLayout(root)

        icon_lbl = QLabel("📄")
        icon_lbl.setStyleSheet("font-size: 28px; background: transparent;")
        icon_lbl.setFixedWidth(36)
        root.addWidget(icon_lbl)

        meta_col = VBox(spacing=2)
        meta_col.setContentsMargins(0, 0, 0, 0)

        self.lbl_name = Typography("data-plm.csv", variant="t", weight="bold",
                                   color=Colors.neutral_black)
        self.lbl_meta = Typography(
            "Just uploaded • 4.2 KB • UTF-8",
            variant="c",
            color=Colors.neutral_60,
        )

        meta_col.addWidget(self.lbl_name)
        meta_col.addWidget(self.lbl_meta)

        meta_widget = QWidget()
        meta_widget.setLayout(meta_col)
        meta_widget.setStyleSheet("background: transparent;")
        root.addWidget(meta_widget, stretch=1)

        self.lbl_rows = Typography("35 baris", variant="c", color=Colors.neutral_70)
        self.lbl_cols = Typography("15 kolom", variant="c", color=Colors.neutral_70)
        root.addWidget(self.lbl_rows)
        root.addWidget(self.lbl_cols)


    @staticmethod
    def _make_badge(text: str, fg: str, bg: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setStyleSheet(f"""
            QLabel {{
                background: {bg};
                color: {fg};
                border-radius: 6px;
                padding: 3px 10px;
                font-size: 12px;
                font-weight: 600;
                font-family: 'Plus Jakarta Sans';
            }}
        """)
        lbl.setFixedHeight(26)
        return lbl

    def update_file_info(self, filename: str, size_kb: float,
                         n_rows: int, n_cols: int, valid: bool):
        self.lbl_name.setText(filename)
        self.lbl_meta.setText(f"Just uploaded • {size_kb:.1f} KB • UTF-8")
        self.lbl_rows.setText(f"{n_rows} baris")
        self.lbl_cols.setText(f"{n_cols} kolom")

        if valid:
            self.badge.setText("✔  Valid CSV")
        else:
            self.badge.setText("✘  Invalid CSV")


# ================== LEGEND ==================
class ClusterLegend(QWidget):
    CLUSTERS = [
        ("Nordik / Eropa Barat", "#3b82f6"),
        ("Eropa Tengah", "#22c55e"),
        ("Eropa Selatan", "#f59e0b"),
        ("Eropa Timur / Balkan", "#a855f7"),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: transparent;")

        bar = HBox(spacing=20, margin=(4, 0, 4, 0), align=Qt.AlignmentFlag.AlignCenter )
        self.setLayout(bar)

        for label, color in self.CLUSTERS:
            dot = QLabel("●")
            dot.setStyleSheet(
                f"color: {color}; font-size: 14px; background: transparent;"
            )
            dot.setFixedWidth(16)

            txt = Typography(label, variant="c", color=Colors.neutral_70)

            pair = HBox(spacing=4)
            pair.addWidget(dot)
            pair.addWidget(txt)

            wrapper = QWidget()
            wrapper.setLayout(pair)
            wrapper.setStyleSheet("background: transparent;")
            bar.addWidget(wrapper)



# ================== UPLOAD PAGE ==================
class UploadPage(QWidget):
    COLUMNS = [
        "#", "Country",
        "All_2018", "All_2021",
        "GenY_2018", "GenY_2021",
        "GenX_2018", "GenX_2021",
        "Men_GenY_18", "Men_GenY_21",
    ]

    SAMPLE_ROWS = [
        [1, "Germany", 18, 17, 28, 25, 18, 19, 32, 28],
        [2, "France", 14, 13, 24, 21, 14, 15, 27, 24],
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._csv_rows = list(self.SAMPLE_ROWS)
        self._build_ui()

    def _build_ui(self):
        root = VBox(spacing=16)
        self.setLayout(root)

        text_header = HBox(spacing=4)
        num   = Typography("1   .", variant='p', weight="bold", color=Colors.primary_active)
        title = Typography("Upload Data", variant='p', weight="bold", color=Colors.neutral_black)
        text_header.addWidget(num)
        text_header.addWidget(title)
        text_header.setAlignment(Qt.AlignmentFlag.AlignLeft)

        root.addLayout(text_header)

        self.file_card = FileInfoCard()
        root.addWidget(self.file_card)

        self.table = PaginationTable(
            columns=self.COLUMNS,
            rows=self._csv_rows,
            page_size=8,
        )
        root.addWidget(self.table, stretch=1)

        self.legend = ClusterLegend()
        root.addWidget(self.legend)


# ================== RUN APP ==================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    Fonts().load_fonts()

    win = MainWindow()
    win.show()
    sys.exit(app.exec())