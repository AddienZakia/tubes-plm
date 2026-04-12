import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontDatabase, QFont
from src.components import Typography, VBox, Colors
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FCM Clustering App")
        self.setFixedSize(1000, 750)

        # load fonts
        loc_fonts = os.listdir("assets/fonts")
        for font in loc_fonts:
            QFontDatabase.addApplicationFont(os.path.join("assets/fonts", font))


        central = QWidget()
        central.setStyleSheet(f"background-color: {Colors.neutral_10};")
        layout = VBox(
            spacing=0,
            align=Qt.AlignmentFlag.AlignCenter,
            margin=(0, 0, 0, 0),
        )
        central.setLayout(layout)

        placeholder = Typography(
            "FCM Clustering — coming soon",
            variant="h5",
            color=Colors.neutral_50,
            align=Qt.AlignmentFlag.AlignCenter,
            weight="bold"
        )
        layout.addWidget(placeholder)

        self.setCentralWidget(central)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = MainWindow()
    win.show()
    sys.exit(app.exec())