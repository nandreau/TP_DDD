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

/*
// Optional: Handle API errors with toast
api.interceptors.response.use(
  response => response,
  error => {
    const toast = getToast()
    const message =
      error?.response?.data?.message || error.message || 'An unexpected error occurred'

    if (toast) {
      toast.add({
        severity: 'error',
        summary: 'API Error',
        detail: message,
        life: 4000
      })
    }

    return Promise.reject(error)
  }
)
*/

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
