<script setup>
import { ref, onMounted } from 'vue'
import { Plus, Trash2, TrendingUp, TrendingDown } from 'lucide-vue-next'
import { useCategoriesStore } from '@/stores/categories'
import { useToastStore } from '@/stores/toast'

const cats = useCategoriesStore()
const toast = useToastStore()

// Формы добавления для каждого типа
const forms = ref({
  income: { name: '', icon: '' },
  expense: { name: '', icon: '' },
})

onMounted(() => cats.load(true))

async function add(type) {
  const f = forms.value[type]
  if (!f.name.trim()) return
  try {
    await cats.add({ name: f.name.trim(), type, icon: f.icon || null })
    f.name = ''
    f.icon = ''
    toast.success('Категория добавлена')
  } catch (e) {
    toast.error(e.response?.data?.detail || 'Не удалось добавить')
  }
}

async function remove(cat) {
  if (!confirm(`Удалить категорию «${cat.name}»?`)) return
  await cats.remove(cat.id)
  toast.success('Категория удалена')
}
</script>

<template>
  <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
    <!-- Доходы -->
    <section class="card p-5">
      <div class="mb-4 flex items-center gap-2">
        <div class="flex h-9 w-9 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600">
          <TrendingUp class="h-5 w-5" />
        </div>
        <h2 class="font-display text-lg font-bold tracking-tight">Категории доходов</h2>
      </div>

      <div class="space-y-2">
        <div
          v-for="c in cats.income"
          :key="c.id"
          class="group flex items-center gap-3 rounded-xl border border-slate-100 px-3 py-2.5"
        >
          <span class="text-lg">{{ c.icon || '💰' }}</span>
          <span class="flex-1 text-sm font-medium text-slate-800">{{ c.name }}</span>
          <button class="rounded-lg p-1.5 text-slate-300 hover:bg-rose-50 hover:text-rose-500" @click="remove(c)">
            <Trash2 class="h-4 w-4" />
          </button>
        </div>
        <p v-if="cats.income.length === 0" class="py-4 text-center text-sm text-slate-400">Нет категорий</p>
      </div>

      <form class="mt-4 flex gap-2" @submit.prevent="add('income')">
        <input v-model="forms.income.icon" class="input w-14 text-center" placeholder="🙂" maxlength="2" />
        <input v-model="forms.income.name" class="input flex-1" placeholder="Название категории" />
        <button class="btn-primary shrink-0" type="submit"><Plus class="h-4 w-4" /></button>
      </form>
    </section>

    <!-- Расходы -->
    <section class="card p-5">
      <div class="mb-4 flex items-center gap-2">
        <div class="flex h-9 w-9 items-center justify-center rounded-xl bg-rose-50 text-rose-600">
          <TrendingDown class="h-5 w-5" />
        </div>
        <h2 class="font-display text-lg font-bold tracking-tight">Категории расходов</h2>
      </div>

      <div class="space-y-2">
        <div
          v-for="c in cats.expense"
          :key="c.id"
          class="group flex items-center gap-3 rounded-xl border border-slate-100 px-3 py-2.5"
        >
          <span class="text-lg">{{ c.icon || '💸' }}</span>
          <span class="flex-1 text-sm font-medium text-slate-800">{{ c.name }}</span>
          <button class="rounded-lg p-1.5 text-slate-300 hover:bg-rose-50 hover:text-rose-500" @click="remove(c)">
            <Trash2 class="h-4 w-4" />
          </button>
        </div>
        <p v-if="cats.expense.length === 0" class="py-4 text-center text-sm text-slate-400">Нет категорий</p>
      </div>

      <form class="mt-4 flex gap-2" @submit.prevent="add('expense')">
        <input v-model="forms.expense.icon" class="input w-14 text-center" placeholder="🙂" maxlength="2" />
        <input v-model="forms.expense.name" class="input flex-1" placeholder="Название категории" />
        <button class="btn-primary shrink-0" type="submit"><Plus class="h-4 w-4" /></button>
      </form>
    </section>
  </div>
</template>
