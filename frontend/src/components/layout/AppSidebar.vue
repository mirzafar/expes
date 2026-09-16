<script setup>
import { RouterLink } from 'vue-router'
import {
  LayoutDashboard,
  TrendingUp,
  TrendingDown,
  ChartPie,
  Tags,
  Settings,
  Wallet,
} from 'lucide-vue-next'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()

const nav = [
  { to: '/', label: 'Обзор', icon: LayoutDashboard, exact: true },
  { to: '/income', label: 'Доходы', icon: TrendingUp },
  { to: '/expenses', label: 'Расходы', icon: TrendingDown },
  { to: '/analytics', label: 'Аналитика', icon: ChartPie },
  { to: '/categories', label: 'Категории', icon: Tags },
]
const bottomNav = [{ to: '/settings', label: 'Настройки', icon: Settings }]

function initials(name) {
  return (name || '?')
    .split(' ')
    .map((w) => w[0])
    .slice(0, 2)
    .join('')
    .toUpperCase()
}
</script>

<template>
  <aside class="flex h-full w-64 flex-col border-r border-slate-200/80 bg-white">
    <!-- Логотип -->
    <div class="flex items-center gap-2.5 px-5 h-16 border-b border-slate-200/70">
      <div class="flex h-9 w-9 items-center justify-center rounded-xl bg-indigo-600 text-white">
        <Wallet class="h-5 w-5" :stroke-width="2.2" />
      </div>
      <span class="font-display text-lg font-bold tracking-tight">Expes</span>
    </div>

    <!-- Навигация -->
    <nav class="flex-1 px-3 py-4 space-y-1">
      <p class="px-3 pb-2 text-xs font-semibold uppercase tracking-wider text-slate-400">
        Меню
      </p>
      <RouterLink
        v-for="item in nav"
        :key="item.to"
        :to="item.to"
        :class="[
          'group flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-colors',
          ($route.path === item.to || (!item.exact && $route.path.startsWith(item.to)))
            ? 'bg-indigo-50 text-indigo-700'
            : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900',
        ]"
      >
        <component :is="item.icon" class="h-5 w-5" :stroke-width="2" />
        {{ item.label }}
      </RouterLink>
    </nav>

    <!-- Нижняя навигация -->
    <div class="px-3 pb-2 space-y-1 border-t border-slate-200/70 pt-3">
      <RouterLink
        v-for="item in bottomNav"
        :key="item.to"
        :to="item.to"
        :class="[
          'flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-colors',
          $route.path.startsWith(item.to)
            ? 'bg-indigo-50 text-indigo-700'
            : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900',
        ]"
      >
        <component :is="item.icon" class="h-5 w-5" :stroke-width="2" />
        {{ item.label }}
      </RouterLink>
    </div>

    <!-- Пользователь -->
    <div class="flex items-center gap-3 border-t border-slate-200/70 px-4 py-3.5">
      <div class="flex h-9 w-9 items-center justify-center rounded-full bg-slate-200 text-sm font-semibold text-slate-700">
        {{ initials(auth.user?.name) }}
      </div>
      <div class="min-w-0 flex-1">
        <p class="truncate text-sm font-semibold text-slate-900">{{ auth.user?.name }}</p>
        <p class="truncate text-xs text-slate-400">{{ auth.user?.email }}</p>
      </div>
    </div>
  </aside>
</template>
