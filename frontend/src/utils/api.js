import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Важно для работы с httpOnly cookies
});

// Request interceptor to add token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // If token expired, try to refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        // Backend использует httpOnly cookies для refresh_token
        const response = await axios.post(`${API_URL}/auth/refresh`, {}, {
          withCredentials: true // Важно для отправки cookies
        });

        const { access_token } = response.data;
        localStorage.setItem('access_token', access_token);

        originalRequest.headers.Authorization = `Bearer ${access_token}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Refresh failed, logout user
        localStorage.removeItem('access_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// Auth API calls
export const loginUser = async (credentials) => {
  try {
    // Backend использует /signin endpoint
    const response = await api.post('/auth/signin', credentials);
    return {
      access_token: response.data.access_token,
      token_type: response.data.token_type,
      // refresh_token хранится в httpOnly cookie на бэкенде
    };
  } catch (error) {
    throw new Error(
      error.response?.data?.message ||
      error.response?.data?.detail ||
      'Неверный email или пароль'
    );
  }
};

export const registerUser = async (userData) => {
  try {
    // Backend использует /signup endpoint и не возвращает токен
    // Поэтому после регистрации нужно сделать авторизацию
    await api.post('/auth/signup', {
      email: userData.email,
      password: userData.password
    });

    // После успешной регистрации делаем вход
    return await loginUser({
      email: userData.email,
      password: userData.password
    });
  } catch (error) {
    throw new Error(
      error.response?.data?.message ||
      error.response?.data?.detail ||
      'Ошибка регистрации'
    );
  }
};

export const logoutUser = async () => {
  try {
    // Backend использует httpOnly cookies для refresh_token
    await api.post('/auth/logout');
  } catch (error) {
    console.error('Logout error:', error);
  } finally {
    localStorage.removeItem('access_token');
  }
};

export const getCurrentUser = async () => {
  try {
    const response = await api.get('/auth/me');
    return response.data;
  } catch (error) {
    throw new Error('Не удалось получить данные пользователя');
  }
};

export default api;
