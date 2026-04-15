import os

from PyQt6.QtWidgets import QApplication, QMainWindow
import sys

from src.utils.font import Fonts
from src.utils.layout import AppLayout  
from .preview import Preview as PreviewPage


# ================== MAIN WINDOW ==================
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setFixedSize(1000, 750)

#         self.app_layout = AppLayout(current_step=1)

#         # isi konten dengan halaman Upload
#         page = UploadPage()
#         self.app_layout.set_content(page)

#         self.setCentralWidget(self.app_layout)


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
    """Kartu info file yang sudah diupload."""
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
 
        root = HBox(spacing=12, margin=(16, 14, 16, 14), align=Qt.AlignmentFlag.AlignVCenter)
        self.setLayout(root)
 
        icon_lbl = QLabel("📄")
        icon_lbl.setStyleSheet("font-size: 28px; background: transparent;")
        icon_lbl.setFixedWidth(36)
        root.addWidget(icon_lbl)
 
        meta_col = VBox(spacing=2)
        meta_col.setContentsMargins(0, 0, 0, 0)
 
        self.lbl_name = Typography("—", variant="t", weight="bold", color=Colors.neutral_black)
        self.lbl_meta = Typography("—", variant="c", color=Colors.neutral_60)
 
        meta_col.addWidget(self.lbl_name)
        meta_col.addWidget(self.lbl_meta)
 
        meta_widget = QWidget()
        meta_widget.setLayout(meta_col)
        meta_widget.setStyleSheet("background: transparent;")
        root.addWidget(meta_widget, stretch=1)
 
        self.lbl_rows = Typography("—", variant="c", color=Colors.neutral_70)
        self.lbl_cols = Typography("—", variant="c", color=Colors.neutral_70)
        root.addWidget(self.lbl_rows)
        root.addWidget(self.lbl_cols)
 
    def update_file_info(self, filename, size_kb, n_rows, n_cols):
        self.lbl_name.setText(filename)
        self.lbl_meta.setText(f"Just uploaded • {size_kb:.1f} KB • UTF-8")
        self.lbl_rows.setText(f"{n_rows} baris")
        self.lbl_cols.setText(f"{n_cols} kolom")
 
 
class UploadPageB(QWidget):
    COLUMNS = [
        "#", "Country",
        "All_2018", "All_2021",
        "GenY_2018", "GenY_2021",
        "GenX_2018", "GenX_2021",
        "Men_GenY_18", "Men_GenY_21",
    ]
 
    def __init__(self, router, parent=None):
        super().__init__(parent)
        self.router     = router
        self._csv_path  = None
        self._csv_rows  = []
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
 
        self.file_card = FileInfoCard()
 
        self.table = PaginationTable(
            columns=self.COLUMNS,
            rows=[],
            page_size=8,
        )
 
        button_container = HBox(spacing=12)
        btn_back = Button("Back", variant="outline_blue", size="md")
        btn_next = Button("Next", variant="primary",      size="md")
        button_container.addWidget(btn_back)
        button_container.addStretch()
        button_container.addWidget(btn_next)
 
        root.addLayout(text_header)
        root.addWidget(self.file_card)
        root.addWidget(self.table, stretch=1)
        root.addLayout(button_container)
 
        # ── navigasi ──────────────────────────────────────────
        btn_back.clicked.connect(self.router.show_upload_a)
        btn_next.clicked.connect(self._go_next)
 
    def load_file(self, path: str, raw_rows: list):
        """Dipanggil oleh UploadPageA setelah file dipilih."""
        self._csv_path = path
        size_kb = os.path.getsize(path) / 1024
 
        # Baris pertama = header, sisanya = data
        data_rows = raw_rows[1:] if len(raw_rows) > 1 else []
        n_rows = len(data_rows)
        n_cols = len(raw_rows[0]) if raw_rows else 0
 
        self.file_card.update_file_info(
            os.path.basename(path), size_kb, n_rows, n_cols
        )
 
        # Tampilkan 10 kolom pertama di tabel preview
        table_rows = []
        for i, row in enumerate(data_rows):
            preview = [i + 1] + row[:9]   # "#" + max 9 kolom
            table_rows.append(preview)
 
        self._csv_rows = table_rows
        self.table.set_rows(table_rows)
 
    def _go_next(self):
        preview = self.router.page_preview.findChild(PreviewPage)
        if preview and self._csv_path:
            preview.load_csv(self._csv_path)
        self.router.go_to(3)



# ================== RUN APP ==================
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     app.setStyle("Fusion")
#     Fonts().load_fonts()

#     win = MainWindow()
#     win.show()
#     sys.exit(app.exec())