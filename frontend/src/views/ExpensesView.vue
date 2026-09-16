<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { TrendingDown, Plus } from 'lucide-vue-next'
import { listTransactions, deleteTransaction, getByCategory } from '@/api/transactions'
import { useUiStore } from '@/stores/ui'
import { periodRange, DEFAULT_PERIOD } from '@/utils/period'
import StatCard from '@/components/ui/StatCard.vue'
import PeriodFilter from '@/components/ui/PeriodFilter.vue'
import TxTable from '@/components/TxTable.vue'
import CategoryDonut from '@/components/charts/CategoryDonut.vue'

const ui = useUiStore()
const period = ref(DEFAULT_PERIOD)
const items = ref([])
const byCat = ref([])
const loading = ref(true)

const total = computed(() => items.value.reduce((sum, t) => sum + t.amount, 0))

async function load() {
  loading.value = true
  const range = periodRange(period.value)
  try {
    const [list, cats] = await Promise.all([
      listTransactions({ type: 'expense', limit: 100, ...range }),
      getByCategory('expense', range),
    ])
    items.value = list
    byCat.value = cats
  } finally {
    loading.value = false
  }
}

async function onDelete(tx) {
  if (!confirm('Удалить этот расход?')) return
  await deleteTransaction(tx.id)
  ui.notifyChange()
}

onMounted(load)
watch(() => ui.changeToken, load)
</script>

<template>
  <div class="space-y-6">
    <div class="flex flex-wrap items-center justify-between gap-3">
      <PeriodFilter v-model="period" @change="load" />
      <button class="btn-primary" @click="ui.openAdd('expense')">
        <Plus class="h-4 w-4" :stroke-width="2.4" /> Расход
      </button>
    </div>

    <StatCard label="Расходы за период" :amount="total" :icon="TrendingDown" tone="rose" />

    <div class="grid grid-cols-1 gap-4 lg:grid-cols-5">
      <div class="lg:col-span-2">
        <CategoryDonut title="Расходы по категориям" :slices="byCat" />
      </div>
      <div class="lg:col-span-3">
        <h2 class="mb-3 font-display text-lg font-bold tracking-tight">Все расходы</h2>
        <TxTable :items="items" :loading="loading" empty-text="Нет расходов за период" @delete="onDelete" />
      </div>
    </div>
  </div>
</template>
