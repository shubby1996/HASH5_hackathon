import React, { useEffect, useState } from 'react';
import { Box, Grid, Card, CardContent, Typography, CircularProgress } from '@mui/material';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { patientService } from '../services/patientService';

const COLORS = ['#1976d2', '#e91e63', '#4caf50', '#ff9800', '#9c27b0', '#00bcd4'];

const Dashboard = () => {
  const [stats, setStats] = useState({
    total: 0,
    genderData: [],
    ageData: []
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const patients = await patientService.getAll();
        
        // Calculate statistics
        const genderCount = patients.reduce((acc, p) => {
          acc[p.gender] = (acc[p.gender] || 0) + 1;
          return acc;
        }, {});

        const ageGroups = patients.reduce((acc, p) => {
          const year = parseInt(p.birthDate.split('-')[0]);
          const age = new Date().getFullYear() - year;
          const group = age < 18 ? '0-17' : age < 40 ? '18-39' : age < 60 ? '40-59' : '60+';
          acc[group] = (acc[group] || 0) + 1;
          return acc;
        }, {});

        setStats({
          total: patients.length,
          genderData: Object.keys(genderCount).map(key => ({
            name: key.charAt(0).toUpperCase() + key.slice(1),
            value: genderCount[key]
          })),
          ageData: Object.keys(ageGroups).map(key => ({
            name: key,
            count: ageGroups[key]
          }))
        });
      } catch (error) {
        console.error('Error fetching stats:', error);
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" p={4}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ p: 3 }}>
        <Typography variant="h6" color="error">
          Error loading dashboard: {error}
        </Typography>
        <Typography variant="body2" sx={{ mt: 2 }}>
          Make sure the backend is running at http://localhost:8000
        </Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" fontWeight={700} gutterBottom>
        📊 Healthcare Dashboard
      </Typography>

      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} md={4}>
          <Card elevation={3} sx={{ bgcolor: 'primary.main', color: 'white' }}>
            <CardContent>
              <Typography variant="h6">Total Patients</Typography>
              <Typography variant="h2" fontWeight={700}>{stats.total}</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card elevation={3} sx={{ bgcolor: 'success.main', color: 'white' }}>
            <CardContent>
              <Typography variant="h6">Male Patients</Typography>
              <Typography variant="h2" fontWeight={700}>
                {stats.genderData.find(d => d.name === 'Male')?.value || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card elevation={3} sx={{ bgcolor: 'secondary.main', color: 'white' }}>
            <CardContent>
              <Typography variant="h6">Female Patients</Typography>
              <Typography variant="h2" fontWeight={700}>
                {stats.genderData.find(d => d.name === 'Female')?.value || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card elevation={2}>
            <CardContent>
              <Typography variant="h6" fontWeight={600} gutterBottom>
                Gender Distribution
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={stats.genderData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    outerRadius={100}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {stats.genderData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card elevation={2}>
            <CardContent>
              <Typography variant="h6" fontWeight={600} gutterBottom>
                Age Distribution
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={stats.ageData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="count" fill="#1976d2" name="Patients" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
