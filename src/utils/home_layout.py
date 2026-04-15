import os

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFrame, QSizePolicy
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtCore import Qt
from src.components.layout import VBox, HBox
from src.components.typography import Typography
from src.components.colors import Colors

class BgWidget(QWidget):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.pixmap = QPixmap(image_path)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap)


class HomeLayout(QWidget):
    def __init__(self, current_step=1, parent=None):
        super().__init__(parent)

        base_dir = os.path.dirname(__file__)
        image_path = os.path.abspath(
            os.path.join(base_dir, "../../assets/image/layout-bg.png")
        )

        root = VBox(spacing=0, margin=(32, 20, 32, 20))
        bg = BgWidget(image_path)
        bg.setLayout(root)

        header = HBox(spacing=0, margin=(0, 0, 0, 14))

        self.content_frame = QFrame()
        self.content_frame.setObjectName("contentFrame")
        self.content_frame.setStyleSheet("""
            QFrame#contentFrame {
                background-color: white;
                border: 1px solid #d1d5db;
                border-radius: 14px;
                height: 300px;
            }
        """)
        self.content_frame.setMaximumHeight(600)
        # self.content_frame.setSizePolicy(
        #     QSizePolicy.Policy.Minimum,
        #     QSizePolicy.Policy.Expanding,
        # )
        self.content_layout = VBox(spacing=0, margin=(16, 16, 16, 16))
        # self.content_layout.setSizeConstraint(
        #     QVBoxLayout.SizeConstraint.SetMinAndMaxSize
        # )
        self.content_frame.setLayout(self.content_layout)

        root.addLayout(header)
        root.addWidget(self.content_frame)

        outer = VBox(spacing=0, margin=(0, 0, 0, 0))
        outer.addWidget(bg)
        self.setLayout(outer)

    def set_content(self, widget: QWidget):
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.content_layout.addWidget(widget)