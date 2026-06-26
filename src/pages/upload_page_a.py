import os

from PyQt6.QtWidgets import QApplication, QFileDialog, QMainWindow
import sys

from src.utils import AppLayout, Fonts
from src.components import VBox, HBox, Button, Typography, Colors, UploadFile
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt

from .upload_page_b import UploadPageB

class MainWindow(QWidget):
    def __init__(self, router, parent=None):
        super().__init__(parent)
        self.router = router
        self._build_ui()
 
    def _build_ui(self):
        vbox = VBox(spacing=20, align=Qt.AlignmentFlag.AlignVCenter)
        self.setLayout(vbox)
 
        teks = HBox(spacing=5, align=Qt.AlignmentFlag.AlignLeft)
        teks.addWidget(Typography("1. ", variant='p', color=Colors.primary_hover, weight="bold"))
        teks.addWidget(Typography("Upload Data", variant='p', weight="bold", color=Colors.neutral_black))
 
        self.upload_widget = UploadFile(accept="CSV Files (*.csv)")
        self.upload_widget.setFixedHeight(500)
 
        button_container = HBox(spacing=30)
        button_container.addSpacing(20)
        btn_back = Button("Back", variant="outline_blue", size="md")
 
        button_container.addWidget(btn_back)
 
        vbox.addLayout(teks)
        vbox.addStretch()
        vbox.addWidget(self.upload_widget)
        vbox.addStretch()
        vbox.addLayout(button_container)
 
        # ── navigasi ──────────────────────────────────────────
        btn_back.clicked.connect(self.router.show_home)
 
        # Ketika file sudah dipilih via UploadFile → pindah ke state B
        # Asumsi: UploadFile punya signal `file_selected(path)` atau kita
        # override via file-dialog. Sesuaikan dengan implementasi UploadFile kamu.
        try:
            self.upload_widget.file_selected.connect(self._on_file_selected)
        except AttributeError:
            # Jika UploadFile belum punya signal, pasang tombol manual
            btn_open = Button("Pilih File CSV", variant="outline_blue", size="md")
            btn_open.clicked.connect(self._open_dialog)
            vbox.insertWidget(vbox.count() - 1, btn_open)
 
    def _open_dialog(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Pilih File CSV", "", "CSV Files (*.csv)"
        )
        if path:
            self._on_file_selected(path)
 
    def _on_file_selected(self, path: str):
        """Baca CSV lalu pindah ke UploadPageB."""
        import csv as _csv
        rows = []
        with open(path, newline='', encoding='utf-8') as f:
            reader = _csv.reader(f, delimiter=';')
            for row in reader:
                rows.append(row)
 
        # Simpan ke recent
        self._save_recent(path)
 
        # Pindah ke state B dengan membawa data
        b_page = self.router.page_upload_b.findChild(UploadPageB)
        if b_page:
            b_page.load_file(path, rows)
        self.router.go_to(2)
 
    @staticmethod
    def _save_recent(path: str):
        import json, datetime
        recent_path = "src/contents/data_recent.json"
        data = []
        if os.path.exists(recent_path):
            try:
                with open(recent_path, "r") as f:
                    data = json.load(f)
            except Exception:
                data = []
        data.append({
            "date": datetime.datetime.now().strftime("%Y/%m/%d - %H:%M:%S"),
            "file": os.path.basename(path),
            "path": path,
        })
        with open(recent_path, "w") as f:
            json.dump(data, f, indent=4)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    Fonts().load_fonts()

    win = MainWindow()
    win.show()
    sys.exit(app.exec())