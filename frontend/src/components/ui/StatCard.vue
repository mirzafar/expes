<script setup>
import { formatMoney } from '@/utils/format'

defineProps({
  label: { type: String, required: true },
  amount: { type: Number, default: 0 },
  icon: { type: [Object, Function], default: null },
  // 'indigo' | 'emerald' | 'rose' | 'slate'
  tone: { type: String, default: 'indigo' },
  delta: { type: Number, default: null }, // % изменения, опционально
})

const tones = {
  indigo: 'bg-indigo-50 text-indigo-600',
  emerald: 'bg-emerald-50 text-emerald-600',
  rose: 'bg-rose-50 text-rose-600',
  slate: 'bg-slate-100 text-slate-600',
}
</script>

<template>
  <div class="card p-5">
    <div class="flex items-start justify-between">
      <span class="text-sm font-medium text-slate-500">{{ label }}</span>
      <div v-if="icon" :class="['flex h-9 w-9 items-center justify-center rounded-xl', tones[tone]]">
        <component :is="icon" class="h-5 w-5" :stroke-width="2" />
      </div>
    </div>
    <p class="mt-3 font-display text-2xl font-bold tracking-tight text-slate-900">
      {{ formatMoney(amount) }}
    </p>
    <div v-if="delta !== null" class="mt-1.5 flex items-center gap-1.5">
      <span
        :class="[
          'rounded-full px-1.5 py-0.5 text-xs font-semibold',
          delta >= 0 ? 'bg-emerald-50 text-emerald-600' : 'bg-rose-50 text-rose-600',
        ]"
      >
        {{ delta >= 0 ? '+' : '' }}{{ delta }}%
      </span>
      <span class="text-xs text-slate-400">за месяц</span>
    </div>
  </div>
</template>
