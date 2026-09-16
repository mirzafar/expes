import api from './client'

// Убирает пустые фильтры, чтобы не слать ?type=&category= и т.п.
function cleanParams(params = {}) {
  const out = {}
  for (const [key, value] of Object.entries(params)) {
    if (value !== null && value !== undefined && value !== '') {
      out[key] = value
    }
  }
  return out
}

export async function listTransactions(filters = {}) {
  const { data } = await api.get('/transactions', { params: cleanParams(filters) })
  return data
}

export async function createTransaction(payload) {
  const { data } = await api.post('/transactions', payload)
  return data
}

export async function updateTransaction(id, changes) {
  const { data } = await api.put(`/transactions/${id}`, changes)
  return data
}

export async function deleteTransaction(id) {
  await api.delete(`/transactions/${id}`)
}

export async function getSummary(period = {}) {
  const { data } = await api.get('/stats/summary', { params: cleanParams(period) })
  return data
}

export async function getByCategory(type = 'expense', period = {}) {
  const { data } = await api.get('/stats/by-category', {
    params: cleanParams({ type, ...period }),
  })
  return data
}

export async function getTimeseries(months = 6) {
  const { data } = await api.get('/stats/timeseries', { params: { months } })
  return data
}
