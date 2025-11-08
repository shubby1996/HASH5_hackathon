import React, { useEffect, useState } from 'react';
import { Box, Typography, CircularProgress, Alert, ToggleButtonGroup, ToggleButton } from '@mui/material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import axios from 'axios';

const VitalSignsChart = ({ patientId }) => {
  const [vitals, setVitals] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedVital, setSelectedVital] = useState('Heart Rate');

  useEffect(() => {
    let mounted = true;
    const fetchVitals = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await axios.get(`http://localhost:8000/api/vital-signs/${patientId}`);
        if (mounted) {
          setVitals(response.data);
          
          const available = Object.keys(response.data);
          if (available.length > 0 && !available.includes(selectedVital)) {
            setSelectedVital(available[0]);
          }
        }
      } catch (err) {
        if (mounted) {
          setError(err.response?.data?.detail || 'Failed to load vital signs');
        }
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    };

    if (patientId) {
      fetchVitals();
    }
    
    return () => { mounted = false; };
  }, [patientId]);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" p={3}>
        <CircularProgress size={30} />
        <Typography variant="body2" color="text.secondary" sx={{ ml: 2 }}>
          Loading vital signs...
        </Typography>
      </Box>
    );
  }

  if (error) {
    return <Alert severity="info">{error}</Alert>;
  }

  const vitalKeys = Object.keys(vitals);
  if (vitalKeys.length === 0) {
    return <Alert severity="info">No vital signs data available</Alert>;
  }

  const currentData = vitals[selectedVital] || [];
  const chartData = currentData.map(d => ({
    date: new Date(d.date).toLocaleDateString(),
    value: d.value,
    systolic: d.systolic,
    diastolic: d.diastolic
  })).reverse();

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'center', mb: 2 }}>
        <ToggleButtonGroup
          value={selectedVital}
          exclusive
          onChange={(e, newVital) => newVital && setSelectedVital(newVital)}
          size="small"
        >
          {vitalKeys.map(vital => (
            <ToggleButton key={vital} value={vital}>
              {vital}
            </ToggleButton>
          ))}
        </ToggleButtonGroup>
      </Box>

      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Legend />
          {selectedVital === 'Blood Pressure' ? (
            <>
              <Line type="monotone" dataKey="systolic" stroke="#e53935" name="Systolic" strokeWidth={2} />
              <Line type="monotone" dataKey="diastolic" stroke="#1e88e5" name="Diastolic" strokeWidth={2} />
            </>
          ) : (
            <Line type="monotone" dataKey="value" stroke="#1976d2" strokeWidth={2} name={selectedVital} />
          )}
        </LineChart>
      </ResponsiveContainer>

      {currentData.length > 0 && (
        <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block', textAlign: 'center' }}>
          {currentData.length} readings • Unit: {currentData[0].unit || 'N/A'}
        </Typography>
      )}
    </Box>
  );
};

export default VitalSignsChart;
