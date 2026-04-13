# 📘 Panduan Git untuk Pemula

Panduan singkat penggunaan Git dari awal hingga kolaborasi bareng teman.

---

## Daftar Isi

1. [Instalasi & Setup](#1-instalasi--setup)
2. [Konsep Dasar](#2-konsep-dasar)
3. [Memulai Repository](#3-memulai-repository)
4. [Workflow Harian](#4-workflow-harian)
5. [Menghubungkan ke GitHub](#5-menghubungkan-ke-github)
6. [Kolaborasi](#6-kolaborasi)
7. [Cheat Sheet](#7-cheat-sheet)

---

## 1. Instalasi & Setup

**Download & Install Git**

1. Buka [git-scm.com](https://git-scm.com) → download sesuai OS
2. Install seperti biasa (semua pilihan bisa default)
3. Cek apakah Git sudah terpasang:

```bash
git --version
# Harusnya muncul: git version 2.xx.x
```

**Perkenalkan dirimu ke Git (wajib, cukup sekali)**

```bash
git config --global user.name "Nama Kamu"
git config --global user.email "email@kamu.com"
```

> Gunakan email yang sama dengan akun GitHub kamu.

---

## 2. Konsep Dasar

| Istilah               | Penjelasan                                                           |
| --------------------- | -------------------------------------------------------------------- |
| **Working Directory** | Folder proyekmu — tempat kamu nulis dan edit file                    |
| **Staging Area**      | "Antrian" file yang siap disimpan ke riwayat                         |
| **Repository (Repo)** | Database riwayat semua perubahan di proyekmu                         |
| **Commit**            | Satu titik simpan — seperti foto snapshot proyekmu                   |
| **Branch**            | Jalur pengerjaan terpisah — biar tidak saling ganggu saat kolaborasi |
| **Push**              | Upload perubahan dari komputer ke GitHub                             |
| **Pull**              | Ambil perubahan terbaru dari GitHub ke komputer                      |

**Alur dasar Git:**

```
Edit file  →  git add  →  git commit  →  git push
(lokal)      (staging)    (disimpan)     (ke GitHub)
```

---

## 3. Memulai Repository

### Bikin repo baru dari nol

```bash
# Masuk ke folder proyek
cd nama-folder-proyekmu

# Inisialisasi Git
git init
```

### Ambil repo yang sudah ada dari GitHub (clone)

```bash
git clone https://github.com/AddienZakia/tubes-plm.git

# Masuk ke foldernya
cd nama-repo
```

### Cek kondisi repo

```bash
git status
```

> Jalankan `git status` sesering mungkin untuk tahu kondisi proyekmu.

---

## 4. Workflow Harian

Setiap kali selesai mengerjakan sesuatu, ikuti langkah berikut:

**Langkah 1 — Lihat file apa yang berubah**

```bash
git status
```

**Langkah 2 — Tambahkan file ke staging**

```bash
git add nama-file.txt   # file tertentu
git add .               # semua file yang berubah
```

**Langkah 3 — Simpan dengan pesan**

```bash
git commit -m "Tambah halaman login"
```

> Tulis pesan yang jelas — jelaskan _apa_ yang kamu kerjakan.

**Langkah 4 — Upload ke GitHub**

```bash
git push
```

**Ambil update dari GitHub (lakukan ini setiap mulai kerja)**

```bash
git pull
```

**Lihat riwayat commit**

```bash
git log --oneline
```

---

## 5. Menghubungkan ke GitHub

### Buat repo baru di GitHub

1. Login ke [github.com](https://github.com)
2. Klik tombol **New** (hijau) atau ikon **+**
3. Isi nama repo, pilih Public atau Private
4. **Jangan** centang _Initialize with README_ jika proyekmu sudah ada di komputer
5. Klik **Create repository**

### Hubungkan repo lokal ke GitHub

```bash
# Tambahkan alamat GitHub
git remote add origin https://github.com/username/nama-repo.git

# Upload pertama kali
git push -u origin main
```

> Setelah push pertama, selanjutnya cukup `git push` saja.

---

## 6. Kolaborasi

### Alur kolaborasi yang direkomendasikan

1. Branch `main` selalu bersih — ini milik bersama, jangan langsung edit di sini
2. Tiap orang bikin branch sendiri untuk setiap fitur/tugas
3. Selesai, push branch lalu buat **Pull Request** di GitHub
4. Review bareng, baru di-merge ke `main`

### Perintah branch

```bash
# Lihat semua branch
git branch

# Buat branch baru sekaligus pindah ke sana
git checkout -b nama-branch

# Pindah ke branch yang sudah ada
git checkout main

# Upload branch ke GitHub
git push -u origin nama-branch
```

### Buat Pull Request (PR)

1. Setelah push branch, buka GitHub — ada banner kuning muncul otomatis
2. Klik **Compare & pull request**
3. Tulis judul dan deskripsi singkat apa yang dikerjakan
4. Klik **Create pull request**
5. Minta temanmu review → kalau sudah oke, klik **Merge**

### Menangani conflict

Conflict terjadi kalau dua orang edit bagian yang sama. Git akan menandainya seperti ini:

```
kode milikmu
```

Cara menyelesaikannya:

1. Buka file yang conflict
2. Pilih mana yang mau dipakai (atau gabungkan keduanya)
3. Hapus semua tanda `<<<<<<<`, `=======`, dan `>>>>>>>`
4. Jalankan `git add .` lalu `git commit`

---

## 7. Cheat Sheet

```bash
# Setup
git config --global user.name "Nama"
git config --global user.email "email"

# Repo
git init                    # buat repo baru
git clone <url>             # clone dari GitHub

# Sehari-hari
git status                  # cek kondisi file
git add .                   # tambah semua ke staging
git add <file>              # tambah file tertentu
git commit -m "pesan"       # simpan dengan pesan
git push                    # upload ke GitHub
git pull                    # ambil update dari GitHub
git log --oneline           # lihat riwayat ringkas

# Branch
git branch                  # lihat semua branch
git checkout -b nama        # buat & pindah branch baru
git checkout main           # pindah ke branch main
git push -u origin nama     # upload branch ke GitHub

# Batalkan perubahan
git checkout -- <file>      # buang perubahan (belum di-add)
git reset HEAD <file>       # batalkan git add
```

---

## File `.gitignore`

Buat file bernama `.gitignore` di root proyekmu untuk memberitahu Git file apa yang **tidak** perlu dilacak.

```gitignore
# Contoh isi .gitignore
node_modules/
.env
*.log
.DS_Store
```

> ⚠️ File `.env` biasanya berisi password/API key — **selalu** masukkan ke `.gitignore`!

---

_Panduan ini dibuat untuk membantu kolaborasi antar anggota tim yang baru mengenal Git._
