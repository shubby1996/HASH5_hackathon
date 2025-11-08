import json
from datetime import datetime
from typing import Optional

# In-memory storage (will be replaced with S3/DynamoDB later)
class StorageService:
    def __init__(self):
        self.reports = {}  # job_id -> report
        self.status = {}   # job_id -> status
    
    def save_report(self, job_id: str, report: dict):
        """Save report to storage"""
        self.reports[job_id] = report
        self.status[job_id] = {
            'job_id': job_id,
            'status': 'completed',
            'progress': 'Report generation complete',
            'created_at': datetime.utcnow().isoformat()
        }
    
    def get_report(self, job_id: str) -> Optional[dict]:
        """Get report by job ID"""
        return self.reports.get(job_id)
    
    def get_status(self, job_id: str) -> Optional[dict]:
        """Get report status"""
        return self.status.get(job_id)
    
    def set_status(self, job_id: str, status: str, progress: str = None):
        """Update report status"""
        if job_id not in self.status:
            self.status[job_id] = {
                'job_id': job_id,
                'status': status,
                'progress': progress,
                'created_at': datetime.utcnow().isoformat()
            }
        else:
            self.status[job_id]['status'] = status
            if progress:
                self.status[job_id]['progress'] = progress
    
    def get_patient_reports(self, patient_id: str) -> list:
        """Get all reports for a patient"""
        return [r for r in self.reports.values() if r.get('patient_id') == patient_id]

storage_service = StorageService()
