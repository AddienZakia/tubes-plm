from PyQt6.QtWidgets import QLabel, QSizePolicy
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap
from typing import Literal, Optional


ObjectFit = Literal["fill", "contain", "cover"]


class Image(QLabel):
    def __init__(
        self,
        src: Optional[str] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        object_fit: ObjectFit = "contain",
        rounded: int = 0,
        alt: str = "",
        parent=None,
    ):
        super().__init__(parent)

        self._src        = src
        self._width      = width
        self._height     = height
        self._object_fit = object_fit
        self._rounded    = rounded
        self._alt        = alt
        self._pixmap_raw: Optional[QPixmap] = None

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        if width:
            self.setFixedWidth(width)
        if height:
            self.setFixedHeight(height)

        if rounded:
            self.setStyleSheet(f"border-radius: {rounded}px; overflow: hidden;")

        if src:
            self.set_src(src)
        elif alt:
            self.setText(alt)

    def set_src(self, src: str):
        self._src = src
        pixmap = QPixmap(src)

        if pixmap.isNull():
            self.setText(self._alt or "Image not found")
            return

        self._pixmap_raw = pixmap
        self._render()

    def _render(self):
        if self._pixmap_raw is None:
            return

        w = self._width  or self._pixmap_raw.width()
        h = self._height or self._pixmap_raw.height()
        target = QSize(w, h)

        if self._object_fit == "fill":
            scaled = self._pixmap_raw.scaled(
                target,
                Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        elif self._object_fit == "cover":
            scaled = self._pixmap_raw.scaled(
                target,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation,
            )
            # center crop
            x = (scaled.width()  - w) // 2
            y = (scaled.height() - h) // 2
            scaled = scaled.copy(x, y, w, h)
        else:  # contain (default)
            scaled = self._pixmap_raw.scaled(
                target,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

        self.setPixmap(scaled)
        self.setFixedSize(scaled.size())

    def set_object_fit(self, object_fit: ObjectFit):
        self._object_fit = object_fit
        self._render()

    def set_size(self, width: int, height: int):
        self._width  = width
        self._height = height
        self.setFixedWidth(width)
        self.setFixedHeight(height)
        self._render()