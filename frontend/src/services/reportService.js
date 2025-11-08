import api from './api';

export const reportService = {
  generate: async (patientId) => {
    const response = await api.post('/reports/generate', { patient_id: patientId });
    return response.data;
  },

  getStatus: async (jobId) => {
    const response = await api.get(`/reports/status/${jobId}`);
    return response.data;
  },

  getReport: async (jobId) => {
    const response = await api.get(`/reports/${jobId}`);
    return response.data;
  },

  pollUntilComplete: async (jobId, onProgress) => {
    return new Promise((resolve, reject) => {
      const interval = setInterval(async () => {
        try {
          const status = await reportService.getStatus(jobId);
          
          if (onProgress) {
            onProgress(status);
          }

          if (status.status === 'completed') {
            clearInterval(interval);
            const report = await reportService.getReport(jobId);
            resolve(report);
          } else if (status.status === 'failed') {
            clearInterval(interval);
            reject(new Error(status.progress || 'Report generation failed'));
          }
        } catch (error) {
          clearInterval(interval);
          reject(error);
        }
      }, 3000); // Poll every 3 seconds
    });
  },
};
