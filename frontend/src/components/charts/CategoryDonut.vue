<script setup>
import { computed } from 'vue'
import { formatMoney } from '@/utils/format'

const props = defineProps({
  title: { type: String, default: 'По категориям' },
  slices: { type: Array, default: () => [] }, // [{category, total}]
  height: { type: Number, default: 300 },
})

// Индиго-палитра с вариациями
const PALETTE = ['#4f46e5', '#7c3aed', '#0ea5e9', '#10b981', '#f59e0b', '#f43f5e', '#64748b', '#ec4899']

const series = computed(() => props.slices.map((s) => Math.round(s.total)))

const options = computed(() => ({
  chart: { type: 'donut', fontFamily: 'inherit' },
  labels: props.slices.map((s) => s.category),
  colors: PALETTE,
  stroke: { width: 0 },
  dataLabels: { enabled: false },
  legend: {
    position: 'bottom',
    fontSize: '13px',
    markers: { radius: 12 },
    itemMargin: { horizontal: 8, vertical: 3 },
  },
  plotOptions: {
    pie: {
      donut: {
        size: '70%',
        labels: {
          show: true,
          total: {
            show: true,
            label: 'Всего',
            fontSize: '13px',
            color: '#94a3b8',
            formatter: (w) => formatMoney(w.globals.seriesTotals.reduce((a, b) => a + b, 0)),
          },
        },
      },
    },
  },
  tooltip: { y: { formatter: (v) => formatMoney(v) } },
}))
</script>

<template>
  <div class="card p-5">
    <h3 class="mb-1 font-display text-base font-bold tracking-tight">{{ title }}</h3>
    <div v-if="slices.length === 0" class="flex h-64 items-center justify-center text-sm text-slate-400">
      Нет данных
    </div>
    <apexchart v-else type="donut" :height="height" :options="options" :series="series" />
  </div>
</template>
