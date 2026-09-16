<script setup>
import { ref, onMounted, watch } from 'vue'
import { Wallet, TrendingUp, TrendingDown } from 'lucide-vue-next'
import { getTimeseries, getByCategory, getSummary } from '@/api/transactions'
import { useUiStore } from '@/stores/ui'
import { periodRange, DEFAULT_PERIOD } from '@/utils/period'
import StatCard from '@/components/ui/StatCard.vue'
import PeriodFilter from '@/components/ui/PeriodFilter.vue'
import AreaTrendChart from '@/components/charts/AreaTrendChart.vue'
import CategoryDonut from '@/components/charts/CategoryDonut.vue'

const ui = useUiStore()
const period = ref(DEFAULT_PERIOD)
const trend = ref([])
const incomeByCat = ref([])
const expenseByCat = ref([])
const summary = ref({ total_income: 0, total_expense: 0, balance: 0 })
const months = ref(6)
const loading = ref(true)

const monthOptions = [
  { label: '6 мес', value: 6 },
  { label: '12 мес', value: 12 },
]

// Сводка и разбивка по категориям — за выбранный период
async function loadPeriod() {
  const range = periodRange(period.value)
  const [inc, exp, s] = await Promise.all([
    getByCategory('income', range),
    getByCategory('expense', range),
    getSummary(range),
  ])
  incomeByCat.value = inc
  expenseByCat.value = exp
  summary.value = s
}

// Тренд — за N месяцев
async function loadTrend() {
  trend.value = await getTimeseries(months.value)
}

async function load() {
  loading.value = true
  try {
    await Promise.all([loadPeriod(), loadTrend()])
  } finally {
    loading.value = false
  }
}

function setMonths(m) {
  months.value = m
  loadTrend()
}

onMounted(load)
watch(() => ui.changeToken, load)
</script>

<template>
  <div class="space-y-6">
    <!-- Период -->
    <div class="flex justify-end">
      <PeriodFilter v-model="period" @change="loadPeriod" />
    </div>

    <!-- Итоги за период -->
    <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
      <StatCard label="Баланс" :amount="summary.balance" :icon="Wallet" tone="indigo" />
      <StatCard label="Доходы" :amount="summary.total_income" :icon="TrendingUp" tone="emerald" />
      <StatCard label="Расходы" :amount="summary.total_expense" :icon="TrendingDown" tone="rose" />
    </div>

    <!-- Тренд с отдельным переключателем месяцев -->
    <div>
      <div class="mb-3 flex items-center justify-between">
        <h2 class="font-display text-lg font-bold tracking-tight">Тренд по месяцам</h2>
        <div class="inline-flex rounded-xl border border-slate-200 bg-white p-0.5">
          <button
            v-for="m in monthOptions"
            :key="m.value"
            :class="[
              'rounded-lg px-3 py-1.5 text-sm font-semibold transition',
              months === m.value ? 'bg-indigo-600 text-white' : 'text-slate-500 hover:text-slate-900',
            ]"
            @click="setMonths(m.value)"
          >
            {{ m.label }}
          </button>
        </div>
      </div>
      <AreaTrendChart :points="trend" :height="340" />
    </div>

    <!-- Две круговых за период -->
    <div class="grid grid-cols-1 gap-4 lg:grid-cols-2">
      <CategoryDonut title="Доходы по категориям" :slices="incomeByCat" />
      <CategoryDonut title="Расходы по категориям" :slices="expenseByCat" />
    </div>
  </div>
</template>
