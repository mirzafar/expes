<script setup>
import { ArrowUpRight, ArrowDownRight, Trash2, Inbox } from 'lucide-vue-next'
import { formatMoney, formatDate } from '@/utils/format'

defineProps({
  items: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
  emptyText: { type: String, default: 'Пока нет операций' },
})
const emit = defineEmits(['delete'])
</script>

<template>
  <div class="card overflow-hidden">
    <!-- Загрузка -->
    <div v-if="loading" class="divide-y divide-slate-100">
      <div v-for="n in 4" :key="n" class="flex items-center gap-4 px-5 py-4">
        <div class="h-10 w-10 animate-pulse rounded-full bg-slate-100"></div>
        <div class="flex-1 space-y-2">
          <div class="h-3 w-32 animate-pulse rounded bg-slate-100"></div>
          <div class="h-3 w-20 animate-pulse rounded bg-slate-100"></div>
        </div>
        <div class="h-4 w-16 animate-pulse rounded bg-slate-100"></div>
      </div>
    </div>

    <!-- Пусто -->
    <div v-else-if="items.length === 0" class="flex flex-col items-center justify-center py-16 text-center">
      <div class="flex h-12 w-12 items-center justify-center rounded-2xl bg-slate-100 text-slate-400">
        <Inbox class="h-6 w-6" />
      </div>
      <p class="mt-3 text-sm font-medium text-slate-500">{{ emptyText }}</p>
    </div>

    <!-- Список -->
    <div v-else class="divide-y divide-slate-100">
      <div
        v-for="tx in items"
        :key="tx.id"
        class="group flex items-center gap-4 px-5 py-3.5 hover:bg-slate-50/60"
      >
        <div
          :class="[
            'flex h-10 w-10 items-center justify-center rounded-full',
            tx.type === 'income' ? 'bg-emerald-50 text-emerald-600' : 'bg-rose-50 text-rose-600',
          ]"
        >
          <component :is="tx.type === 'income' ? ArrowUpRight : ArrowDownRight" class="h-5 w-5" :stroke-width="2.2" />
        </div>

        <div class="min-w-0 flex-1">
          <p class="truncate text-sm font-semibold text-slate-900">
            {{ tx.category || 'Без категории' }}
          </p>
          <p class="truncate text-xs text-slate-400">
            {{ formatDate(tx.date) }}<template v-if="tx.note"> · {{ tx.note }}</template>
          </p>
        </div>

        <span
          :class="[
            'text-sm font-bold tabular-nums',
            tx.type === 'income' ? 'text-emerald-600' : 'text-slate-900',
          ]"
        >
          {{ tx.type === 'income' ? '+' : '−' }}{{ formatMoney(tx.amount) }}
        </span>

        <button
          class="rounded-lg p-2 text-slate-300 opacity-0 transition hover:bg-rose-50 hover:text-rose-500 group-hover:opacity-100"
          title="Удалить"
          @click="emit('delete', tx)"
        >
          <Trash2 class="h-4 w-4" />
        </button>
      </div>
    </div>
  </div>
</template>
