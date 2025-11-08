from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime

from app.models.qa import QARequest, QAResponse, QAHistoryItem
from app.services.qa_service import qa_service
from app.services.storage_service import storage_service

router = APIRouter()

# In-memory Q&A history (will be replaced with DynamoDB later)
qa_history = {}

@router.post("/qa/ask", response_model=QAResponse)
async def ask_question(request: QARequest):
    """Ask question about cached reports"""
    try:
        response = qa_service.ask_question(request.question, request.cached_reports)
        
        # Add question to response
        response['question'] = request.question
        
        # Store in history if patient_id is in cached_reports
        patient_id = request.cached_reports.get('patient_id')
        if patient_id:
            if patient_id not in qa_history:
                qa_history[patient_id] = []
            
            qa_history[patient_id].append({
                'patient_id': patient_id,
                'question': request.question,
                'answer': response['answer'],
                'ui_type': response['ui_type'],
                'data': response['data'],
                'sources': response['sources'],
                'timestamp': datetime.utcnow().isoformat()
            })
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/qa/history/{patient_id}", response_model=List[QAHistoryItem])
async def get_qa_history(patient_id: str):
    """Get Q&A history for a patient"""
    history = qa_history.get(patient_id, [])
    return history

@router.delete("/qa/history/{patient_id}")
async def clear_qa_history(patient_id: str):
    """Clear Q&A history for a patient"""
    if patient_id in qa_history:
        del qa_history[patient_id]
    return {"message": "History cleared"}
