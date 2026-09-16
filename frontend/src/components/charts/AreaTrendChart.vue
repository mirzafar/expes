<script setup>
import { computed } from 'vue'
import { formatMonth, formatShort, formatMoney } from '@/utils/format'

const props = defineProps({
  points: { type: Array, default: () => [] }, // [{period, income, expense}]
  height: { type: Number, default: 300 },
})

const series = computed(() => [
  { name: 'Доходы', data: props.points.map((p) => Math.round(p.income)) },
  { name: 'Расходы', data: props.points.map((p) => Math.round(p.expense)) },
])

const options = computed(() => ({
  chart: {
    type: 'area',
    toolbar: { show: false },
    fontFamily: 'inherit',
    zoom: { enabled: false },
    animations: { easing: 'easeinout', speed: 400 },
  },
  colors: ['#10b981', '#f43f5e'],
  dataLabels: { enabled: false },
  stroke: { curve: 'smooth', width: 2.5 },
  fill: {
    type: 'gradient',
    gradient: { shadeIntensity: 1, opacityFrom: 0.35, opacityTo: 0.02, stops: [0, 100] },
  },
  grid: { borderColor: '#f1f5f9', strokeDashArray: 4, padding: { left: 8, right: 8 } },
  xaxis: {
    categories: props.points.map((p) => formatMonth(p.period)),
    axisBorder: { show: false },
    axisTicks: { show: false },
    labels: { style: { colors: '#94a3b8', fontSize: '12px' } },
  },
  yaxis: {
    labels: {
      style: { colors: '#94a3b8', fontSize: '12px' },
      formatter: (v) => formatShort(v),
    },
  },
  legend: { position: 'top', horizontalAlign: 'right', markers: { radius: 12 }, fontSize: '13px' },
  tooltip: { y: { formatter: (v) => formatMoney(v) } },
}))
</script>

<template>
  <div class="card p-5">
    <h3 class="font-display text-base font-bold tracking-tight">Доходы и расходы</h3>
    <p class="mb-2 text-xs text-slate-400">по месяцам</p>
    <apexchart type="area" :height="height" :options="options" :series="series" />
  </div>
</template>
