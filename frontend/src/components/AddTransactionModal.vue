<script setup>
import { ref, watch, computed } from 'vue'
import { createTransaction } from '@/api/transactions'
import { useUiStore } from '@/stores/ui'
import { useToastStore } from '@/stores/toast'
import { useCategoriesStore } from '@/stores/categories'
import BaseModal from '@/components/ui/BaseModal.vue'

const ui = useUiStore()
const toast = useToastStore()
const cats = useCategoriesStore()

const type = ref('expense')
const amount = ref('')
const category = ref('')
const date = ref('')
const note = ref('')
const error = ref('')
const submitting = ref(false)

// Дата по умолчанию — сегодня (YYYY-MM-DD)
function todayStr() {
  const d = new Date()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${d.getFullYear()}-${m}-${day}`
}

// Категории для выбранного типа
const options = computed(() => cats.byType(type.value))

// При открытии: подставляем тип, сегодняшнюю дату, грузим категории
watch(
  () => ui.addOpen,
  (open) => {
    if (open) {
      type.value = ui.addDefaultType
      amount.value = ''
      category.value = ''
      date.value = todayStr()
      note.value = ''
      error.value = ''
      cats.load()
    }
  }
)

// При смене типа сбрасываем выбранную категорию (у доходов и расходов они разные)
watch(type, () => {
  category.value = ''
})

async function onSubmit() {
  error.value = ''
  submitting.value = true
  try {
    const payload = {
      type: type.value,
      amount: Number(amount.value),
      category: category.value || null,
      note: note.value || null,
    }
    if (date.value) payload.date = new Date(date.value).toISOString()

    await createTransaction(payload)
    ui.notifyChange()
    ui.closeAdd()
    toast.success(type.value === 'income' ? 'Доход добавлен' : 'Расход добавлен')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Не удалось сохранить. Попробуйте ещё раз.'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <BaseModal :open="ui.addOpen" title="Новая операция" @close="ui.closeAdd">
    <form class="space-y-4" @submit.prevent="onSubmit">
      <!-- Переключатель типа -->
      <div class="grid grid-cols-2 gap-2 rounded-xl bg-slate-100 p-1">
        <button
          type="button"
          :class="[
            'rounded-lg py-2 text-sm font-semibold transition',
            type === 'expense' ? 'bg-white text-rose-600 shadow-sm' : 'text-slate-500',
          ]"
          @click="type = 'expense'"
        >
          Расход
        </button>
        <button
          type="button"
          :class="[
            'rounded-lg py-2 text-sm font-semibold transition',
            type === 'income' ? 'bg-white text-emerald-600 shadow-sm' : 'text-slate-500',
          ]"
          @click="type = 'income'"
        >
          Доход
        </button>
      </div>

      <div>
        <label class="label">Сумма</label>
        <input
          v-model="amount"
          type="number"
          step="0.01"
          min="0.01"
          class="input"
          required
          placeholder="0.00"
          autofocus
        />
      </div>

      <div>
        <label class="label">Категория</label>
        <select v-model="category" class="input">
          <option value="">Без категории</option>
          <option v-for="c in options" :key="c.id" :value="c.name">
            {{ c.icon ? c.icon + ' ' : '' }}{{ c.name }}
          </option>
        </select>
        <RouterLink
          to="/categories"
          class="mt-1 inline-block text-xs font-medium text-indigo-600 hover:text-indigo-700"
          @click="ui.closeAdd"
        >
          + Управлять категориями
        </RouterLink>
      </div>

      <div>
        <label class="label">Дата</label>
        <input v-model="date" type="date" class="input" />
      </div>

      <div>
        <label class="label">Заметка</label>
        <input v-model="note" type="text" class="input" placeholder="необязательно" />
      </div>

      <p v-if="error" class="rounded-xl bg-red-50 px-3.5 py-2.5 text-sm text-red-600">{{ error }}</p>

      <div class="flex justify-end gap-2 pt-1">
        <button type="button" class="btn-ghost" @click="ui.closeAdd">Отмена</button>
        <button type="submit" class="btn-primary" :disabled="submitting">
          {{ submitting ? 'Сохраняем…' : 'Добавить' }}
        </button>
      </div>
    </form>
  </BaseModal>
</template>
