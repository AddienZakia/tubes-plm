from PyQt6.QtWidgets import QApplication, QMainWindow
import sys

from src.components.typography import Typography
from src.utils.font import Fonts
from src.utils.layout import AppLayout  

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1000, 750)

        self.app_layout = AppLayout(current_step=1)

        page = Typography("Hello world", variant='h4')
        self.app_layout.set_content(page)

        self.setCentralWidget(self.app_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    Fonts().load_fonts()

    win = MainWindow()
    win.show()
    sys.exit(app.exec())