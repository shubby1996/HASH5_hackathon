import React, { useEffect, useState } from 'react';
import { 
  Box, 
  Card, 
  CardContent, 
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  CircularProgress,
  TextField,
  Chip
} from '@mui/material';
import usePatientStore from '../store/usePatientStore';

const PatientList = () => {
  const { patients, loading, error, fetchPatients, selectPatient, selectedPatient } = usePatientStore();
  const [searchTerm, setSearchTerm] = useState('');
  const [filterGender, setFilterGender] = useState('all');

  useEffect(() => {
    fetchPatients();
  }, [fetchPatients]);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" p={4}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box p={4}>
        <Typography color="error">Error: {error}</Typography>
      </Box>
    );
  }

  const filteredPatients = patients.filter(p => {
    const matchesSearch = p.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesGender = filterGender === 'all' || p.gender === filterGender;
    return matchesSearch && matchesGender;
  });

  return (
    <Box>
      <Card elevation={2}>
        <CardContent>
          <Typography variant="h5" fontWeight={600} gutterBottom>
            Select Patient
          </Typography>
          
          <TextField
            fullWidth
            size="small"
            placeholder="Search by name..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            sx={{ mb: 2 }}
          />
          
          <Box sx={{ mb: 2, display: 'flex', gap: 1 }}>
            <Chip 
              label="All" 
              onClick={() => setFilterGender('all')}
              color={filterGender === 'all' ? 'primary' : 'default'}
              clickable
            />
            <Chip 
              label="Male" 
              onClick={() => setFilterGender('male')}
              color={filterGender === 'male' ? 'primary' : 'default'}
              clickable
            />
            <Chip 
              label="Female" 
              onClick={() => setFilterGender('female')}
              color={filterGender === 'female' ? 'primary' : 'default'}
              clickable
            />
          </Box>
          
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            {filteredPatients.length} of {patients.length} patients
          </Typography>
          
          <FormControl fullWidth>
            <InputLabel>Choose a patient</InputLabel>
            <Select
              value={selectedPatient?.id || ''}
              label="Choose a patient"
              onChange={(e) => {
                const patient = patients.find(p => p.id === e.target.value);
                if (patient) selectPatient(patient);
              }}
            >
              {filteredPatients.map((patient) => (
                <MenuItem key={patient.id} value={patient.id}>
                  {patient.name} ({patient.gender}, {patient.birthDate})
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </CardContent>
      </Card>
    </Box>
  );
};

export default PatientList;
