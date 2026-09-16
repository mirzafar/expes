<script setup>
import { useRouter } from 'vue-router'
import { LogOut, User, Mail } from 'lucide-vue-next'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()

function logout() {
  auth.logout()
  router.push({ name: 'login' })
}
</script>

<template>
  <div class="max-w-2xl space-y-6">
    <div class="card p-6">
      <h2 class="font-display text-lg font-bold tracking-tight">Профиль</h2>
      <div class="mt-5 space-y-4">
        <div class="flex items-center gap-3">
          <div class="flex h-10 w-10 items-center justify-center rounded-xl bg-slate-100 text-slate-500">
            <User class="h-5 w-5" />
          </div>
          <div>
            <p class="text-xs text-slate-400">Имя</p>
            <p class="text-sm font-semibold text-slate-900">{{ auth.user?.name }}</p>
          </div>
        </div>
        <div class="flex items-center gap-3">
          <div class="flex h-10 w-10 items-center justify-center rounded-xl bg-slate-100 text-slate-500">
            <Mail class="h-5 w-5" />
          </div>
          <div>
            <p class="text-xs text-slate-400">Email</p>
            <p class="text-sm font-semibold text-slate-900">{{ auth.user?.email }}</p>
          </div>
        </div>
      </div>
    </div>

    <div class="card p-6">
      <h2 class="font-display text-lg font-bold tracking-tight">Сессия</h2>
      <p class="mt-1.5 text-sm text-slate-500">Выйти из аккаунта на этом устройстве.</p>
      <button class="btn mt-4 bg-rose-50 text-rose-600 hover:bg-rose-100" @click="logout">
        <LogOut class="h-4 w-4" /> Выйти
      </button>
    </div>
  </div>
</template>
