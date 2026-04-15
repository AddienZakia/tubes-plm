

import sys

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QWidget,
    QFileDialog, QSizePolicy, QFrame, QScrollArea,
    QHBoxLayout, QLabel, QVBoxLayout, QAbstractItemView,
    QTableWidget, QTableWidgetItem, QHeaderView, QPushButton,
    QTableWidgetItem
)

from src.utils.font import Fonts

from .home_page import MainWindow as HomePage
from .preview import Preview as PreviewPage
from .result import MainWindow as ResultPage
from .upload_page_a import MainWindow as UploadPageA
from .upload_page_b import UploadPageB

from src.utils import HomeLayout
from src.utils import AppLayout


class MainWindow(QMainWindow):
    """
    Router utama aplikasi.
    Menggunakan QStackedWidget untuk berpindah antar halaman.
 
    Index halaman:
        0 → HomePage
        1 → UploadPage  (state A: belum upload)
        2 → UploadPage  (state B: sudah upload, preview data)
        3 → PreviewPage (preview per tahun)
        4 → ResultPage
        5 → RecentPage
    """
 
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fuzzy C-Means Clustering")
        self.setFixedSize(1000, 750)
 
        # ── stack ──────────────────────────────────────────────
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
 
        # ── buat semua halaman ──────────────────────────────────
        self.page_home        = self._wrap_home(HomePage(self), current_step=1)
        self.page_upload_a    = self._wrap_app(UploadPageA(self),    current_step=1)
        self.page_upload_b    = self._wrap_app(UploadPageB(self),    current_step=1)
        self.page_preview     = self._wrap_app(PreviewPage(self),    current_step=2)
        self.page_result      = self._wrap_app(ResultPage(self),     current_step=4)
        # self.page_recent      = self._wrap_app(RecentPage(self),     current_step=1)
 
        # ── daftarkan ke stack (urutan = index) ─────────────────
        self.stack.addWidget(self.page_home)        # 0
        self.stack.addWidget(self.page_upload_a)    # 1
        self.stack.addWidget(self.page_upload_b)    # 2
        self.stack.addWidget(self.page_preview)     # 3
        self.stack.addWidget(self.page_result)      # 4
        # self.stack.addWidget(self.page_recent)      # 5
 
        self.stack.setCurrentIndex(0)
 
    def _wrap_home(self, content_widget, current_step=1):
        """Bungkus konten dengan AppLayout (dengan stepper)."""
        layout = HomeLayout(current_step=current_step)
        layout.set_content(content_widget)
        return layout
    
    def _wrap_app(self, content_widget, current_step=1):
        """Bungkus konten dengan AppLayout (dengan stepper)."""
        layout = AppLayout(current_step=current_step)
        layout.set_content(content_widget)
        return layout
 
    def go_to(self, index: int):
        self.stack.setCurrentIndex(index)
 
    # ── shortcut navigasi ────────────────────────────────────────
    def show_home(self):         self.go_to(0)
    def show_upload_a(self):     self.go_to(1)
    def show_upload_b(self, csv_path=None, csv_data=None):
        if csv_path and csv_data is not None:
            self.page_upload_b.findChild(UploadPageB).load_file(csv_path, csv_data)
        self.go_to(2)
    def show_preview(self, csv_path=None):
        if csv_path:
            self.page_preview.findChild(PreviewPage).load_csv(csv_path)
        self.go_to(3)
    def show_result(self, columns=None, rows=None, stats=None):
        if columns and rows:
            self.page_result.findChild(ResultPage).load_result(columns, rows, stats)
        self.go_to(4)
    def show_recent(self):       self.go_to(5)


# def _patch_router(router: MainWindow):
#     """Tambahkan metode navigasi tambahan setelah semua page dibuat."""
#     router.go_to_upload_b = lambda: router.go_to(2)
#     router.go_to_preview  = lambda: router.go_to(3)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    Fonts().load_fonts()
 
    win = MainWindow()
    # _patch_router(win)
    win.show()
    sys.exit(app.exec())
 