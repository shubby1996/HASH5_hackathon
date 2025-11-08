import React, { useEffect, useState } from 'react';
import { Box, Typography, CircularProgress, Alert } from '@mui/material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import api from '../services/api';

const ECGChart = ({ patientId }) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchECG = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await api.get(`/ecg/${patientId}`);
        const chartData = response.data.time.map((t, i) => ({
          time: t.toFixed(2),
          amplitude: response.data.amplitude[i]
        }));
        setData(chartData);
      } catch (err) {
        setError(err.response?.data?.detail || 'Failed to load ECG data');
      } finally {
        setLoading(false);
      }
    };

    fetchECG();
  }, [patientId]);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" p={3}>
        <CircularProgress size={30} />
        <Typography variant="body2" color="text.secondary" sx={{ ml: 2 }}>
          Loading ECG data...
        </Typography>
      </Box>
    );
  }

  if (error) {
    return <Alert severity="info">{error}</Alert>;
  }

  if (!data || data.length === 0) {
    return <Alert severity="info">No ECG data available for this patient</Alert>;
  }

  return (
    <Box>
      <ResponsiveContainer width="100%" height={250}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="time" 
            label={{ value: 'Time (s)', position: 'insideBottom', offset: -5 }}
          />
          <YAxis 
            label={{ value: 'Amplitude (mV)', angle: -90, position: 'insideLeft' }}
          />
          <Tooltip />
          <Line 
            type="monotone" 
            dataKey="amplitude" 
            stroke="#1976d2" 
            dot={false}
            strokeWidth={1.5}
          />
        </LineChart>
      </ResponsiveContainer>
    </Box>
  );
};

export default ECGChart;
