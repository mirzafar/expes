<script setup>
import { RouterLink } from 'vue-router'
import { LayoutDashboard, TrendingUp, Plus, TrendingDown, ChartPie, Tags } from 'lucide-vue-next'
import { useUiStore } from '@/stores/ui'

const ui = useUiStore()

const nav = [
  { to: '/', label: 'Обзор', icon: LayoutDashboard, exact: true },
  { to: '/income', label: 'Доходы', icon: TrendingUp },
  { to: '/expenses', label: 'Расходы', icon: TrendingDown },
  { to: '/analytics', label: 'Анализ', icon: ChartPie },
  { to: '/categories', label: 'Категории', icon: Tags },
]
</script>

<template>
  <nav class="fixed inset-x-0 bottom-0 z-30 flex items-center justify-around border-t border-slate-200 bg-white/90 px-2 pb-[env(safe-area-inset-bottom)] backdrop-blur lg:hidden">
    <template v-for="(item, i) in nav" :key="item.to">
      <!-- Центральная кнопка добавления -->
      <button
        v-if="i === 2"
        class="-mt-5 flex h-12 w-12 items-center justify-center rounded-full bg-indigo-600 text-white shadow-lg shadow-indigo-600/30"
        @click="ui.openAdd('expense')"
      >
        <Plus class="h-6 w-6" :stroke-width="2.4" />
      </button>

      <RouterLink
        :to="item.to"
        :class="[
          'flex flex-1 flex-col items-center gap-0.5 py-2.5 text-[11px] font-medium whitespace-nowrap',
          ($route.path === item.to || (!item.exact && $route.path.startsWith(item.to)))
            ? 'text-indigo-600'
            : 'text-slate-400',
        ]"
      >
        <component :is="item.icon" class="h-5 w-5" :stroke-width="2" />
        {{ item.label }}
      </RouterLink>
    </template>
  </nav>
</template>
