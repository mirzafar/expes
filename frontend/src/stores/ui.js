import { defineStore } from 'pinia'
import { ref } from 'vue'

// Глобальное UI-состояние: модалка добавления и сигнал «данные изменились»
export const useUiStore = defineStore('ui', () => {
  const addOpen = ref(false)
  const addDefaultType = ref('expense')
  // Счётчик-сигнал: страницы следят за ним и перезагружаются при изменении данных
  const changeToken = ref(0)

  function openAdd(type = 'expense') {
    addDefaultType.value = type
    addOpen.value = true
  }
  function closeAdd() {
    addOpen.value = false
  }
  function notifyChange() {
    changeToken.value++
  }

  return { addOpen, addDefaultType, changeToken, openAdd, closeAdd, notifyChange }
})
