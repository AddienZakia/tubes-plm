from PyQt6.QtWidgets import QApplication, QMainWindow
import sys


from src.components.typography import Typography
from src.utils.font import Fonts
from src.utils.layout import AppLayout  
from src.components.upload_file import UploadFile
from src.components import Image
from src.components import VBox, HBox, Button, Typography, Colors
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QColor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1000, 750)

        self.app_layout = AppLayout(current_step=1)

        vbox = VBox(spacing=20)
        widget = QWidget()
        widget.setFixedSize(1000, 750)

        teks = HBox(spacing=5)
        teks.addWidget(Typography("1. ", variant='p', color=Colors.primary_hover, weight="bold"))
        teks.addWidget(Typography("Upload Data", variant='p', weight="bold", color=Colors.neutral_black))
        teks.addStretch()

        upload = UploadFile(accept="CSV Files (*.csv)")
        

        button_container = HBox() # Margin kiri 50, kanan 50
        button_container = HBox(spacing=30)
        button_container.addSpacing(20)
        btn_back = Button("Back", variant="primary", size="md")
        button_container.addWidget(btn_back)
        button_container.addStretch()
        
        vbox.addLayout(teks)
        vbox.addWidget(upload)
        vbox.addSpacing(180)

        vbox.addLayout(button_container)
        vbox.addSpacing(150)
 
        widget.setLayout(vbox)
        self.app_layout.set_content(widget)

        self.setCentralWidget(self.app_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    Fonts().load_fonts()

    win = MainWindow()
    win.show()
    sys.exit(app.exec())