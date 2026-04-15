from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
import sys

from src.components.typography import Typography
from src.utils.font import Fonts
from src.utils.layout import AppLayout  

from src.components.pagination_table import PaginationTable
from src.components import HBox, VBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1000, 750)
        self.app_layout = AppLayout(current_step=1)

        widget = QWidget()
        # -----

        vb = VBox()

        rows = [[f"Negara {i}", i * 10, i * 5, i % 3] for i in range(1, 36)]

        # basic
        tbl = PaginationTable(
            columns=["Negara", "Val A", "Val B", "Cluster"],
            rows=rows,
            page_size=10,   # default 10 baris per halaman
        )

        vb.addWidget(tbl)

        widget.setLayout(vb)

        # --------
        self.app_layout.set_content(widget)
        self.setCentralWidget(self.app_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    Fonts().load_fonts()

    win = MainWindow()
    win.show()
    sys.exit(app.exec())