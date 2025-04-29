import axios from 'axios'
import { getToast } from '@/composables/usePrimeToast'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('authToken')
  if (token) {
    config.headers.Authorization = `Token ${token}`
  }
  return config
})

api.interceptors.response.use(
  response => response,
  error => {
    const toast = getToast()
    let title = 'API Error';
    let details = 'An unexpected error occurred';
    
    if (error.response) {
      if (error.response.status === 500) {
        title = 'Server Error';
        details = 'This API is not implemented yet.';
      } else {
        title = error.response.data?.error || 'API Error';
        details = error.response.data?.detail || 'An unexpected error occurred';
      }
    }    

    if (toast) {
      toast.add({
        severity: 'error',
        summary: title,
        detail: details,
        life: 4000
      })
    }

    return Promise.reject(error)
  }
)

export const ApiService = {
  get(url, config = {}) {
    return api.get(url, config)
  },
  post(url, data, config = {}) {
    return api.post(url, data, config)
  },
  put(url, data, config = {}) {
    return api.put(url, data, config)
  },
  patch(url, data, config = {}) {
    return api.patch(url, data, config)
  },
  delete(url, config = {}) {
    return api.delete(url, config)
  }
}
