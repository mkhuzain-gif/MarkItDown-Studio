# 🚀 MarkItDown Generator Studio

A modern, fast, and feature-rich document-to-Markdown converter powered by **Microsoft MarkItDown 0.1.9** and **FastAPI**.

---

## 🌟 Fitur Utama

- **Web UI Interaktif**: Tampilan modern & responsif (Dark Mode) untuk konversi dokumen langsung di browser.
- **Drag & Drop / Multi-file Batch**: Unggah satu atau puluhan file sekaligus.
- **Live Markdown Preview**: Tampilan hasil render Markdown berdampingan (*split view*), lengkap dengan editor teks.
- **Single-Click Actions**:
  - 📋 Salin teks Markdown ke clipboard dengan satu klik.
  - 💾 Unduh file `.md`.
  - 📦 Unduh semua file yang telah dikonversi dalam format **ZIP**.
- **Konversi URL & YouTube**: Ubah artikel web atau transkrip video YouTube menjadi Markdown rapi.
- **CLI & Scripting Ready**: Dukungan konversi via terminal atau modul Python tersendiri.

---

## 📂 Format File yang Didukung

| Kategori | Format |
|---|---|
| **Dokumen** | PDF (`.pdf`), Microsoft Word (`.docx`), PowerPoint (`.pptx`) |
| **Data & Spreadsheet** | Excel (`.xlsx`, `.xls`), CSV (`.csv`), JSON (`.json`), XML (`.xml`) |
| **Web & Media** | HTML (`.html`), Audio (`.mp3`, `.wav`), Gambar EXIF (`.jpg`, `.png`), URL Web & YouTube |

---

## ⚡ Cara Menjalankan Web UI

### Cara 1: Double-Click (Paling Mudah)
Cukup klik dua kali file **`run_web.bat`**. Browser Anda akan otomatis terbuka di `http://127.0.0.1:8000`.

### Cara 2: Lewat PowerShell / Terminal
```powershell
.\.venv\Scripts\python.exe app.py
```
Lalu buka browser di: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 💻 Cara Menggunakan via Terminal / Script (CLI)

Gunakan script `generator.py` untuk konversi cepat langsung dari terminal:

```powershell
# 1. Konversi 1 file
.\.venv\Scripts\python.exe generator.py "dokumen.pdf"

# 2. Konversi dengan menentukan nama file output
.\.venv\Scripts\python.exe generator.py "dokumen.pdf" -o "hasil.md"

# 3. Konversi seluruh folder dokumen sekaligus (Batch Mode)
.\.venv\Scripts\python.exe generator.py -b ./folder_input -d ./folder_output
```

---

## 🐍 Penggunaan via Python API

```python
from generator import MarkdownGenerator

gen = MarkdownGenerator()

# Konversi file tunggal
md_text = gen.convert_file("laporan.docx", "laporan.md")

# Konversi batch dalam folder
gen.convert_directory("./input_docs", "./output_md")
```

