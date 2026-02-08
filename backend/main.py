from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Dict, List, Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI(
    title="RT-DocWatch API",
    description="Audit konsistensi dokumen radioterapi untuk mencegah error laterality/dose/fraction.",
    version="0.1.0",
)


class DocumentRecord(BaseModel):
    document_type: str = Field(..., description="Jenis dokumen: simulasi/kontur/resep/rencana/delivery")
    patient_id: str
    site: Optional[str] = None
    laterality: Optional[str] = None
    dose_gy: Optional[float] = None
    fraction_count: Optional[int] = None


class AuditRequest(BaseModel):
    records: List[DocumentRecord]
    qa_time_manual_minutes: float = Field(..., ge=0)


@dataclass
class Inconsistency:
    field: str
    values: Dict[str, int]
    severity: str


def evaluate_consistency(records: List[DocumentRecord]) -> List[Inconsistency]:
    fields = ["site", "laterality", "dose_gy", "fraction_count"]
    inconsistencies: List[Inconsistency] = []

    for field_name in fields:
        counter = Counter(
            str(getattr(record, field_name))
            for record in records
            if getattr(record, field_name) is not None
        )

        if len(counter) > 1:
            severity = "high" if field_name in {"laterality", "dose_gy", "fraction_count"} else "medium"
            inconsistencies.append(
                Inconsistency(field=field_name, values=dict(counter), severity=severity)
            )

    return inconsistencies


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/audit")
def audit_documents(payload: AuditRequest) -> Dict[str, object]:
    if not payload.records:
        return {
            "error": "records tidak boleh kosong",
            "near_miss_detected": 0,
            "qa_time_llm_minutes": 0,
            "qa_time_manual_minutes": payload.qa_time_manual_minutes,
            "escape_rate": 0,
            "team_workload_reduction_percent": 0,
            "inconsistencies": [],
        }

    inconsistencies = evaluate_consistency(payload.records)
    high_risk_findings = sum(1 for item in inconsistencies if item.severity == "high")

    # Simulasi metrik outcome
    qa_time_llm_minutes = round(max(3.0, payload.qa_time_manual_minutes * 0.35), 2)
    workload_reduction = round(
        ((payload.qa_time_manual_minutes - qa_time_llm_minutes) / payload.qa_time_manual_minutes) * 100,
        2,
    ) if payload.qa_time_manual_minutes else 0

    # Asumsi: jika ada high risk inconsistency, escape rate ditekan
    escape_rate = 0.01 if high_risk_findings > 0 else 0.05

    return {
        "near_miss_detected": len(inconsistencies),
        "qa_time_llm_minutes": qa_time_llm_minutes,
        "qa_time_manual_minutes": payload.qa_time_manual_minutes,
        "escape_rate": escape_rate,
        "team_workload_reduction_percent": workload_reduction,
        "inconsistencies": [
            {"field": item.field, "values": item.values, "severity": item.severity}
            for item in inconsistencies
        ],
    }
