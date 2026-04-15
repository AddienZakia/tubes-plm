from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QScrollArea, QFrame, QStackedWidget
from PyQt6.QtCore import Qt

import sys
from src.utils import Fonts
from src.utils import AppLayout
from src.components import HBox, VBox, Typography, Colors, ScatterPlot, LineChart, Button, PaginationTable

data_c = [['No', 'Negara', 'Cluster 0', 'Cluster 1', 'Cluster 2', 'Hasil'], 
          [[1, 'Germany', 0.5189, 0.0756, 0.4055, 'Cluster 0'], [2, 'France', 0.1197, 0.0659, 0.8144, 'Cluster 2'], [3, 'Italy', 0.0181, 0.0774, 0.9044, 'Cluster 2'], [4, 'Spain', 0.0028, 0.0047, 0.9925, 'Cluster 2'], [5, 'Netherlands', 0.9308, 0.0206, 0.0487, 'Cluster 0'], [6, 'Belgium', 0.8823, 0.0252, 0.0925, 'Cluster 0'], [7, 'Sweden', 0.9851, 0.0041, 0.0108, 'Cluster 0'], [8, 'Norway', 0.9964, 0.001, 0.0026, 'Cluster 0'], [9, 'Denmark', 0.9586, 0.0119, 0.0295, 'Cluster 0'], [10, 'Finland', 0.9655, 0.008, 0.0265, 'Cluster 0'], [11, 'Poland', 0.0333, 0.3244, 0.6423, 'Cluster 2'], [12, 'Czech Republic', 0.0066, 0.0095, 0.9839, 'Cluster 2'], [13, 'Hungary', 0.0314, 0.5665, 0.4021, 'Cluster 1'], [14, 'Romania', 0.0003, 0.9976, 0.002, 'Cluster 1'], [15, 'Bulgaria', 0.002, 0.9853, 0.0128, 'Cluster 1'], [16, 'Greece', 0.0248, 0.7199, 0.2553, 'Cluster 1'], [17, 'Portugal', 0.006, 0.0178, 0.9762, 'Cluster 2'], [18, 'Austria', 0.9265, 0.0164, 0.0571, 'Cluster 0'], [19, 'Switzerland', 0.9977, 0.0006, 0.0017, 'Cluster 0'], [20, 'Ireland', 0.9766, 0.0056, 0.0178, 'Cluster 0'], [21, 'Luxembourg', 0.9446, 0.0162, 0.0392, 'Cluster 0'], [22, 'Slovakia', 0.03, 0.2175, 0.7525, 'Cluster 2'], [23, 'Slovenia', 0.0198, 0.0229, 0.9574, 'Cluster 2'], [24, 'Croatia', 0.006, 0.0178, 0.9762, 'Cluster 2'], [25, 'Estonia', 0.6938, 0.0557, 0.2505, 'Cluster 0'], [26, 'Latvia', 0.0005, 0.0011, 0.9984, 'Cluster 2'], [27, 'Lithuania', 0.0066, 0.0095, 0.9839, 'Cluster 2'], [28, 'Cyprus', 0.0329, 0.3025, 0.6646, 'Cluster 2'], [29, 'Malta', 0.0629, 0.047, 0.89, 'Cluster 2'], [30, 'Iceland', 0.9851, 0.0041, 0.0108, 'Cluster 0'], [31, 'Albania', 0.0062, 0.9649, 0.0289, 'Cluster 1'], [32, 'Serbia', 0.0003, 0.9976, 0.002, 'Cluster 1'], [33, 'North Macedonia', 0.0032, 0.9808, 0.016, 'Cluster 1'], [34, 'Montenegro', 0.0032, 0.9808, 0.016, 'Cluster 1'], [35, 'Bosnia', 0.0062, 0.9649, 0.0289, 'Cluster 1']]]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setFixedSize(1000, 750)
        self.app_layout = AppLayout(4)

        # ----
        vbox = VBox(spacing=16)

        # headers
        text_header = HBox(spacing=4)
        num   = Typography("4.", variant='p', weight="bold", color=Colors.primary_active)
        title = Typography("Result - Analisis & Perbandingan", variant='p', weight="bold", color=Colors.neutral_black)
        text_header.addWidget(num)
        text_header.addWidget(title)
        text_header.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # button navigation
        button_hbox   = HBox()
        button_graph  = Button("Clustering Graph", variant="outlined")
        button_table  = Button("Clustering Table", variant="primary")
        button_hbox.addWidget(button_graph)
        button_hbox.addWidget(button_table)

        # statistic
        stats = self.statistic(2, 3, 1)

        # ── stacked widget ───────────────────────────────────────
        stack = QStackedWidget()

        # page 0 → graph
        graph_widget = QWidget()
        graph_layout = VBox()
        graph_widget.setLayout(graph_layout)
        self.graph_clustering(graph_layout)
        stack.addWidget(graph_widget)   # index 0

        # page 1 → table
        table_widget = QWidget()
        table_layout = VBox()
        table_widget.setLayout(table_layout)
        self.table_clustering(table_layout)
        stack.addWidget(table_widget)   # index 1

        # default → graph
        stack.setCurrentIndex(0)

        # ── connect buttons ──────────────────────────────────────
        def show_graph():
            stack.setCurrentIndex(0)

        def show_table():
            stack.setCurrentIndex(1)

        button_graph.clicked.connect(show_graph)
        button_table.clicked.connect(show_table)
    
        vbox.addLayout(text_header)
        vbox.addLayout(button_hbox)
        vbox.addWidget(stats)
        vbox.addWidget(stack)           # ← ini yang sebelumnya hilang

        widget = QWidget()
        widget.setLayout(vbox)

        scroll_area = self.scroll_area(widget)

        self.app_layout.set_content(scroll_area)
        self.setCentralWidget(self.app_layout)

    def statistic(self, cluster, iterasi, m):
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

        v_cluster = VBox()
        title_cluster = Typography("Cluster", variant="c", weight="medium", align=Qt.AlignmentFlag.AlignCenter, color=Colors.neutral_60)
        value_cluster = Typography(str(cluster), variant="p", weight="bold", align=Qt.AlignmentFlag.AlignCenter, color=Colors.primary_active)
        v_cluster.addWidget(title_cluster)
        v_cluster.addWidget(value_cluster)

        v_iter = VBox()
        title_iter = Typography("Iterasi", variant="c", weight="medium", align=Qt.AlignmentFlag.AlignCenter, color=Colors.neutral_60)
        value_iter = Typography(str(iterasi), variant="p", weight="bold", align=Qt.AlignmentFlag.AlignCenter, color=Colors.primary_active)
        v_iter.addWidget(title_iter)
        v_iter.addWidget(value_iter)

        v_m = VBox()
        title_m = Typography("m (fuzz)", variant="c", weight="medium", align=Qt.AlignmentFlag.AlignCenter, color=Colors.neutral_60)
        value_m = Typography(str(m), variant="p", weight="bold", align=Qt.AlignmentFlag.AlignCenter, color=Colors.primary_active)
        v_m.addWidget(title_m)
        v_m.addWidget(value_m)

        hbox.addLayout(v_cluster)
        hbox.addLayout(v_iter)
        hbox.addLayout(v_m)

        frame.setLayout(hbox)
        return frame

    def scroll_area(self, widget):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollArea > QWidget > QWidget {
                background: transparent;
            }
            QScrollBar:vertical {
                background: transparent;
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #9ca3af;
                border-radius: 4px;
                min-height: 40px;
            }
            QScrollBar::handle:vertical:hover {
                background: #6b7280;
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: transparent;
            }
        """)
        scroll_area.setWidget(widget)
        return scroll_area

    def graph_clustering(self, layout):
        chart = ScatterPlot(
            title="FCM Clustering Result",
            x_label="Dimension 1",
            y_label="Dimension 2",
        )
        line_chart = LineChart(
            title="Elbow Method",
            x_label="Jumlah Cluster (C)",
            y_label="Objective Function (J)",
        )

        points      = [[0.1, 0.4], [0.8, 0.2], [0.5, 0.9]]
        labels      = [0, 1, 0]
        annotations = ["Indonesia", "Malaysia", "Singapore"]

        chart.plot(
            points=points,
            labels=labels,
            annotations=annotations,
            n_clusters=2,
        )
        line_chart.plot(series=[
            {
                "label": "J value",
                "x": [2, 3, 4, 5, 6, 7],
                "y": [0.85, 0.61, 0.45, 0.38, 0.33, 0.30],
            }
        ])

        chart.setMinimumHeight(400)
        line_chart.setMinimumHeight(400)

        layout.addWidget(chart)
        layout.addWidget(line_chart)

    def table_clustering(self, layout):
        CENTER = Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter

        tbl = PaginationTable(
            columns=data_c[0],
            rows=data_c[1],
            page_size=10,
            col_widths={
                "No":     50,
                "Negara": 300,
            },
            col_aligns={
                "No":    CENTER,
                "Hasil": CENTER,
            },
        )

        layout.addWidget(tbl)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    Fonts().load_fonts()

    win = MainWindow()
    win.show()
    sys.exit(app.exec())