import api from './api';

export const patientService = {
  getAll: async () => {
    const response = await api.get('/patients');
    return response.data;
  },

  getById: async (id) => {
    const response = await api.get(`/patients/${id}`);
    return response.data;
  },

  getSummary: async (id) => {
    const response = await api.get(`/patients/${id}/summary`);
    return response.data;
  },
};
