from PyQt6.QtWidgets import QApplication, QMainWindow
import sys

from src.components.typography import Typography, Colors
from src.utils.font import Fonts
from src.utils.layout import AppLayout  
from src.components import VBox, HBox, Button, Typography, Image
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget
from src.components import Button


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        
        self.setFixedSize(1000, 750)
        
        self.app_layout = AppLayout()
        # ---- 
        
        vbox = VBox(spacing=20)
        
        teks = HBox(spacing=10, margin=(0, 0, 0, 0)) 
        teks.addWidget(Typography("FCM", variant='h4', color=Colors.primary_hover, weight="bold"))
        teks.addWidget(Typography("Clustering App", variant='h4', weight="bold", color=Colors.neutral_black))
        
        teks1 = Typography("Cluster your data using the Fuzzy C-Means (FCM)", variant='p', color=Colors.neutral_black, align=Qt.AlignmentFlag.AlignCenter)
        img = Image('assets/image/Gambar page 1.png')
        
        button_container = HBox(margin=(0, 50, 0, 50)) # Margin kiri 50, kanan 50
        button_container = HBox(spacing=30)
        button_container.addSpacing(50)
        btn_recent = Button("Recent", variant="primary", size="md")
        btn_start = Button("Start", variant="primary", size="md")
        button_container.addStretch() # Stretch kiri
        button_container.addWidget(btn_recent)
        button_container.addWidget(btn_start)
        button_container.addStretch() # Stretch kanan
        
        vbox.addSpacing(75)
        vbox.addLayout(teks)
        vbox.setAlignment(teks, Qt.AlignmentFlag.AlignHCenter)
        
        vbox.addWidget(teks1)
        vbox.addSpacing(10)
        
        vbox.addWidget(img, alignment=Qt.AlignmentFlag.AlignCenter)
        vbox.addStretch()
        
        vbox.addLayout(button_container)
        vbox.addSpacing(150)
        
        widget.setLayout(vbox)
        
        
        # ----
        self.app_layout.set_content(widget)
        self.setCentralWidget(self.app_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    Fonts().load_fonts()

    win = MainWindow()
    win.show()
    sys.exit(app.exec())