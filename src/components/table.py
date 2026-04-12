from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from typing import Optional
from .colors import Colors


class Table(QTableWidget):
    def __init__(
        self,
        columns: list[str],
        rows: list[list] = [],
        stretch_last: bool = True,
        parent=None,
    ):
        super().__init__(parent)

        self.columns = columns
        self.setColumnCount(len(columns))
        self.setHorizontalHeaderLabels(columns)

        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setAlternatingRowColors(True)
        self.verticalHeader().setVisible(False)
        self.setShowGrid(False)

        header = self.horizontalHeader()
        if stretch_last:
            header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        self._apply_style()

        if rows:
            self.set_rows(rows)

    def _apply_style(self):
        self.setStyleSheet(f"""
            QTableWidget {{
                background-color:    {Colors.neutral_white};
                alternate-background-color: {Colors.neutral_10};
                border:              1px solid {Colors.neutral_30};
                border-radius:       8px;
                outline:             none;
                font-family:         Inter;
                font-size:           13px;
                color:               {Colors.neutral_black};
                gridline-color:      transparent;
            }}
            QTableWidget::item {{
                padding:  8px 12px;
                border:   none;
            }}
            QTableWidget::item:selected {{
                background-color: #DBEAFE;
                color:            {Colors.neutral_black};
            }}
            QHeaderView::section {{
                background-color: {Colors.neutral_20};
                color:            {Colors.neutral_70};
                font-weight:      600;
                font-size:        12px;
                font-family:      Inter;
                padding:          8px 12px;
                border:           none;
                border-bottom:    1px solid {Colors.neutral_30};
            }}
            QScrollBar:vertical {{
                width: 6px;
                background: transparent;
            }}
            QScrollBar::handle:vertical {{
                background:    {Colors.neutral_40};
                border-radius: 3px;
            }}
        """)

    def set_rows(self, rows: list[list]):
        self.setRowCount(len(rows))

        for row_idx, row_data in enumerate(rows):
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
                self.setItem(row_idx, col_idx, item)

        self.resizeRowsToContents()

    def clear_rows(self):
        self.setRowCount(0)

    def append_row(self, row_data: list):
        row_idx = self.rowCount()
        self.insertRow(row_idx)

        for col_idx, value in enumerate(row_data):
            item = QTableWidgetItem(str(value))
            item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            self.setItem(row_idx, col_idx, item)