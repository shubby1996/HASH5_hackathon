from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReportGenerateRequest(BaseModel):
    patient_id: str

class ReportStatus(BaseModel):
    job_id: str
    status: str  # pending, processing, completed, failed
    progress: Optional[str] = None
    created_at: str

class Report(BaseModel):
    job_id: str
    patient_id: str
    patient_name: str
    cardiology: str
    radiology: str
    endocrinology: str
    comprehensive: str
    created_at: str
    status: str = "completed"
