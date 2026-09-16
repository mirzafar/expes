import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import AppLayout from '@/layouts/AppLayout.vue'

const routes = [
  // Страницы приложения — внутри общей оболочки
  {
    path: '/',
    component: AppLayout,
    meta: { requiresAuth: true },
    children: [
      { path: '', name: 'overview', component: () => import('@/views/OverviewView.vue'), meta: { title: 'Обзор' } },
      { path: 'income', name: 'income', component: () => import('@/views/IncomeView.vue'), meta: { title: 'Доходы' } },
      { path: 'expenses', name: 'expenses', component: () => import('@/views/ExpensesView.vue'), meta: { title: 'Расходы' } },
      { path: 'analytics', name: 'analytics', component: () => import('@/views/AnalyticsView.vue'), meta: { title: 'Аналитика' } },
      { path: 'categories', name: 'categories', component: () => import('@/views/CategoriesView.vue'), meta: { title: 'Категории' } },
      { path: 'settings', name: 'settings', component: () => import('@/views/SettingsView.vue'), meta: { title: 'Настройки' } },
    ],
  },
  // Авторизация — без оболочки, на весь экран
  { path: '/login', name: 'login', component: () => import('@/views/LoginView.vue'), meta: { guestOnly: true } },
  { path: '/register', name: 'register', component: () => import('@/views/RegisterView.vue'), meta: { guestOnly: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }
  if (to.meta.guestOnly && auth.isAuthenticated) {
    return { name: 'overview' }
  }
})

export default router
