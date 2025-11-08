import React, { useEffect, useState } from 'react';
import { 
  Box, 
  Card, 
  CardContent, 
  Typography, 
  Chip,
  CircularProgress,
  Grid,
  ToggleButton,
  ToggleButtonGroup
} from '@mui/material';
import { patientService } from '../services/patientService';
import ECGChart from './ECGChart';
import MRIReports from './MRIReports';
import MRIImages from './MRIImages';
import VitalSignsChart from './VitalSignsChart';

const PatientDetail = ({ patientId, onSummaryLoad }) => {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState('vitals');

  useEffect(() => {
    let mounted = true;
    const fetchSummary = async () => {
      setLoading(true);
      try {
        const data = await patientService.getSummary(patientId);
        if (mounted) {
          setSummary(data);
          if (onSummaryLoad) {
            onSummaryLoad(data);
          }
        }
      } catch (error) {
        console.error('Error fetching summary:', error);
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    };

    if (patientId) {
      fetchSummary();
    }
    
    return () => { mounted = false; };
  }, [patientId, onSummaryLoad]);

  if (loading) {
    return (
      <Box display="flex" flexDirection="column" justifyContent="center" alignItems="center" p={4}>
        <CircularProgress />
        <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
          Loading patient data...
        </Typography>
      </Box>
    );
  }

  if (!summary) {
    return null;
  }

  return (
    <Box sx={{ mb: 3 }}>
      <Card elevation={2}>
        <CardContent>
          <Typography variant="h5" fontWeight={600} gutterBottom>
            {summary.name}
          </Typography>
          
          <Grid container spacing={2} sx={{ mb: 3, mt: 1 }}>
            <Grid item xs={6}>
              <Typography variant="caption" color="text.secondary" fontWeight={500}>GENDER</Typography>
              <Typography variant="body1">{summary.gender.charAt(0).toUpperCase() + summary.gender.slice(1)}</Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography variant="caption" color="text.secondary" fontWeight={500}>BIRTH DATE</Typography>
              <Typography variant="body1">{summary.birthDate}</Typography>
            </Grid>
          </Grid>

          {summary.conditions.length > 0 && (
            <Box sx={{ mb: 2, p: 2, bgcolor: 'error.50', borderRadius: 1 }}>
              <Typography variant="subtitle2" fontWeight={600} gutterBottom>Conditions</Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {summary.conditions.map((condition, index) => (
                  <Chip key={index} label={condition} color="error" size="small" />
                ))}
              </Box>
            </Box>
          )}

          {summary.medications.length > 0 && (
            <Box sx={{ mb: 2, p: 2, bgcolor: 'primary.50', borderRadius: 1 }}>
              <Typography variant="subtitle2" fontWeight={600} gutterBottom>Medications</Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {summary.medications.map((med, index) => (
                  <Chip key={index} label={med} color="primary" size="small" />
                ))}
              </Box>
            </Box>
          )}

          {summary.allergies.length > 0 && (
            <Box sx={{ mb: 2, p: 2, bgcolor: 'warning.50', borderRadius: 1 }}>
              <Typography variant="subtitle2" fontWeight={600} gutterBottom>Allergies</Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {summary.allergies.map((allergy, index) => (
                  <Chip key={index} label={allergy} color="warning" size="small" />
                ))}
              </Box>
            </Box>
          )}

          <Box sx={{ mt: 2, p: 1.5, bgcolor: 'grey.100', borderRadius: 1 }}>
            <Typography variant="caption" color="text.secondary" fontWeight={500}>
              {summary.has_ecg && '✅ ECG Data Available'}
              {summary.has_ecg && summary.mri_reports_count > 0 && ' • '}
              {summary.mri_reports_count > 0 && `📊 ${summary.mri_reports_count} MRI Reports`}
            </Typography>
          </Box>
        </CardContent>
      </Card>

      {/* Medical Data Visualization with Toggle */}
      {(summary.has_ecg || summary.mri_reports_count > 0) && (
        <Card elevation={2} sx={{ mt: 2 }}>
          <CardContent>
            <Typography variant="h6" fontWeight={600} gutterBottom>
              Medical Data Visualization
            </Typography>
            
            <Box sx={{ display: 'flex', justifyContent: 'center', mb: 3 }}>
              <ToggleButtonGroup
                value={viewMode}
                exclusive
                onChange={(e, newMode) => newMode && setViewMode(newMode)}
                size="small"
              >
                <ToggleButton value="vitals">
                  ❤️ Vital Signs
                </ToggleButton>
                {summary.has_ecg && (
                  <ToggleButton value="ecg">
                    📈 ECG Waveform
                  </ToggleButton>
                )}
                {summary.mri_reports_count > 0 && (
                  <ToggleButton value="mri-reports">
                    🔬 MRI Reports
                  </ToggleButton>
                )}
                {summary.mri_reports_count > 0 && (
                  <ToggleButton value="mri-images">
                    🖼️ MRI Images
                  </ToggleButton>
                )}
              </ToggleButtonGroup>
            </Box>

            {viewMode === 'vitals' && <VitalSignsChart patientId={patientId} />}
            {viewMode === 'ecg' && summary.has_ecg && <ECGChart patientId={patientId} />}
            {viewMode === 'mri-reports' && summary.mri_reports_count > 0 && <MRIReports patientId={patientId} />}
            {viewMode === 'mri-images' && summary.mri_reports_count > 0 && <MRIImages patientId={patientId} />}
          </CardContent>
        </Card>
      )}
    </Box>
  );
};

export default PatientDetail;
