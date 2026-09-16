<script setup>
import { PERIODS } from '@/utils/period'

defineProps({
  modelValue: { type: String, default: 'month' },
})
const emit = defineEmits(['update:modelValue', 'change'])

function select(key) {
  emit('update:modelValue', key)
  emit('change', key)
}
</script>

<template>
  <div class="inline-flex rounded-xl border border-slate-200 bg-white p-0.5">
    <button
      v-for="p in PERIODS"
      :key="p.key"
      :class="[
        'rounded-lg px-3 py-1.5 text-sm font-semibold transition',
        modelValue === p.key ? 'bg-indigo-600 text-white' : 'text-slate-500 hover:text-slate-900',
      ]"
      @click="select(p.key)"
    >
      {{ p.label }}
    </button>
  </div>
</template>
