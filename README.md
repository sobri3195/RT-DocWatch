# RT-DocWatch

> **RT-DocWatch** adalah aplikasi prototype untuk audit konsistensi data antar dokumen radioterapi berbasis **FastAPI (backend)** dan **React + Vite (frontend)**.

![License](https://img.shields.io/badge/license-Educational-blue.svg)
![Backend](https://img.shields.io/badge/backend-FastAPI-009688.svg)
![Frontend](https://img.shields.io/badge/frontend-React%2018-61dafb.svg)
![Status](https://img.shields.io/badge/status-Prototype-orange.svg)

---

## 📑 Daftar Isi

- [Gambaran Umum](#-gambaran-umum)
- [Analisis Kodebase (Detail & Mendalam)](#-analisis-kodebase-detail--mendalam)
- [Fitur Utama](#-fitur-utama)
- [Fungsi Sistem](#-fungsi-sistem)
- [Arsitektur Teknis](#-arsitektur-teknis)
- [Struktur Proyek](#-struktur-proyek)
- [Spesifikasi API](#-spesifikasi-api)
- [Instalasi & Menjalankan](#-instalasi--menjalankan)
- [Contoh Payload Uji](#-contoh-payload-uji)
- [Keterbatasan Saat Ini](#-keterbatasan-saat-ini)
- [Roadmap Pengembangan](#-roadmap-pengembangan)
- [Author & Kontak](#-author--kontak)
- [Donasi & Dukungan](#-donasi--dukungan)
- [Disclaimer](#-disclaimer)

---

## 🧭 Gambaran Umum

RT-DocWatch membantu proses QA radioterapi dengan cara membandingkan field kritis lintas dokumen (misalnya simulasi, resep, delivery), lalu menandai ketidaksesuaian (*inconsistency*) yang berpotensi menjadi **near miss**.

Field audit utama:
- `site`
- `laterality`
- `dose_gy`
- `fraction_count`

Hasil audit berisi:
- jumlah temuan (`near_miss_detected`),
- estimasi waktu QA berbantuan sistem,
- indikasi `escape_rate`,
- dan detail mismatch per field.

---

## 🔍 Analisis Kodebase (Detail & Mendalam)

### 1) Backend (`backend/main.py`)

Backend dibangun dengan FastAPI dan memiliki 2 endpoint utama:

1. **`GET /health`**
   - Mengecek status layanan.
   - Respon sederhana: `{ "status": "ok" }`.

2. **`POST /audit`**
   - Menerima payload bertipe `AuditRequest`.
   - Melakukan validasi record + kalkulasi metrik QA.
   - Mengembalikan inconsistency serta ringkasan outcome.

#### Model data dan validasi
- `DocumentRecord` memetakan setiap dokumen radioterapi.
- `AuditRequest` mewajibkan:
  - `records: List[DocumentRecord]`
  - `qa_time_manual_minutes: float` dengan batas `>= 0`

#### Mesin audit inti: `evaluate_consistency(records)`
- Mengiterasi field audit tetap: `site`, `laterality`, `dose_gy`, `fraction_count`.
- Menggunakan `Counter` untuk menghitung variasi nilai per field.
- Bila nilai unik > 1, maka field ditandai **inconsistent**.
- Severity:
  - `high`: `laterality`, `dose_gy`, `fraction_count`
  - `medium`: `site`

#### Simulasi metrik outcome
Saat request valid dan records tidak kosong:
- `near_miss_detected`: jumlah total inconsistency.
- `qa_time_llm_minutes`: `max(3.0, manual * 0.35)` (dibulatkan 2 desimal).
- `team_workload_reduction_percent`: persentase efisiensi waktu.
- `escape_rate`:
  - `0.01` jika ada temuan risiko tinggi,
  - `0.05` jika tidak ada high risk.

#### Penanganan kasus khusus
Jika `records` kosong, API mengembalikan objek fallback dengan nilai metrik nol dan `error` message agar frontend tetap bisa merender respon secara konsisten.

---

### 2) Frontend (`frontend/src/App.jsx`)

Frontend menggunakan React function component tunggal dengan state lokal.

#### Alur kerja UI
1. User mengisi URL API dan JSON payload.
2. Tombol **Jalankan Audit** aktif hanya jika JSON valid.
3. Aplikasi melakukan `fetch` ke endpoint backend.
4. Hasil ditampilkan pada panel **Hasil Outcome**.
5. Pada layar mobile, panel dipisah menggunakan tab bawah: **Audit** dan **Hasil**.

#### Komponen logika penting
- `samplePayload`: payload default untuk demo mismatch.
- `parsedPreview` (`useMemo`): validasi JSON real-time.
- `runAudit()`:
  - parse JSON,
  - POST ke API,
  - handle error response,
  - set hasil ke state.

#### UX yang sudah baik
- Validasi JSON sebelum request.
- Error handling yang jelas.
- Responsif mobile (bottom navigation).
- Hasil detail inconsistency ditampilkan dalam format JSON prettified.

---

### 3) Styling (`frontend/src/styles.css`)

- Skema warna clean (biru-putih) untuk dashboard QA.
- Card layout dengan shadow ringan.
- Komponen input dan tombol konsisten.
- Adaptive design menggunakan media query (`max-width: 768px`).
- Bottom nav fixed pada mobile untuk navigasi cepat antar panel.

---

### 4) Dependency footprint

#### Backend (`backend_requirements.txt`)
- `fastapi`
- `uvicorn`
- `pydantic`
- `python-multipart`

#### Frontend (`frontend/package.json`)
- Runtime: `react`, `react-dom`
- Build/dev: `vite`

Arsitektur dependency saat ini termasuk ringan dan cocok untuk prototyping cepat.

---

## ✨ Fitur Utama

- ✅ Audit konsistensi lintas dokumen radioterapi.
- ✅ Klasifikasi severity temuan (`medium` / `high`).
- ✅ Simulasi metrik QA (waktu, workload reduction, escape rate).
- ✅ Input payload JSON langsung dari antarmuka web.
- ✅ Endpoint backend fleksibel (dapat diganti dari UI).
- ✅ UI responsif untuk desktop dan mobile.

---

## ⚙️ Fungsi Sistem

Secara fungsional, RT-DocWatch dirancang untuk:

1. **Lapisan verifikasi awal** sebelum pemeriksaan manual final.
2. **Deteksi dini potensi near miss** berbasis mismatch data antar dokumen.
3. **Pendukung evaluasi proses QA** melalui metrik simulatif yang mudah dipahami tim.
4. **Sarana demo & edukasi** alur audit dokumen radioterapi berbasis rule engine.

---

## 🏗️ Arsitektur Teknis

```text
User Input JSON (Frontend)
        │
        ▼
POST /audit (FastAPI)
        │
        ▼
Rule-based Consistency Evaluation
        │
        ▼
Outcome Metrics + Inconsistency Detail (JSON)
        │
        ▼
Result Rendering (Frontend)
```

---

## 🗂️ Struktur Proyek

```bash
RT-DocWatch/
├── backend/
│   └── main.py
├── frontend/
│   ├── index.html
│   ├── package.json
│   └── src/
│       ├── App.jsx
│       ├── main.jsx
│       └── styles.css
├── backend_requirements.txt
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

**Request body**
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

**Response body (contoh)**
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

## 🚀 Instalasi & Menjalankan

### 1) Jalankan Backend

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend_requirements.txt
uvicorn backend.main:app --reload
```

Backend berjalan di: **http://localhost:8000**

---

### 2) Jalankan Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend berjalan di: **http://localhost:5173**

---

## 🧪 Contoh Payload Uji

Gunakan payload ini agar sistem menampilkan mismatch pada `laterality`, `dose_gy`, dan `fraction_count`:

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

## ⚠️ Keterbatasan Saat Ini

- Rule engine masih statis (belum adaptive / learning).
- Belum ada autentikasi, audit trail, dan role-based access.
- Belum terintegrasi dengan HIS/RIS/EMR/DICOM RT.
- Metrik outcome masih simulasi (bukan validasi klinis real-world).
- Belum ada persistence database dan histori audit.

---

## 🛣️ Roadmap Pengembangan

- Integrasi data pipeline klinis (FHIR / DICOM-RT aware).
- Rule configurator dinamis berbasis profile institusi.
- Dashboard tren QA dan analytics longitudinal.
- Export laporan (PDF/CSV) dan notifikasi otomatis.
- Integrasi LLM guardrailed + human-in-the-loop review.

---

## 👤 Author & Kontak

**Author:** Lettu Kes dr. Muhammad Sobri Maulana, S.Kom, CEH, OSCP, OSCE  
**GitHub:** https://github.com/sobri3195  
**Email:** muhammadsobrimaulana31@gmail.com  
**Website:** https://muhammadsobrimaulana.netlify.app  

### 🌐 Social & Community

- YouTube: https://www.youtube.com/@muhammadsobrimaulana6013
- Telegram: https://t.me/winlin_exploit
- TikTok: https://www.tiktok.com/@dr.sobri
- Grup WhatsApp: https://chat.whatsapp.com/B8nwRZOBMo64GjTwdXV8Bl
- Landing page: https://muhammad-sobri-maulana-kvr6a.sevalla.page/
- Toko Online Sobri: https://pegasus-shop.netlify.app
- Gumroad: https://maulanasobri.gumroad.com/

---

## 💝 Donasi & Dukungan

Jika proyek ini bermanfaat, dukungan Anda sangat berarti untuk pengembangan lanjutan:

- Lynk: https://lynk.id/muhsobrimaulana
- Trakteer: https://trakteer.id/g9mkave5gauns962u07t
- KaryaKarsa: https://karyakarsa.com/muhammadsobrimaulana
- Nyawer: https://nyawer.co/MuhammadSobriMaulana

---

## 📌 Disclaimer

Aplikasi ini adalah **prototype edukasi dan riset**. Bukan perangkat medis tersertifikasi, bukan pengganti clinical judgment, dan tidak boleh dijadikan satu-satunya dasar keputusan terapi pasien.

Semua implementasi untuk lingkungan klinis wajib melalui:
- validasi medis formal,
- tata kelola keamanan data,
- serta kepatuhan regulasi yang berlaku.
