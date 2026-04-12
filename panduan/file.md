# PyQt6 — Panduan Pemakaian Components & Fungsi Dasar

---

## 1. Typography

```python
from src.components import Typography, Colors
from PyQt6.QtCore import Qt

# basic
Typography("Hello World")

# variants: h1 h2 h3 h4 h5 h6 t p b c
Typography("Judul Besar",   variant="h1")
Typography("Sub judul",     variant="h4")
Typography("Body text",     variant="p")
Typography("Caption kecil", variant="c")

# weight: regular | medium | bold
Typography("Tebal",  variant="p", weight="bold")
Typography("Medium", variant="p", weight="medium")

# warna — pakai Colors atau hex langsung
Typography("Biru",  variant="p", color=Colors.primary_main)
Typography("Merah", variant="p", color="#DC2626")
Typography("Abu",   variant="p", color=Colors.neutral_60)

# alignment
Typography("Tengah", variant="p", align=Qt.AlignmentFlag.AlignCenter)
Typography("Kanan",  variant="p", align=Qt.AlignmentFlag.AlignRight)

# word wrap — teks panjang otomatis turun baris
Typography("Teks yang sangat panjang...", variant="p", word_wrap=True)

# update teks setelah dibuat
label = Typography("awal", variant="p")
label.setText("teks baru")

# update warna setelah dibuat
label.set_color(Colors.error_main)
```

---

## 2. Button

```python
from src.components import Button

# variants: primary | success | warning | error | info | alternative | outlined
Button("Simpan",   variant="primary")
Button("Berhasil", variant="success")
Button("Hapus",    variant="error")
Button("Batal",    variant="outlined")

# size: sm | md | lg
Button("Kecil",  size="sm")
Button("Sedang", size="md")
Button("Besar",  size="lg")

# disabled
btn = Button("Submit", variant="primary")
btn.setDisabled(True)   # disable
btn.setDisabled(False)  # enable kembali
btn.isEnabled()         # -> bool

# handle klik
btn = Button("Klik Aku", variant="primary")
btn.clicked.connect(lambda: print("diklik!"))

# atau pakai function
def handle_submit():
    print("submit!")

btn.clicked.connect(handle_submit)
```

---

## 3. VBox & HBox

```python
from src.components import VBox, HBox, Button, Typography
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget

# VBox — susun widget secara vertikal (atas ke bawah)
layout = VBox()
layout.addWidget(Typography("Atas", variant="p"))
layout.addWidget(Typography("Bawah", variant="p"))

# HBox — susun widget secara horizontal (kiri ke kanan)
layout = HBox()
layout.addWidget(Button("Batal",  variant="outlined"))
layout.addWidget(Button("Simpan", variant="primary"))

# spacing — jarak antar widget (pixel)
VBox(spacing=4)    # rapat
VBox(spacing=16)   # longgar

# margin — (left, top, right, bottom)
VBox(margin=(16, 16, 16, 16))   # semua sisi 16px
VBox(margin=(24, 0, 24, 0))     # kiri kanan 24px, atas bawah 0

# align — rata widget di dalam layout
VBox(align=Qt.AlignmentFlag.AlignCenter)  # tengah
HBox(align=Qt.AlignmentFlag.AlignRight)   # kanan
HBox(align=Qt.AlignmentFlag.AlignVCenter) # tengah vertikal

# addStretch — dorong widget ke sisi berlawanan
layout = HBox()
layout.addWidget(Typography("Kiri", variant="p"))
layout.addStretch()                             # ← ini mendorong
layout.addWidget(Button("Kanan", variant="outlined"))

# nested layout
outer = VBox(spacing=16, margin=(24, 24, 24, 24))

row = HBox(spacing=8)
row.addWidget(Button("A", variant="primary"))
row.addWidget(Button("B", variant="outlined"))

outer.addWidget(Typography("Header", variant="h5"))
outer.addLayout(row)   # addLayout untuk layout, addWidget untuk widget

# attach layout ke widget
container = QWidget()
container.setLayout(VBox(spacing=12))
```

---

## 4. Image

```python
from src.components import Image

# basic
Image(src="assets/images/logo.png")

# dengan ukuran fix
Image(src="assets/images/banner.jpg", width=400, height=200)

# object_fit: contain | cover | fill
Image(src="assets/images/foto.jpg", width=80, height=80, object_fit="cover")    # crop tengah
Image(src="assets/images/foto.jpg", width=80, height=80, object_fit="contain")  # scale in-bounds
Image(src="assets/images/foto.jpg", width=80, height=80, object_fit="fill")     # stretch

# rounded (cocok buat avatar)
Image(src="assets/images/avatar.png", width=80, height=80, rounded=40, object_fit="cover")

# fallback text kalau gambar ga ada
Image(src="path/salah.png", alt="Gambar tidak ditemukan")

# set dinamis setelah dibuat
img = Image(width=200, height=200)
img.set_src("assets/images/foto.jpg")
img.set_size(300, 150)
img.set_object_fit("cover")
```

