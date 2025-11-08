import React, { useEffect, useState } from 'react';
import { 
  Box, 
  Typography, 
  CircularProgress,
  Accordion,
  AccordionSummary,
  AccordionDetails
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import api from '../services/api';

const MRIReports = ({ patientId }) => {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let mounted = true;
    const fetchMRI = async () => {
      setLoading(true);
      try {
        const response = await api.get(`/mri/${patientId}`);
        if (mounted) {
          setReports(response.data.reports || []);
        }
      } catch (error) {
        console.error('Error fetching MRI:', error);
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    };

    fetchMRI();
    return () => { mounted = false; };
  }, [patientId]);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" p={2}>
        <CircularProgress size={24} />
        <Typography variant="caption" color="text.secondary" sx={{ ml: 1 }}>
          Loading reports...
        </Typography>
      </Box>
    );
  }

  if (reports.length === 0) {
    return (
      <Typography variant="body2" color="text.secondary">
        No MRI reports available
      </Typography>
    );
  }

  return (
    <Box>
      {reports.map((report, index) => (
        <Accordion key={index} sx={{ mb: 1 }}>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            <Box>
              <Typography variant="subtitle2" fontWeight={600}>
                {report.type}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                {report.date.substring(0, 10)} • {report.status}
              </Typography>
            </Box>
          </AccordionSummary>
          <AccordionDetails>
            <Typography variant="body2" style={{ whiteSpace: 'pre-wrap' }}>
              {report.conclusion}
            </Typography>
          </AccordionDetails>
        </Accordion>
      ))}
    </Box>
  );
};

export default MRIReports;
