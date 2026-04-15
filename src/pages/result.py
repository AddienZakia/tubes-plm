from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QScrollArea, QFrame, QStackedWidget
from PyQt6.QtCore import Qt

import sys
from src.utils import Fonts
from src.utils import AppLayout
from src.components import HBox, VBox, Typography, Colors, ScatterPlot, LineChart, Button, PaginationTable
import numpy as np
from sklearn.manifold import TSNE

data_c = [['No', 'Negara', 'Cluster 0', 'Cluster 1', 'Cluster 2', 'Hasil'], 
          [[1, 'Germany', 0.5189, 0.0756, 0.4055, 'Cluster 0'], [2, 'France', 0.1197, 0.0659, 0.8144, 'Cluster 2'], [3, 'Italy', 0.0181, 0.0774, 0.9044, 'Cluster 2'], [4, 'Spain', 0.0028, 0.0047, 0.9925, 'Cluster 2'], [5, 'Netherlands', 0.9308, 0.0206, 0.0487, 'Cluster 0'], [6, 'Belgium', 0.8823, 0.0252, 0.0925, 'Cluster 0'], [7, 'Sweden', 0.9851, 0.0041, 0.0108, 'Cluster 0'], [8, 'Norway', 0.9964, 0.001, 0.0026, 'Cluster 0'], [9, 'Denmark', 0.9586, 0.0119, 0.0295, 'Cluster 0'], [10, 'Finland', 0.9655, 0.008, 0.0265, 'Cluster 0'], [11, 'Poland', 0.0333, 0.3244, 0.6423, 'Cluster 2'], [12, 'Czech Republic', 0.0066, 0.0095, 0.9839, 'Cluster 2'], [13, 'Hungary', 0.0314, 0.5665, 0.4021, 'Cluster 1'], [14, 'Romania', 0.0003, 0.9976, 0.002, 'Cluster 1'], [15, 'Bulgaria', 0.002, 0.9853, 0.0128, 'Cluster 1'], [16, 'Greece', 0.0248, 0.7199, 0.2553, 'Cluster 1'], [17, 'Portugal', 0.006, 0.0178, 0.9762, 'Cluster 2'], [18, 'Austria', 0.9265, 0.0164, 0.0571, 'Cluster 0'], [19, 'Switzerland', 0.9977, 0.0006, 0.0017, 'Cluster 0'], [20, 'Ireland', 0.9766, 0.0056, 0.0178, 'Cluster 0'], [21, 'Luxembourg', 0.9446, 0.0162, 0.0392, 'Cluster 0'], [22, 'Slovakia', 0.03, 0.2175, 0.7525, 'Cluster 2'], [23, 'Slovenia', 0.0198, 0.0229, 0.9574, 'Cluster 2'], [24, 'Croatia', 0.006, 0.0178, 0.9762, 'Cluster 2'], [25, 'Estonia', 0.6938, 0.0557, 0.2505, 'Cluster 0'], [26, 'Latvia', 0.0005, 0.0011, 0.9984, 'Cluster 2'], [27, 'Lithuania', 0.0066, 0.0095, 0.9839, 'Cluster 2'], [28, 'Cyprus', 0.0329, 0.3025, 0.6646, 'Cluster 2'], [29, 'Malta', 0.0629, 0.047, 0.89, 'Cluster 2'], [30, 'Iceland', 0.9851, 0.0041, 0.0108, 'Cluster 0'], [31, 'Albania', 0.0062, 0.9649, 0.0289, 'Cluster 1'], [32, 'Serbia', 0.0003, 0.9976, 0.002, 'Cluster 1'], [33, 'North Macedonia', 0.0032, 0.9808, 0.016, 'Cluster 1'], [34, 'Montenegro', 0.0032, 0.9808, 0.016, 'Cluster 1'], [35, 'Bosnia', 0.0062, 0.9649, 0.0289, 'Cluster 1']]]

