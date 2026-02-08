import { useMemo, useState } from "react";

const samplePayload = {
  qa_time_manual_minutes: 28,
  records: [
    {
      document_type: "simulasi",
      patient_id: "RT-001",
      site: "breast",
      laterality: "left",
      dose_gy: 50,
      fraction_count: 25
    },
    {
      document_type: "resep",
      patient_id: "RT-001",
      site: "breast",
      laterality: "right",
      dose_gy: 50,
      fraction_count: 25
    },
    {
      document_type: "delivery",
      patient_id: "RT-001",
      site: "breast",
      laterality: "left",
      dose_gy: 48,
      fraction_count: 24
    }
  ]
};

export function App() {
  const [apiUrl, setApiUrl] = useState("http://localhost:8000/audit");
  const [jsonInput, setJsonInput] = useState(JSON.stringify(samplePayload, null, 2));
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const parsedPreview = useMemo(() => {
    try {
      return JSON.parse(jsonInput);
    } catch {
      return null;
    }
  }, [jsonInput]);

  async function runAudit() {
    setError("");
    setLoading(true);

    try {
      const payload = JSON.parse(jsonInput);
      const response = await fetch(apiUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        throw new Error(`API error ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message || "Gagal memproses audit");
      setResult(null);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="container">
      <h1>RT-DocWatch</h1>
      <p className="subtitle">Audit Konsistensi Dokumen Radioterapi Berbasis LLM</p>

      <section className="card">
        <label>URL API Python</label>
        <input value={apiUrl} onChange={(e) => setApiUrl(e.target.value)} />

        <label>Payload (JSON)</label>
        <textarea value={jsonInput} onChange={(e) => setJsonInput(e.target.value)} rows={18} />

        <button type="button" onClick={runAudit} disabled={loading || !parsedPreview}>
          {loading ? "Memproses..." : "Jalankan Audit"}
        </button>
        {!parsedPreview && <p className="error">JSON tidak valid.</p>}
        {error && <p className="error">{error}</p>}
      </section>

      {result && (
        <section className="card">
          <h2>Hasil Outcome</h2>
          <ul>
            <li>Near miss terdeteksi: {result.near_miss_detected}</li>
            <li>Waktu QA manual: {result.qa_time_manual_minutes} menit</li>
            <li>Waktu QA dengan LLM: {result.qa_time_llm_minutes} menit</li>
            <li>Escape rate: {result.escape_rate}</li>
            <li>Penurunan beban kerja tim: {result.team_workload_reduction_percent}%</li>
          </ul>

          <h3>Inconsistency Detail</h3>
          <pre>{JSON.stringify(result.inconsistencies, null, 2)}</pre>
        </section>
      )}
    </main>
  );
}
