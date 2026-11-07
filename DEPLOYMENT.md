# 🌐 Panduan Deploy MarkItDown Studio (Tanpa Database)

Karena aplikasi ini **stateless** (tidak memerlukan database), Anda bisa mendeploy-nya dengan sangat mudah, cepat, dan bahkan gratis di berbagai platform cloud.

---

## Opsi 1: Deploy di Vercel (Serverless Python)

Aplikasi ini sudah dilengkapi dengan konfigurasi `vercel.json` dan handler `api/index.py` untuk Vercel:

1. Push kodingan ini ke akun GitHub Anda.
2. Buka [vercel.com](https://vercel.com) dan login dengan akun GitHub Anda.
3. Klik **Add New...** $\rightarrow$ **Project**.
4. Pilih repository `MARKITDOWN-GENERATOR` Anda, lalu klik **Deploy**.
5. Vercel akan otomatis mendeteksi konfigurasi `@vercel/python` dan mendeploy aplikasi Anda secara serverless!

> [!NOTE]
> **Catatan Penting Vercel**: 
> Vercel menggunakan arsitektur *Serverless Function*. Akun Vercel gratis memiliki batas durasi proses (*timeout*) maksimal 10-15 detik per request dan batas ukuran paket (*bundle size* 250MB). Untuk file dokumen berukuran standar (Word, Excel, PDF beberapa halaman), Vercel berfungsi dengan baik. Namun jika Anda sering mengonversi file PDF ratusan halaman atau file video/audio panjang, disarankan menggunakan **Render** atau **Hugging Face Spaces** yang tidak memiliki batasan timeout ketat.

---

## Opsi 2: Deploy di Render (Rekomendasi Terbaik untuk Dokumen Berat)

1. Push kodingan ini ke repository GitHub pribadi Anda.
2. Buka [render.com](https://render.com) dan buat akun gratis.
3. Klik **New +** $\rightarrow$ Pilih **Web Service**.
4. Hubungkan repository GitHub Anda.
5. Konfigurasi form Render:
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Plan**: `Free`
6. Klik **Create Web Service**. Dalam 1-2 menit, aplikasi Anda akan aktif dengan link publik HTTPS (misal: `https://markitdown-studio.onrender.com`).

---

## Opsi 2: Deploy di Hugging Face Spaces (Gratis 100%)

1. Buka [huggingface.co/spaces](https://huggingface.co/spaces) dan buat Space baru.
2. Beri nama Space (misal: `markitdown-studio`).
3. Pilih SDK: **Docker** $\rightarrow$ **Blank**.
4. Clone repo Hugging Face ke komputer Anda atau push langsung file project ini (`Dockerfile`, `requirements.txt`, `app.py`, folder `static/`).
5. Hugging Face akan otomatis mem-build Dockerfile dan aplikasi langsung online 24/7 secara gratis!

---

## Opsi 3: Deploy di Railway

1. Buka [railway.app](https://railway.app).
2. Klik **New Project** $\rightarrow$ **Deploy from GitHub repo**.
3. Pilih repository project ini.
4. Railway akan mendeteksi `Dockerfile` atau `requirements.txt` secara otomatis.
5. Selesai! Railway akan memberikan domain publik yang bisa langsung diakses.

---

## Opsi 4: Deploy Menggunakan Docker (VPS / Server Sendiri)

Jika Anda memiliki server Linux/VPS (seperti DigitalOcean, Linode, AWS, GCP, dll):

```bash
# 1. Build image Docker
docker build -t markitdown-studio .

# 2. Jalankan container di port 80 (atau port 8000)
docker run -d -p 80:8000 --name markitdown-app --restart always markitdown-studio
```
Aplikasi kini berjalan di `http://IP_SERVER_ANDA`.

---

## 🔒 Catatan Keamanan & Privasi
- Aplikasi ini otomatis menghapus file yang diunggah segera setelah konversi selesai (`temp_path.unlink()`).
- Tidak ada data dokumen yang tersimpan di disk server secara permanen, sehingga aman untuk memproses dokumen pribadi/sensitif.