class MainWindow(QWidget):
    def __init__(self, router, parent=None):
        super().__init__(parent)
        self.router = router
        self._columns   = []
        self._rows      = []
        self._stats     = {}
        self._history_J = []
        self._build_ui()
 
    # ── layout awal (kosong / placeholder) ──────────────────────
    def _build_ui(self):
        from PyQt6.QtWidgets import QStackedWidget as _Stack
 
        root = VBox(spacing=16)
        self.setLayout(root)
 
        # Header
        text_header = HBox(spacing=4)
        num   = Typography("4.", variant='p', weight="bold", color=Colors.primary_active)
        title = Typography("Result - Analisis & Perbandingan", variant='p', weight="bold", color=Colors.neutral_black)
        text_header.addWidget(num)
        text_header.addWidget(title)
        text_header.setAlignment(Qt.AlignmentFlag.AlignLeft)
 
        # Tombol toggle Graph / Table
        btn_row = HBox(spacing=8)
        self.btn_graph = Button("Clustering Graph", variant="primary",      size="md")
        self.btn_table = Button("Clustering Table", variant="outline_blue", size="md")
        btn_row.addWidget(self.btn_graph)
        btn_row.addWidget(self.btn_table)
 
        # Statistik
        self.stats_frame = self._build_stats_frame(cluster=0, iterasi=0, m=0)
 
        # Stack graph / table
        self.inner_stack = _Stack()
        self.graph_widget = QWidget()
        self.table_widget = QWidget()
        self._graph_layout = VBox()
        self._table_layout = VBox()
        self.graph_widget.setLayout(self._graph_layout)
        self.table_widget.setLayout(self._table_layout)
        self.inner_stack.addWidget(self.graph_widget)   # 0
        self.inner_stack.addWidget(self.table_widget)   # 1
        self.inner_stack.setCurrentIndex(0)
 
        # Scroll
        scroll = self._make_scroll(self.inner_stack)
        self.inner_stack.setStyleSheet("background: white;")
 
        # Nav
        nav = HBox(spacing=12)
        btn_back = Button("Back", variant="outline_blue", size="md")
        nav.addWidget(btn_back)
        nav.addStretch()
 
        root.addLayout(text_header)
        root.addLayout(btn_row)
        root.addWidget(self.stats_frame)
        root.addWidget(scroll, stretch=1)
        root.addLayout(nav)
 
        # ── koneksi ───────────────────────────────────────────
        self.btn_graph.clicked.connect(lambda: self._show_panel(0))
        self.btn_table.clicked.connect(lambda: self._show_panel(1))
        btn_back.clicked.connect(self.router.show_preview)
 
    def _show_panel(self, idx: int):
        self.inner_stack.setCurrentIndex(idx)
        self.btn_graph.set_variant("primary"      if idx == 0 else "outline_blue")
        self.btn_table.set_variant("outline_blue" if idx == 0 else "primary")
 
    def _build_stats_frame(self, cluster, iterasi, m):
        from PyQt6.QtWidgets import QFrame
        frame = QFrame()
        frame.setObjectName("stats")
        frame.setStyleSheet(f"""
            QFrame#stats {{
                background-color: {Colors.primary_surface};
                padding: 12px 0;
                border-radius: 12px;
                border: 1px solid {Colors.primary_active};
            }}
        """)
 
        hbox = HBox()
        for lbl_text, val in [("Cluster", cluster), ("Iterasi", iterasi), ("m (fuzz)", m)]:
            col = VBox()
            col.addWidget(Typography(lbl_text, variant="c", weight="medium",
                                     align=Qt.AlignmentFlag.AlignCenter, color=Colors.neutral_60))
            col.addWidget(Typography(str(val), variant="p", weight="bold",
                                     align=Qt.AlignmentFlag.AlignCenter, color=Colors.primary_active))
            hbox.addLayout(col)
 
        frame.setLayout(hbox)
        return frame
 
    @staticmethod
    def _make_scroll(widget):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea { background: transparent; border: none; }
            QScrollBar:vertical { background: transparent; width: 8px; }
            QScrollBar::handle:vertical { background: #9ca3af; border-radius: 4px; min-height: 40px; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
        """)
        scroll.setWidget(widget)
        return scroll
 
    # ── dipanggil dari PreviewPage ───────────────────────────────
    def load_result(self, columns, rows, stats: dict):
        self._columns   = columns
        self._rows      = rows
        self._stats     = stats
        self._history_J = stats.get("history_J", [])
 
        # Perbarui statistik
        old = self.stats_frame
        new = self._build_stats_frame(
            cluster = stats.get("cluster", 0),
            iterasi = stats.get("iterasi", 0),
            m       = stats.get("m",       0),
        )
        layout = self.layout()
        idx = layout.indexOf(old)
        layout.removeWidget(old)
        old.deleteLater()
        layout.insertWidget(idx, new)
        self.stats_frame = new
 
        # Bersihkan dan isi ulang graph & table
        self._clear_layout(self._graph_layout)
        self._clear_layout(self._table_layout)
        self._fill_graph()
        self._fill_table()
 
    @staticmethod
    def _clear_layout(layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
 
    def _fill_graph(self):
        

        # Ambil koordinat dari t-SNE, bukan membership
        membership = []
        labels, annotations = [], []
        for row in self._rows:
            membership.append([float(v) for v in row[2:-1]])  # kolom cluster
            label_idx = int(row[-1].replace("Cluster ", ""))
            labels.append(label_idx)
            annotations.append(str(row[1]))

        arr = np.array(membership)
        projected = TSNE(n_components=2, perplexity=4, random_state=42).fit_transform(arr)
        points = projected.tolist()

        chart = ScatterPlot(
            title="FCM Clustering Result",
            x_label="Dimension 1",
            y_label="Dimension 2",
        )
        n_clusters = len(set(labels)) or 1
        chart.plot(points=points, labels=labels, annotations=annotations, n_clusters=n_clusters)

        # Elbow chart tetap sama
        line_chart = LineChart(title="Elbow Method", x_label="Iterasi", y_label="J")
        if self._history_J:
            line_chart.plot(series=[{
                "label": "J value",
                "x": list(range(1, len(self._history_J) + 1)),
                "y": self._history_J,
            }])

        chart.setMinimumHeight(400)
        line_chart.setMinimumHeight(400)
        self._graph_layout.addWidget(chart)
        self._graph_layout.addWidget(line_chart)
 
    def _fill_table(self):
        CENTER = Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter
        tbl = PaginationTable(
            columns=self._columns,
            rows=self._rows,
            page_size=10,
            col_widths={"No": 50, "Negara": 300} if "Negara" in self._columns else {},
            col_aligns={"No": CENTER, "Hasil": CENTER},
        )
        self._table_layout.addWidget(tbl)

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     app.setStyle("Fusion")
#     Fonts().load_fonts()

#     win = MainWindow()
#     win.show()
#     sys.exit(app.exec())