---

## 5. UploadFile

```python
from src.components import UploadFile

# basic — default accept CSV
upload = UploadFile()

# custom accept
upload = UploadFile(accept="CSV Files (*.csv)")
upload = UploadFile(accept="Images (*.png *.jpg *.jpeg)")
upload = UploadFile(accept="All Files (*)")

# custom tinggi
upload = UploadFile(height=160)

# ambil path file yang dipilih
path = upload.get_path()   # -> str | None

# reset ke kondisi awal
upload.reset()

# signal — triggered setiap file dipilih (drag drop atau click)
upload.file_selected.connect(lambda path: print(f"File: {path}"))

# contoh penggunaan nyata
def on_file_selected(path: str):
    print(f"Loading: {path}")
    # proses CSV di sini...

upload = UploadFile(accept="CSV Files (*.csv)")
upload.file_selected.connect(on_file_selected)
```

---

## 6. Table

```python
from src.components import Table

# basic
columns = ["Negara", "2018", "2021", "Cluster"]
rows    = [
    ["Indonesia", 45, 67, 0],
    ["Malaysia",  55, 72, 1],
    ["Singapore", 88, 95, 2],
]
table = Table(columns=columns, rows=rows)

# tanpa data awal, isi nanti
table = Table(columns=columns)
table.set_rows(rows)         # set semua sekaligus (replace)
table.append_row(["Thailand", 60, 80, 1])  # tambah 1 baris
table.clear_rows()           # kosongkan

# stretch kolom terakhir — default True
Table(columns=columns, stretch_last=True)
```

---

## 7. PaginationTable

```python
from src.components import PaginationTable

rows = [[f"Negara {i}", i * 10, i * 5, i % 3] for i in range(1, 36)]

# basic
tbl = PaginationTable(
    columns=["Negara", "Val A", "Val B", "Cluster"],
    rows=rows,
    page_size=10,   # default 10 baris per halaman
)

# update data (reset ke halaman 1)
tbl.set_rows(new_rows)

# ganti jumlah baris per halaman
tbl.set_page_size(15)

# akses table di dalamnya kalau perlu
tbl.table.append_row(["Baru", 0, 0, 0])
```

---

## 8. ScatterPlot

```python
from src.components import ScatterPlot

chart = ScatterPlot(
    title="FCM Clustering Result",
    x_label="Dimension 1",
    y_label="Dimension 2",
)

# plot data
# points    — list of [x, y]
# labels    — cluster index tiap point (0, 1, 2, ...)
# annotations — nama tiap point (opsional)
points      = [[0.1, 0.4], [0.8, 0.2], [0.5, 0.9]]
labels      = [0, 1, 0]
annotations = ["Indonesia", "Malaysia", "Singapore"]

chart.plot(
    points=points,
    labels=labels,
    annotations=annotations,
    n_clusters=2,
)

# clear / reset
chart.clear()
```

---

## 9. LineChart

```python
from src.components import LineChart

chart = LineChart(
    title="Elbow Method",
    x_label="Jumlah Cluster (C)",
    y_label="Objective Function (J)",
)

# plot — bisa multiple series sekaligus
chart.plot(series=[
    {
        "label": "J value",
        "x": [2, 3, 4, 5, 6, 7],
        "y": [0.85, 0.61, 0.45, 0.38, 0.33, 0.30],
    }
])

# multiple series
chart.plot(series=[
    {"label": "m=2", "x": [2,3,4,5], "y": [0.85, 0.61, 0.45, 0.38]},
    {"label": "m=3", "x": [2,3,4,5], "y": [0.90, 0.70, 0.55, 0.48]},
])

# tanpa markers bulat
chart.plot(series=[...], markers=False)

# clear
chart.clear()
```

---

## 10. Fungsi-fungsi Umum PyQt6

### Ukuran & Posisi

```python
widget.setFixedSize(400, 300)       # lebar & tinggi fix, tidak bisa di-resize
widget.setFixedWidth(200)           # hanya lebar yang fix
widget.setFixedHeight(100)          # hanya tinggi yang fix
widget.setMinimumSize(300, 200)     # ukuran minimum
widget.setMaximumSize(800, 600)     # ukuran maksimum
widget.resize(500, 400)             # resize (bisa berubah)
widget.setGeometry(x, y, w, h)     # posisi x,y + ukuran w,h sekaligus
widget.move(100, 50)                # pindah ke posisi x=100, y=50
widget.width()                      # -> int, lebar sekarang
widget.height()                     # -> int, tinggi sekarang
```

