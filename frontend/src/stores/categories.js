import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import * as catApi from '@/api/categories'

export const useCategoriesStore = defineStore('categories', () => {
  const items = ref([])
  const loaded = ref(false)

  const income = computed(() => items.value.filter((c) => c.type === 'income'))
  const expense = computed(() => items.value.filter((c) => c.type === 'expense'))

  function byType(type) {
    return type === 'income' ? income.value : expense.value
  }

  async function load(force = false) {
    if (loaded.value && !force) return
    items.value = await catApi.listCategories()
    loaded.value = true
  }

  async function add(payload) {
    await catApi.createCategory(payload)
    await load(true)
  }

  async function remove(id) {
    await catApi.deleteCategory(id)
    await load(true)
  }

  return { items, income, expense, byType, load, add, remove }
})
