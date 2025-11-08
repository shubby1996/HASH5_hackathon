from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List
import uuid
from datetime import datetime

from app.models.report import ReportGenerateRequest, ReportStatus, Report
from app.services.healthlake_service import healthlake_service
from app.services.bedrock_service import bedrock_service
from app.services.storage_service import storage_service

router = APIRouter()

def generate_report_task(job_id: str, patient_id: str, patient_summary: dict):
    """Background task to generate report"""
    try:
        # Update status
        storage_service.set_status(job_id, 'processing', 'Starting report generation...')
        
        # Generate report
        def update_progress(message: str):
            storage_service.set_status(job_id, 'processing', message)
        
        report_data = bedrock_service.generate_comprehensive_report(
            patient_id,
            patient_summary,
            progress_callback=update_progress
        )
        
        # Save report
        report = {
            'job_id': job_id,
            'patient_id': patient_id,
            'patient_name': patient_summary.get('name', 'Unknown'),
            'cardiology': report_data['cardiology'],
            'radiology': report_data['radiology'],
            'endocrinology': report_data['endocrinology'],
            'comprehensive': report_data['comprehensive'],
            'created_at': datetime.utcnow().isoformat(),
            'status': 'completed'
        }
        
        storage_service.save_report(job_id, report)
        
    except Exception as e:
        storage_service.set_status(job_id, 'failed', f'Error: {str(e)}')

@router.post("/reports/generate", response_model=ReportStatus)
async def generate_report(request: ReportGenerateRequest, background_tasks: BackgroundTasks):
    """Start report generation (async)"""
    try:
        # Get patient summary
        patient_summary = healthlake_service.get_patient_summary(request.patient_id)
        
        # Create job
        job_id = str(uuid.uuid4())
        
        # Set initial status
        storage_service.set_status(job_id, 'pending', 'Report generation queued')
        
        # Start background task
        background_tasks.add_task(generate_report_task, job_id, request.patient_id, patient_summary)
        
        return {
            'job_id': job_id,
            'status': 'pending',
            'progress': 'Report generation queued',
            'created_at': datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/reports/status/{job_id}", response_model=ReportStatus)
async def get_report_status(job_id: str):
    """Get report generation status"""
    status = storage_service.get_status(job_id)
    
    if not status:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return status

@router.get("/reports/{job_id}", response_model=Report)
async def get_report(job_id: str):
    """Get completed report"""
    report = storage_service.get_report(job_id)
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    return report

@router.get("/reports/patient/{patient_id}", response_model=List[Report])
async def get_patient_reports(patient_id: str):
    """Get all reports for a patient"""
    reports = storage_service.get_patient_reports(patient_id)
    return reports