### Visibility & State

```python
widget.show()               # tampilkan widget
widget.hide()               # sembunyikan (tetap ada di memory)
widget.setVisible(True)     # sama kayak show/hide tapi pakai bool
widget.isVisible()          # -> bool
widget.setDisabled(True)    # disable (greyed out, tidak bisa diklik)
widget.setEnabled(True)     # enable kembali
widget.isEnabled()          # -> bool
```

### Styling

```python
# inline style — mirip CSS
widget.setStyleSheet("""
    QWidget {
        background-color: #F8FAFC;
        border:           1px solid #E2E8F0;
        border-radius:    8px;
        padding:          12px;
    }
""")

# tooltip — muncul saat hover
widget.setToolTip("Klik untuk upload file")
```

### SizePolicy — ngatur gimana widget nge-stretch

```python
from PyQt6.QtWidgets import QSizePolicy

# Expanding — mau sebesar mungkin (ngisi sisa ruang)
widget.setSizePolicy(
    QSizePolicy.Policy.Expanding,
    QSizePolicy.Policy.Expanding,
)

# Fixed — ukurannya tetap
widget.setSizePolicy(
    QSizePolicy.Policy.Fixed,
    QSizePolicy.Policy.Fixed,
)

# Preferred — ikut sizeHint tapi bisa dikecilkan
widget.setSizePolicy(
    QSizePolicy.Policy.Preferred,
    QSizePolicy.Policy.Preferred,
)
```

### QMainWindow — window utama

```python
from PyQt6.QtWidgets import QMainWindow, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Nama App")
        self.setMinimumSize(1024, 680)
        self.resize(1280, 720)

        # set central widget (konten utama)
        central = QWidget()
        self.setCentralWidget(central)

        # set layout ke central widget
        layout = VBox(spacing=0, margin=(24, 24, 24, 24))
        central.setLayout(layout)
```

### QWidget — container / panel

```python
from PyQt6.QtWidgets import QWidget

# bikin panel / card
card = QWidget()
card.setFixedSize(300, 200)
card.setStyleSheet("""
    QWidget {
        background: white;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
    }
""")

layout = VBox(spacing=12, margin=(16, 16, 16, 16))
card.setLayout(layout)
layout.addWidget(Typography("Card Title", variant="h6"))
layout.addWidget(Typography("Isi card", variant="p"))
```

### Signal & Slot — event handling

```python
# signal built-in
btn.clicked.connect(handler)            # button diklik
checkbox.stateChanged.connect(handler)  # checkbox berubah
input.textChanged.connect(handler)      # teks input berubah
upload.file_selected.connect(handler)   # file dipilih (custom signal)

# disconnect
btn.clicked.disconnect(handler)

# lambda untuk one-liner
btn.clicked.connect(lambda: label.setText("Diklik!"))

# contoh lengkap
def on_submit():
    path = upload.get_path()
    if path is None:
        print("Belum pilih file!")
        return
    print(f"Processing: {path}")

btn_submit = Button("Run Clustering", variant="primary")
btn_submit.clicked.connect(on_submit)
```

---

## Contoh Gabungan — Card dengan Form

```python
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import Qt
from src.components import VBox, HBox, Typography, Button, UploadFile, Colors
import sys

class ClusteringCard(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(480)
        self.setStyleSheet("""
            ClusteringCard {
                background:    white;
                border-radius: 12px;
                border:        1px solid #E2E8F0;
            }
        """)

        layout = VBox(spacing=16, margin=(24, 24, 24, 24))
        self.setLayout(layout)

        # header
        layout.addWidget(Typography("FCM Clustering", variant="h5", weight="bold"))
        layout.addWidget(Typography("Upload file CSV dan jalankan clustering", variant="c", color=Colors.neutral_60))

        # upload
        self.upload = UploadFile(accept="CSV Files (*.csv)")
        self.upload.file_selected.connect(self._on_file)
        layout.addWidget(self.upload)

        # footer buttons
        footer = HBox(spacing=8)
        footer.addStretch()
        footer.addWidget(Button("Reset",  variant="outlined", size="sm"))
        self.btn_run = Button("Run", variant="primary", size="sm")
        self.btn_run.setDisabled(True)
        self.btn_run.clicked.connect(self._on_run)
        footer.addWidget(self.btn_run)
        layout.addLayout(footer)

    def _on_file(self, path: str):
        self.btn_run.setDisabled(False)

    def _on_run(self):
        path = self.upload.get_path()
        print(f"Running FCM with: {path}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    card = ClusteringCard()
    card.show()
    sys.exit(app.exec())
```
