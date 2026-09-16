import api, { setTokens } from './client'

// Регистрация: возвращает пару токенов и сразу их сохраняет
export async function register({ email, password, name }) {
  const { data } = await api.post('/auth/register', { email, password, name })
  setTokens(data.access_token, data.refresh_token)
  return data
}

// Вход: бэкенд ждёт форму OAuth2 (username = email)
export async function login({ email, password }) {
  const form = new URLSearchParams()
  form.append('username', email)
  form.append('password', password)
  const { data } = await api.post('/auth/login', form, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  })
  setTokens(data.access_token, data.refresh_token)
  return data
}

// Текущий пользователь
export async function fetchMe() {
  const { data } = await api.get('/auth/me')
  return data
}
