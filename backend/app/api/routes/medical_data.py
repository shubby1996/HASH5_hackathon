from fastapi import APIRouter, HTTPException
from app.services.healthlake_service import healthlake_service

router = APIRouter()

@router.get("/ecg/{patient_id}")
async def get_ecg_data(patient_id: str):
    """Get ECG waveform data for patient"""
    try:
        waveform_obs = healthlake_service.search('Observation', {
            'patient': patient_id, 
            'code': '131328', 
            '_count': '1'
        })
        
        if waveform_obs.get('entry'):
            obs = waveform_obs['entry'][0]['resource']
            if 'valueSampledData' in obs:
                sampled_data = obs['valueSampledData']
                data_string = sampled_data['data']
                period_ms = sampled_data['period']
                
                waveform = [float(x) for x in data_string.split()]
                time = [i * period_ms / 1000 for i in range(len(waveform))]
                
                return {
                    'time': time,
                    'amplitude': waveform,
                    'patient': obs.get('subject', {}).get('display', 'Unknown')
                }
        
        raise HTTPException(status_code=404, detail="No ECG data found")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mri/{patient_id}")
async def get_mri_reports(patient_id: str):
    """Get MRI diagnostic reports for patient"""
    try:
        reports = healthlake_service.search('DiagnosticReport', {
            'patient': patient_id, 
            '_count': '10'
        })
        
        mri_reports = []
        if reports.get('entry'):
            for entry in reports['entry']:
                r = entry['resource']
                mri_reports.append({
                    'type': r.get('code', {}).get('text', 'Unknown'),
                    'conclusion': r.get('conclusion', 'No findings available'),
                    'status': r.get('status', 'unknown'),
                    'date': r.get('effectiveDateTime', 'Unknown')
                })
        
        return {'reports': mri_reports}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mri-images/{patient_id}")
async def get_mri_images(patient_id: str):
    """Get MRI images for patient"""
    try:
        media = healthlake_service.search('Media', {
            'patient': patient_id, 
            '_count': '10'
        })
        
        images = []
        if media.get('entry'):
            for entry in media['entry']:
                m = entry['resource']
                if 'content' in m and 'data' in m['content']:
                    images.append({
                        'data': m['content']['data'],
                        'title': m['content'].get('title', 'MRI Image'),
                        'contentType': m['content'].get('contentType', 'image/png')
                    })
        
        return {'images': images}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/vital-signs/{patient_id}")
async def get_vital_signs(patient_id: str):
    """Get vital signs trends for patient"""
    try:
        vital_codes = {
            '85354-9': 'Blood Pressure',
            '8867-4': 'Heart Rate',
            '8310-5': 'Body Temperature',
            '9279-1': 'Respiratory Rate',
            '2708-6': 'Oxygen Saturation'
        }
        
        vitals = {}
        
        for code, name in vital_codes.items():
            obs = healthlake_service.search('Observation', {
                'patient': patient_id,
                'code': code,
                '_count': '20',
                '_sort': '-date'
            })
            
            data_points = []
            if obs.get('entry'):
                for entry in obs['entry']:
                    r = entry['resource']
                    date = r.get('effectiveDateTime', r.get('issued', ''))
                    
                    if 'valueQuantity' in r:
                        val = r['valueQuantity']
                        data_points.append({
                            'date': date,
                            'value': val.get('value'),
                            'unit': val.get('unit', '')
                        })
                    elif 'component' in r and name == 'Blood Pressure':
                        bp_data = {'date': date}
                        for comp in r['component']:
                            comp_name = comp.get('code', {}).get('text', '')
                            if 'valueQuantity' in comp:
                                if 'Systolic' in comp_name:
                                    bp_data['systolic'] = comp['valueQuantity'].get('value')
                                elif 'Diastolic' in comp_name:
                                    bp_data['diastolic'] = comp['valueQuantity'].get('value')
                                bp_data['unit'] = comp['valueQuantity'].get('unit', 'mm[Hg]')
                        if 'systolic' in bp_data or 'diastolic' in bp_data:
                            data_points.append(bp_data)
            
            if data_points:
                vitals[name] = data_points
        
        return vitals
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
