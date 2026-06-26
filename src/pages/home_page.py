from PyQt6.QtWidgets import QApplication, QMainWindow
import sys

from src.utils.font import Fonts
from src.utils import HomeLayout
from src.components import VBox, HBox, Button, Typography, Image, Colors
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget
from src.components import Button


class MainWindow(QWidget):
    def __init__(self, router, parent=None):
        super().__init__(parent)
        self.router = router
        self._build_ui()
 
    def _build_ui(self):
        vbox = VBox(spacing=20)
        self.setLayout(vbox)
 
        teks = HBox(spacing=10, margin=(0, 0, 0, 0))
        teks.addWidget(Typography("FCM", variant='h6', color=Colors.primary_hover, weight="bold"))
        teks.addWidget(Typography("Clustering App", variant='h6', weight="bold", color=Colors.neutral_black))
 
        teks1 = Typography(
            "Cluster your data using the Fuzzy C-Means (FCM)",
            variant='b', color=Colors.neutral_black,
            align=Qt.AlignmentFlag.AlignCenter
        )
 
        img = Image('assets/image/Gambar page 1.png')
 
        button_container = HBox(spacing=12)
        btn_recent = Button("Recent",  variant="outline_blue", size="md")
        btn_start  = Button("Start",   variant="primary",      size="md")
        btn_recent.setFixedWidth(200)
        btn_start.setFixedWidth(200)
        button_container.addStretch()
        button_container.addWidget(btn_recent)
        button_container.addWidget(btn_start)
        button_container.addStretch()
 
        # ── navigasi ──────────────────────────────────────────
        btn_recent.clicked.connect(self.router.show_recent)
        btn_start.clicked.connect(self.router.show_upload_a)
 
        vbox.addSpacing(75)
        vbox.addLayout(teks)
        vbox.setAlignment(teks, Qt.AlignmentFlag.AlignHCenter)
        vbox.addWidget(teks1)
        vbox.addSpacing(10)
        vbox.addWidget(img, alignment=Qt.AlignmentFlag.AlignCenter)
        vbox.addStretch()
        vbox.addLayout(button_container)
        vbox.addSpacing(100)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    Fonts().load_fonts()

    win = MainWindow()
    win.show()
    sys.exit(app.exec())