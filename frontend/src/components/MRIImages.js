import React, { useEffect, useState } from 'react';
import { Box, Typography, CircularProgress, Alert } from '@mui/material';
import axios from 'axios';

const MRIImages = ({ patientId }) => {
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let mounted = true;
    const fetchImages = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await axios.get(`http://localhost:8000/api/mri-images/${patientId}`);
        if (mounted) {
          setImages(response.data.images || []);
        }
      } catch (err) {
        if (mounted) {
          setError(err.response?.data?.detail || 'Failed to load MRI images');
        }
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    };

    if (patientId) {
      fetchImages();
    }
    
    return () => { mounted = false; };
  }, [patientId]);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" p={3}>
        <CircularProgress size={30} />
        <Typography variant="body2" color="text.secondary" sx={{ ml: 2 }}>
          Loading MRI images...
        </Typography>
      </Box>
    );
  }

  if (error) {
    return <Alert severity="info">{error}</Alert>;
  }

  if (images.length === 0) {
    return <Alert severity="info">No MRI images available</Alert>;
  }

  return (
    <Box>
      {images.map((img, index) => (
        <Box key={index} sx={{ mb: 3 }}>
          <Typography variant="subtitle1" fontWeight={600} gutterBottom>
            {img.title}
          </Typography>
          <Box
            component="img"
            src={`data:${img.contentType};base64,${img.data}`}
            alt={img.title}
            sx={{
              width: '100%',
              maxWidth: 600,
              height: 'auto',
              borderRadius: 1,
              border: '1px solid #ddd'
            }}
          />
        </Box>
      ))}
    </Box>
  );
};

export default MRIImages;
