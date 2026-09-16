import api from './client'

export async function listCategories(type) {
  const params = type ? { type } : {}
  const { data } = await api.get('/categories', { params })
  return data
}

export async function createCategory(payload) {
  const { data } = await api.post('/categories', payload)
  return data
}

export async function deleteCategory(id) {
  await api.delete(`/categories/${id}`)
}
