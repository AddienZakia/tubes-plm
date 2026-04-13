# Panduan Git

Panduan singkat penggunaan Git dari awal hingga kolaborasi bareng teman.

---

## Daftar Isi

1. [Instalasi & Setup](#1-instalasi--setup)
2. [Konsep Dasar](#2-konsep-dasar)
3. [Memulai Repository](#3-memulai-repository)
4. [Workflow Harian](#4-workflow-harian)

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

---
