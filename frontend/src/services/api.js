import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API Service Functions
export const assessmentService = {
  // Start new assessment
  startAssessment: async (personalData) => {
    const response = await api.post('/api/assessment/start', personalData);
    return response.data;
  },

  // Update physical details
  updatePhysical: async (assessmentId, physicalData) => {
    const response = await api.put(`/api/assessment/${assessmentId}/physical`, physicalData);
    return response.data;
  },

  // Update education details
  updateEducation: async (assessmentId, educationData) => {
    const response = await api.put(`/api/assessment/${assessmentId}/education`, educationData);
    return response.data;
  },

  // Get OLQ questions
  getOLQQuestions: async () => {
    const response = await api.get('/api/assessment/olq-questions');
    return response.data;
  },

  // Submit OLQ responses
  submitOLQ: async (olqData, sessionId) => {
    const url = sessionId 
      ? `/api/assessment/olq?session_id=${sessionId}`
      : '/api/assessment/olq';
    const response = await api.post(url, olqData);
    return response.data;
  },

  // Get assessment details
  getAssessment: async (assessmentId) => {
    const response = await api.get(`/api/assessment/${assessmentId}`);
    return response.data;
  },
};

export const recommendationService = {
  // Generate recommendations
  generateRecommendations: async (assessmentId) => {
    const response = await api.post('/api/recommendations/generate', {
      assessment_id: assessmentId,
    });
    return response.data;
  },

  // Get recommendation details
  getRecommendation: async (recommendationId) => {
    const response = await api.get(`/api/recommendations/${recommendationId}`);
    return response.data;
  },

  // Export recommendation as PDF
  exportPDF: async (recommendationId) => {
    const response = await api.get(`/api/recommendations/${recommendationId}/export`, {
      responseType: 'blob',
    });
    return response.data;
  },
};

export const studyPlanService = {
  // Generate study plan
  generateStudyPlan: async (planData) => {
    const response = await api.post('/api/study-plan/generate', planData);
    return response.data;
  },

  // Get study plan details
  getStudyPlan: async (planId) => {
    const response = await api.get(`/api/study-plan/${planId}`);
    return response.data;
  },
};

export const resourceService = {
  // Get resources for a role
  getResources: async (role) => {
    const response = await api.get(`/api/resources/${encodeURIComponent(role)}`);
    return response.data;
  },
};

export default api;
