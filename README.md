# RT-DocWatch

> Prototype **audit konsistensi dokumen radioterapi** berbasis **FastAPI + React (Vite)** untuk membantu deteksi dini ketidaksesuaian data kritis (misalnya laterality, dosis, dan jumlah fraksi).

![License](https://img.shields.io/badge/license-Educational-blue.svg)
![Backend](https://img.shields.io/badge/backend-FastAPI-009688.svg)
![Frontend](https://img.shields.io/badge/frontend-React%2018-61dafb.svg)
![Status](https://img.shields.io/badge/status-Prototype-orange.svg)

---

## 📌 Daftar Isi

- [Tentang Proyek](#-tentang-proyek)
- [Fitur Utama](#-fitur-utama)
- [Fungsi Sistem (Apa yang Dikerjakan Aplikasi)](#-fungsi-sistem-apa-yang-dikerjakan-aplikasi)
- [Arsitektur & Alur Kerja](#-arsitektur--alur-kerja)
- [Struktur Proyek](#-struktur-proyek)
- [Spesifikasi API](#-spesifikasi-api)
- [Instalasi & Menjalankan](#-instalasi--menjalankan)
- [Contoh Payload & Output](#-contoh-payload--output)
- [Rencana Pengembangan](#-rencana-pengembangan)
- [Kontributor & Kontak](#-kontributor--kontak)
- [Dukungan / Donasi](#-dukungan--donasi)
- [Disclaimer Klinis](#-disclaimer-klinis)

---

## 🧭 Tentang Proyek

**RT-DocWatch** adalah prototype untuk memvalidasi konsistensi data antar dokumen radioterapi.

Sistem membaca kumpulan record dokumen (contoh: simulasi, resep, delivery), lalu membandingkan field penting:

- `site`
- `laterality`
- `dose_gy`
- `fraction_count`

Jika terdapat perbedaan nilai antar dokumen, sistem menandainya sebagai **inconsistency** dengan tingkat risiko (`medium` atau `high`) dan menampilkan metrik outcome QA simulatif.

---

## ✨ Fitur Utama

1. **Audit Konsistensi Antar Dokumen**
   - Mendeteksi mismatch nilai antar record pasien untuk field klinis kunci.

2. **Klasifikasi Severity Temuan**
   - `high`: laterality, dose_gy, fraction_count.
   - `medium`: site.

3. **Perhitungan Outcome QA Simulatif**
   - `near_miss_detected`
   - `qa_time_llm_minutes`
   - `qa_time_manual_minutes`
   - `escape_rate`
   - `team_workload_reduction_percent`

4. **Frontend Interaktif Berbasis React**
   - Input URL API backend.
   - Editor payload JSON langsung di browser.
   - Tampilan hasil audit dalam format ringkas + detail inconsistency.

5. **Mobile-Friendly UI**
   - Navigasi bawah (tab Audit / Hasil) untuk layar kecil.

---

## 🧩 Fungsi Sistem (Apa yang Dikerjakan Aplikasi)

Secara fungsional, RT-DocWatch membantu tim QA dengan cara:

- Menjadi **lapisan verifikasi cepat** sebelum review manual penuh.
- Menyorot **potensi near-miss** lebih awal berdasarkan mismatch antar dokumen.
- Memberikan indikator efisiensi waktu QA secara simulatif untuk keperluan evaluasi proses.

> Catatan: Pada versi ini, kalkulasi metrik merupakan simulasi rule-based dan belum terhubung ke model klinis produksi atau sistem hospital information system.

---

## 🏗️ Arsitektur & Alur Kerja

### Backend (FastAPI)

- Endpoint health check: `GET /health`
- Endpoint audit: `POST /audit`
- Core logic:
  1. Validasi payload.
  2. Evaluasi konsistensi per field.
  3. Tentukan severity.
  4. Hitung metrik outcome simulasi.
  5. Kembalikan hasil JSON.

### Frontend (React + Vite)

- Menyediakan payload contoh default.
- Kirim request `POST` ke API backend.
- Tampilkan hasil audit dan detail inconsistency.

### Alur Singkat

`User Input JSON -> Frontend -> POST /audit -> Backend Evaluation -> JSON Result -> Frontend Result Panel`

---

## 🗂️ Struktur Proyek

```bash
RT-DocWatch/
├── backend/
│   └── main.py                # API FastAPI + core audit logic
├── frontend/
│   ├── src/
│   │   ├── App.jsx            # UI audit + result
│   │   ├── main.jsx           # React entry point
│   │   └── styles.css         # Styling + mobile navigation
│   ├── package.json
│   └── index.html
├── backend_requirements.txt   # Dependency Python backend
└── README.md
```

---

## 🔌 Spesifikasi API

### `GET /health`

**Response**

```json
{
  "status": "ok"
}
```

### `POST /audit`

**Request Body**

```json
{
  "qa_time_manual_minutes": 28,
  "records": [
    {
      "document_type": "simulasi",
      "patient_id": "RT-001",
      "site": "breast",
      "laterality": "left",
      "dose_gy": 50,
      "fraction_count": 25
    }
  ]
}
```

**Response Body (contoh)**

```json
{
  "near_miss_detected": 3,
  "qa_time_llm_minutes": 9.8,
  "qa_time_manual_minutes": 28,
  "escape_rate": 0.01,
  "team_workload_reduction_percent": 65,
  "inconsistencies": [
    {
      "field": "laterality",
      "values": {
        "left": 2,
        "right": 1
      },
      "severity": "high"
    }
  ]
}
```

---

## ⚙️ Instalasi & Menjalankan

## 1) Backend

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend_requirements.txt
uvicorn backend.main:app --reload
```

Backend aktif di: `http://localhost:8000`

## 2) Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend aktif di: `http://localhost:5173`

---

## 🧪 Contoh Payload & Output

Gunakan payload berikut untuk memunculkan ketidaksesuaian laterality/dose/fraction:

```json
{
  "qa_time_manual_minutes": 28,
  "records": [
    {
      "document_type": "simulasi",
      "patient_id": "RT-001",
      "site": "breast",
      "laterality": "left",
      "dose_gy": 50,
      "fraction_count": 25
    },
    {
      "document_type": "resep",
      "patient_id": "RT-001",
      "site": "breast",
      "laterality": "right",
      "dose_gy": 50,
      "fraction_count": 25
    },
    {
      "document_type": "delivery",
      "patient_id": "RT-001",
      "site": "breast",
      "laterality": "left",
      "dose_gy": 48,
      "fraction_count": 24
    }
  ]
}
```

---

## 🚀 Rencana Pengembangan

- Integrasi autentikasi & role-based access.
- Audit trail dan logging terstruktur.
- Integrasi database untuk histori audit.
- Export laporan PDF/CSV.
- Integrasi NLP/LLM yang tervalidasi klinis dengan governance keamanan data.
- Rule engine yang dapat dikustomisasi per institusi.

---

## 👤 Kontributor & Kontak

**Author:** Lettu Kes dr. Muhammad Sobri Maulana, S.Kom, CEH, OSCP, OSCE

- GitHub: [github.com/sobri3195](https://github.com/sobri3195)
- Email: [muhammadsobrimaulana31@gmail.com](mailto:muhammadsobrimaulana31@gmail.com)
- Website: [muhammadsobrimaulana.netlify.app](https://muhammadsobrimaulana.netlify.app)
- Website 2: [muhammad-sobri-maulana-kvr6a.sevalla.page](https://muhammad-sobri-maulana-kvr6a.sevalla.page/)
- YouTube: [@muhammadsobrimaulana6013](https://www.youtube.com/@muhammadsobrimaulana6013)
- Telegram: [winlin_exploit](https://t.me/winlin_exploit)
- TikTok: [@dr.sobri](https://www.tiktok.com/@dr.sobri)
- WhatsApp Group: [Gabung Grup](https://chat.whatsapp.com/B8nwRZOBMo64GjTwdXV8Bl)
- Gumroad: [maulanasobri.gumroad.com](https://maulanasobri.gumroad.com/)
- Toko Online Sobri: [pegasus-shop.netlify.app](https://pegasus-shop.netlify.app)

---

## 💖 Dukungan / Donasi

Jika proyek ini bermanfaat, dukungan Anda akan sangat membantu pengembangan lanjutan:

- Lynk: [lynk.id/muhsobrimaulana](https://lynk.id/muhsobrimaulana)
- Trakteer: [trakteer.id/g9mkave5gauns962u07t](https://trakteer.id/g9mkave5gauns962u07t)
- KaryaKarsa: [karyakarsa.com/muhammadsobrimaulana](https://karyakarsa.com/muhammadsobrimaulana)
- Nyawer: [nyawer.co/MuhammadSobriMaulana](https://nyawer.co/MuhammadSobriMaulana)

---

## ⚠️ Disclaimer Klinis

RT-DocWatch adalah **prototype edukasi/research** dan **bukan** medical device tervalidasi.

- Tidak menggantikan clinical judgment.
- Tidak menggantikan QA formal institusi.
- Wajib melalui validasi, uji klinis internal, dan governance sebelum penggunaan operasional klinis.

---

## 📄 Lisensi

Saat ini belum ada lisensi formal yang ditetapkan. Disarankan menambahkan lisensi open-source sesuai kebutuhan (mis. MIT/Apache-2.0) sebelum distribusi luas.
