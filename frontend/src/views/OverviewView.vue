<script setup>
import { ref, onMounted, watch } from 'vue'
import { RouterLink } from 'vue-router'
import { Wallet, TrendingUp, TrendingDown } from 'lucide-vue-next'
import {
  getSummary,
  listTransactions,
  deleteTransaction,
  getByCategory,
  getTimeseries,
} from '@/api/transactions'
import { useUiStore } from '@/stores/ui'
import { periodRange, DEFAULT_PERIOD } from '@/utils/period'
import StatCard from '@/components/ui/StatCard.vue'
import PeriodFilter from '@/components/ui/PeriodFilter.vue'
import TxTable from '@/components/TxTable.vue'
import AreaTrendChart from '@/components/charts/AreaTrendChart.vue'
import CategoryDonut from '@/components/charts/CategoryDonut.vue'

const ui = useUiStore()
const period = ref(DEFAULT_PERIOD)
const summary = ref({ total_income: 0, total_expense: 0, balance: 0, count: 0 })
const recent = ref([])
const trend = ref([])
const expenseByCat = ref([])
const loading = ref(true)

async function load() {
  loading.value = true
  const range = periodRange(period.value)
  try {
    const [s, list, ts, cats] = await Promise.all([
      getSummary(range),
      listTransactions({ ...range, limit: 6 }),
      getTimeseries(6),
      getByCategory('expense', range),
    ])
    summary.value = s
    recent.value = list
    trend.value = ts
    expenseByCat.value = cats
  } finally {
    loading.value = false
  }
}

async function onDelete(tx) {
  if (!confirm(`Удалить операцию «${tx.category || 'без категории'}»?`)) return
  await deleteTransaction(tx.id)
  ui.notifyChange()
}

onMounted(load)
watch(() => ui.changeToken, load)
</script>

<template>
  <div class="space-y-6">
    <!-- Период -->
    <div class="flex justify-end">
      <PeriodFilter v-model="period" @change="load" />
    </div>

    <!-- KPI -->
    <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
      <StatCard label="Баланс" :amount="summary.balance" :icon="Wallet" tone="indigo" />
      <StatCard label="Доходы" :amount="summary.total_income" :icon="TrendingUp" tone="emerald" />
      <StatCard label="Расходы" :amount="summary.total_expense" :icon="TrendingDown" tone="rose" />
    </div>

    <!-- Графики -->
    <div class="grid grid-cols-1 gap-4 lg:grid-cols-5">
      <div class="lg:col-span-3">
        <AreaTrendChart :points="trend" />
      </div>
      <div class="lg:col-span-2">
        <CategoryDonut title="Расходы по категориям" :slices="expenseByCat" />
      </div>
    </div>

    <!-- Последние операции -->
    <div>
      <div class="mb-3 flex items-center justify-between">
        <h2 class="font-display text-lg font-bold tracking-tight">Последние операции</h2>
        <RouterLink to="/expenses" class="text-sm font-semibold text-indigo-600 hover:text-indigo-700">
          Все операции
        </RouterLink>
      </div>
      <TxTable
        :items="recent"
        :loading="loading"
        empty-text="Нет операций за период. Нажмите «Добавить» вверху."
        @delete="onDelete"
      />
    </div>
  </div>
</template>
