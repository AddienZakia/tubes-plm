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


class AppLayout(QWidget):
    def __init__(self, current_step=1, parent=None):
        super().__init__(parent)

        base_dir = os.path.dirname(__file__)
        image_path = os.path.abspath(
            os.path.join(base_dir, "../../assets/image/layout-bg.png")
        )

        root = VBox(spacing=0, margin=(16, 16, 16, 16))
        bg = BgWidget(image_path)
        bg.setLayout(root)

        header = HBox(spacing=0, margin=(0, 0, 0, 14))

        brand = HBox(spacing=6, margin=(0, 0, 0, 0))
        brand.addWidget(Typography("FCM", variant='h4', weight="bold", color=Colors.primary_hover))
        brand.addWidget(Typography("Clustering App", variant='h4', weight="bold", color=Colors.neutral_black))

        # Stepper
        stepper = self._build_stepper(current_step)

        header.addLayout(brand)
        header.addStretch()
        header.addLayout(stepper)

        self.content_frame = QFrame()
        self.content_frame.setObjectName("contentFrame")
        self.content_frame.setStyleSheet("""
            QFrame#contentFrame {
                background-color: white;
                border: 1px solid #d1d5db;
                border-radius: 14px;
            }
        """)
        self.content_frame.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )
        self.content_layout = VBox(spacing=0, margin=(16, 16, 16, 16))
        self.content_frame.setLayout(self.content_layout)

        root.addLayout(header)
        root.addWidget(self.content_frame)

        outer = VBox(spacing=0, margin=(0, 0, 0, 0))
        outer.addWidget(bg)
        self.setLayout(outer)  # <-- pakai outer, bukan root

    def _build_stepper(self, current_step):
        steps = [(1, "Upload"), (2, "Preprocessing"), (3, "Run"), (4, "Result")]
        layout = HBox(spacing=4, margin=(0, 0, 0, 0), align=Qt.AlignmentFlag.AlignVCenter)

        for i, (num, label) in enumerate(steps):
            step_widget = self._step_item(num, label, current_step)
            layout.addLayout(step_widget)

            if i < len(steps) - 1:
                line = QFrame()
                line.setFrameShape(QFrame.Shape.HLine)
                line.setFixedWidth(28)
                line.setFixedHeight(1)
                color = Colors.primary_hover if num < current_step else "#d1d5db"
                line.setStyleSheet(f"background-color: {color}; border: none;")
                layout.addWidget(line)

        return layout

    def _step_item(self, num, label, current_step):
        layout = HBox(spacing=4, margin=(0, 0, 0, 0), align=Qt.AlignmentFlag.AlignVCenter)

        if num < current_step:
            circle = Typography("✓", variant='b', weight="bold", color=Colors.primary_active)
            circle.setFixedSize(24, 24)
            circle.setAlignment(Qt.AlignmentFlag.AlignCenter)
            circle.setStyleSheet("background-color: #22c55e; border-radius: 12px;")
            label_color = "#22c55e"
        elif num == current_step:
            circle = Typography(str(num), variant='b', weight="bold", color=Colors.primary_main)
            circle.setFixedSize(24, 24)
            circle.setAlignment(Qt.AlignmentFlag.AlignCenter)
            circle.setStyleSheet(f"border: 1.5px solid {Colors.primary_hover}; border-radius: 12px; color: {Colors.primary_main}")
            label_color = Colors.primary_hover
        else:
            circle = Typography(str(num), variant='b', color=Colors.primary_active)
            circle.setFixedSize(24, 24)
            circle.setAlignment(Qt.AlignmentFlag.AlignCenter)
            circle.setStyleSheet("border: 1.5px solid #d1d5db; border-radius: 12px;")
            label_color = Colors.neutral_40

        lbl = Typography(label, variant='b', color=label_color)
        layout.addWidget(circle)
        layout.addWidget(lbl)
        return layout

    def set_content(self, widget: QWidget):
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.content_layout.addWidget(widget)