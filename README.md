# RT-DocWatch

Prototype aplikasi **React + Python** untuk audit konsistensi dokumen radioterapi menggunakan pendekatan LLM rule-assisted.

**Author:** dr. Muhammad Sobri Maulana

## Ringkasan Topik

**Judul:** RT-DocWatch: Audit Konsistensi Dokumen Radioterapi Menggunakan LLM untuk Pencegahan Error Laterality/Dose/Fraction.

- **P (Population):** Seluruh kasus radioterapi di suatu pusat layanan, terutama kasus dengan laterality/site spesifik.
- **I (Intervention):** LLM yang memeriksa konsistensi antar dokumen (simulasi, kontur, resep dosis, rencana, delivery record).
- **C (Comparison):** Quality assurance (QA) manual standar.
- **O (Outcome):** Jumlah error/near-miss terdeteksi, waktu QA, escape rate, dan beban kerja tim.

## Arsitektur

- **Backend Python (FastAPI)**
  - Endpoint `POST /audit` untuk mengevaluasi konsistensi field kritis: `site`, `laterality`, `dose_gy`, `fraction_count`.
  - Menghasilkan metrik outcome simulasi QA.
- **Frontend React (Vite)**
  - Form input JSON dokumen radioterapi.
  - Menampilkan hasil audit dan indikator outcome.

## Menjalankan Backend

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend_requirements.txt
uvicorn backend.main:app --reload
```

API tersedia di `http://localhost:8000`.

## Menjalankan Frontend

```bash
cd frontend
npm install
npm run dev
```

UI tersedia di `http://localhost:5173`.

## Contoh Payload

Gunakan payload bawaan di UI atau kirim langsung:

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
    }
  ]
}
```

## Catatan

Ini adalah prototype edukasi untuk demonstrasi alur audit. Integrasi LLM klinis sebenarnya membutuhkan validasi institusional, kontrol keamanan data, dan governance klinis yang ketat.
