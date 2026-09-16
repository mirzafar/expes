import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

// Ключи для хранения токенов в localStorage
export const ACCESS_KEY = 'expes_access'
export const REFRESH_KEY = 'expes_refresh'

export function getAccess() {
  return localStorage.getItem(ACCESS_KEY)
}
export function getRefresh() {
  return localStorage.getItem(REFRESH_KEY)
}
export function setTokens(access, refresh) {
  localStorage.setItem(ACCESS_KEY, access)
  localStorage.setItem(REFRESH_KEY, refresh)
}
export function clearTokens() {
  localStorage.removeItem(ACCESS_KEY)
  localStorage.removeItem(REFRESH_KEY)
}

// Основной клиент — с авторизацией
const api = axios.create({ baseURL: API_URL })

// Отдельный «голый» клиент для запроса refresh, чтобы не зациклить перехватчики
const bare = axios.create({ baseURL: API_URL })

// Подставляем access-токен в каждый запрос
api.interceptors.request.use((config) => {
  const token = getAccess()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Что делать при отзыве сессии (задаётся из main.js, чтобы избежать циклов импорта)
let onAuthFailure = () => {}
export function setOnAuthFailure(fn) {
  onAuthFailure = fn
}

// При 401 один раз пробуем обновить токен и повторить запрос
let refreshing = null

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config
    const status = error.response?.status

    if (status !== 401 || original._retried) {
      return Promise.reject(error)
    }

    const refresh = getRefresh()
    if (!refresh) {
      onAuthFailure()
      return Promise.reject(error)
    }

    original._retried = true
    try {
      // Если несколько запросов упали одновременно — обновляем токен один раз
      if (!refreshing) {
        refreshing = bare
          .post('/auth/refresh', { refresh_token: refresh })
          .then((res) => {
            setTokens(res.data.access_token, res.data.refresh_token)
            return res.data.access_token
          })
          .finally(() => {
            refreshing = null
          })
      }
      const newAccess = await refreshing
      original.headers.Authorization = `Bearer ${newAccess}`
      return api(original)
    } catch (refreshErr) {
      clearTokens()
      onAuthFailure()
      return Promise.reject(refreshErr)
    }
  }
)

export default api
