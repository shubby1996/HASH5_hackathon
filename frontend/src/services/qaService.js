import api from './api';

export const qaService = {
  ask: async (question, cachedReports) => {
    const response = await api.post('/qa/ask', {
      question,
      cached_reports: cachedReports,
    });
    return response.data;
  },

  getHistory: async (patientId) => {
    const response = await api.get(`/qa/history/${patientId}`);
    return response.data;
  },
};
