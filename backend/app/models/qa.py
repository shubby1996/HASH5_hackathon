from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class QARequest(BaseModel):
    question: str
    cached_reports: Dict[str, Any]

class QAResponse(BaseModel):
    question: str
    answer: str
    ui_type: str
    data: Dict[str, Any]
    sources: List[str]
    confidence: str

class QAHistoryItem(BaseModel):
    patient_id: str
    question: str
    answer: str
    ui_type: str
    data: Dict[str, Any]
    sources: List[str]
    timestamp: str
