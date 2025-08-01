// frontend/src/apiService.js

import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000', // The URL of your FastAPI backend
  headers: {
    'Content-Type': 'application/json',
  },
});

// --- Question API Functions ---

// Updated to fetch questions by category ('business' or 'customer')
export const getQuestions = (category = 'customer') => {
  return apiClient.get(`/config/questions/?category=${category}`);
};

export const createQuestion = (questionData) => {
  return apiClient.post('/config/questions/', questionData);
};

export const deleteQuestion = (questionId) => {
  return apiClient.delete(`/config/questions/${questionId}`);
};


// --- NEW Setting API Functions ---

// Fetches the saved values for the business settings
export const getSettings = () => {
  return apiClient.get('/config/settings/');
};

// Saves (creates or updates) a single business setting
export const saveSetting = (settingData) => {
  return apiClient.post('/config/settings/', settingData);
};

// --- NEW Conversation API Functions ---

export const getConversations = () => {
  return apiClient.get('/conversations/');
};

// --- NEW Auth API Functions ---

export const getAuthStatus = () => {
  return apiClient.get('/auth/status');
};
