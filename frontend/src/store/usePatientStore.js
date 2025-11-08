import { create } from 'zustand';
import { patientService } from '../services/patientService';

const usePatientStore = create((set) => ({
  patients: [],
  selectedPatient: null,
  loading: false,
  error: null,

  fetchPatients: async () => {
    set({ loading: true, error: null });
    try {
      const patients = await patientService.getAll();
      set({ patients, loading: false });
    } catch (error) {
      set({ error: error.message, loading: false });
    }
  },

  selectPatient: (patient) => {
    set({ selectedPatient: patient });
  },

  clearSelection: () => {
    set({ selectedPatient: null });
  },
}));

export default usePatientStore;
