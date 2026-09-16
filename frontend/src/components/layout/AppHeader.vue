<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Plus, ChevronDown, LogOut } from 'lucide-vue-next'
import { useAuthStore } from '@/stores/auth'
import { useUiStore } from '@/stores/ui'

defineProps({
  title: { type: String, default: '' },
})

const auth = useAuthStore()
const ui = useUiStore()
const router = useRouter()
const menuOpen = ref(false)

function initials(name) {
  return (name || '?')
    .split(' ')
    .map((w) => w[0])
    .slice(0, 2)
    .join('')
    .toUpperCase()
}

function logout() {
  auth.logout()
  router.push({ name: 'login' })
}
</script>

<template>
  <header class="flex h-16 items-center gap-4 border-b border-slate-200/80 bg-white/80 px-6 backdrop-blur">
    <h1 class="font-display text-xl font-bold tracking-tight text-slate-900">{{ title }}</h1>

    <div class="ml-auto flex items-center gap-2">
      <!-- Добавить -->
      <button class="btn-primary" @click="ui.openAdd('expense')">
        <Plus class="h-4 w-4" :stroke-width="2.4" />
        <span class="hidden sm:inline">Добавить</span>
      </button>

      <!-- Меню пользователя -->
      <div class="relative">
        <button
          class="flex items-center gap-2 rounded-xl p-1.5 hover:bg-slate-100"
          @click="menuOpen = !menuOpen"
        >
          <div class="flex h-8 w-8 items-center justify-center rounded-full bg-slate-200 text-xs font-semibold text-slate-700">
            {{ initials(auth.user?.name) }}
          </div>
          <ChevronDown class="h-4 w-4 text-slate-400" />
        </button>

        <!-- Выпадающее меню -->
        <div
          v-if="menuOpen"
          class="absolute right-0 top-12 z-20 w-52 overflow-hidden rounded-2xl border border-slate-200/80 bg-white py-1.5 shadow-lg"
          @click="menuOpen = false"
        >
          <div class="border-b border-slate-100 px-4 py-2.5">
            <p class="truncate text-sm font-semibold">{{ auth.user?.name }}</p>
            <p class="truncate text-xs text-slate-400">{{ auth.user?.email }}</p>
          </div>
          <button
            class="flex w-full items-center gap-2.5 px-4 py-2.5 text-sm text-slate-600 hover:bg-slate-50"
            @click="logout"
          >
            <LogOut class="h-4 w-4" />
            Выйти
          </button>
        </div>
      </div>
    </div>

    <!-- Клик вне меню закрывает его -->
    <div v-if="menuOpen" class="fixed inset-0 z-10" @click="menuOpen = false"></div>
  </header>
</template>
