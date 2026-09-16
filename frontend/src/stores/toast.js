import { defineStore } from 'pinia'
import { ref } from 'vue'

let counter = 0

export const useToastStore = defineStore('toast', () => {
  const toasts = ref([])

  function push(message, type = 'success', timeout = 3000) {
    const id = ++counter
    toasts.value.push({ id, message, type })
    setTimeout(() => remove(id), timeout)
  }

  function remove(id) {
    toasts.value = toasts.value.filter((t) => t.id !== id)
  }

  const success = (msg) => push(msg, 'success')
  const error = (msg) => push(msg, 'error')

  return { toasts, push, remove, success, error }
})
