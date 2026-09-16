import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import * as authApi from '@/api/auth'
import { getAccess, clearTokens } from '@/api/client'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const ready = ref(false) // первичная проверка сессии завершена

  const isAuthenticated = computed(() => user.value !== null)

  async function register(payload) {
    await authApi.register(payload)
    user.value = await authApi.fetchMe()
  }

  async function login(payload) {
    await authApi.login(payload)
    user.value = await authApi.fetchMe()
  }

  // Восстановление сессии при загрузке приложения
  async function init() {
    if (getAccess()) {
      try {
        user.value = await authApi.fetchMe()
      } catch {
        clearTokens()
        user.value = null
      }
    }
    ready.value = true
  }

  function logout() {
    clearTokens()
    user.value = null
  }

  return { user, ready, isAuthenticated, register, login, init, logout }
})
