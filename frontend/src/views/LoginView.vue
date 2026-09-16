<script setup>
import { ref } from 'vue'
import { useRouter, useRoute, RouterLink } from 'vue-router'
import { Wallet, TrendingUp, PieChart, ShieldCheck } from 'lucide-vue-next'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()

const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function onSubmit() {
  error.value = ''
  loading.value = true
  try {
    await auth.login({ email: email.value, password: password.value })
    router.push(route.query.redirect || { name: 'overview' })
  } catch (e) {
    error.value = e.response?.data?.detail || 'Не удалось войти. Проверьте email и пароль.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="flex min-h-screen">
    <!-- Левая брендовая панель -->
    <div class="relative hidden w-1/2 flex-col justify-between overflow-hidden bg-indigo-600 p-12 text-white lg:flex">
      <div class="absolute -right-24 -top-24 h-96 w-96 rounded-full bg-indigo-500/40 blur-3xl"></div>
      <div class="absolute -bottom-32 -left-16 h-96 w-96 rounded-full bg-violet-500/30 blur-3xl"></div>

      <div class="relative flex items-center gap-2.5">
        <div class="flex h-10 w-10 items-center justify-center rounded-xl bg-white/15 backdrop-blur">
          <Wallet class="h-6 w-6" />
        </div>
        <span class="font-display text-xl font-bold">Expes</span>
      </div>

      <div class="relative">
        <h2 class="font-display text-4xl font-bold leading-tight tracking-tight">
          Держите финансы<br />под контролем
        </h2>
        <p class="mt-4 max-w-md text-indigo-100">
          Учитывайте доходы и расходы, следите за балансом и анализируйте траты — всё в одном месте.
        </p>
        <div class="mt-10 space-y-4">
          <div class="flex items-center gap-3 text-indigo-50">
            <div class="flex h-9 w-9 items-center justify-center rounded-lg bg-white/15"><TrendingUp class="h-5 w-5" /></div>
            Наглядный баланс и статистика
          </div>
          <div class="flex items-center gap-3 text-indigo-50">
            <div class="flex h-9 w-9 items-center justify-center rounded-lg bg-white/15"><PieChart class="h-5 w-5" /></div>
            Аналитика по категориям
          </div>
          <div class="flex items-center gap-3 text-indigo-50">
            <div class="flex h-9 w-9 items-center justify-center rounded-lg bg-white/15"><ShieldCheck class="h-5 w-5" /></div>
            Ваши данные под защитой
          </div>
        </div>
      </div>

      <p class="relative text-sm text-indigo-200">© 2026 Expes</p>
    </div>

    <!-- Правая форма -->
    <div class="flex w-full items-center justify-center px-6 py-12 lg:w-1/2">
      <div class="w-full max-w-sm">
        <div class="mb-8">
          <h1 class="font-display text-2xl font-bold tracking-tight">С возвращением 👋</h1>
          <p class="mt-1.5 text-sm text-slate-500">Войдите в свой аккаунт, чтобы продолжить</p>
        </div>

        <form class="space-y-4" @submit.prevent="onSubmit">
          <div>
            <label class="label">Email</label>
            <input v-model="email" type="email" class="input" required autocomplete="email" placeholder="you@example.com" />
          </div>
          <div>
            <label class="label">Пароль</label>
            <input v-model="password" type="password" class="input" required autocomplete="current-password" placeholder="••••••••" />
          </div>

          <p v-if="error" class="rounded-xl bg-red-50 px-3.5 py-2.5 text-sm text-red-600">{{ error }}</p>

          <button class="btn-primary w-full" type="submit" :disabled="loading">
            {{ loading ? 'Входим…' : 'Войти' }}
          </button>
        </form>

        <p class="mt-6 text-center text-sm text-slate-500">
          Нет аккаунта?
          <RouterLink to="/register" class="font-semibold text-indigo-600 hover:text-indigo-700">Зарегистрироваться</RouterLink>
        </p>
      </div>
    </div>
  </div>
</template>
