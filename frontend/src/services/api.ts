import axios from 'axios';

const api = axios.create({
  baseURL: "http://127.0.0.1:8000"
});

// Tratamento global de erros
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const message = error.response?.data?.detail || error.message || "Erro desconhecido";
    return Promise.reject(message);
  }
);

export const leadService = {
  list: () => api.get('/leads').then(res => res.data),
  scrape: (term: string) => api.post('/scrape', { term, limit: 3 }),
  send: () => api.post('/send', { limit: 3 }),
  monitor: () => api.post('/monitor').then(res => res.data),
};