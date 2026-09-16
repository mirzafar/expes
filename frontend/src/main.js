import { createApp } from 'vue'
import { createPinia } from 'pinia'
import '@fontsource-variable/inter'
import '@fontsource-variable/plus-jakarta-sans'
import App from './App.vue'
import router from './router'
import './assets/main.css'
import VueApexCharts from 'vue3-apexcharts'
import { setOnAuthFailure } from '@/api/client'
import { useAuthStore } from '@/stores/auth'

async function bootstrap() {
  const app = createApp(App)
  app.use(createPinia())
  app.use(VueApexCharts)

  const auth = useAuthStore()

  // Если сессия протухла (refresh не удался) — разлогиниваем и уводим на вход
  setOnAuthFailure(() => {
    auth.logout()
    router.push({ name: 'login' })
  })

  // Восстанавливаем пользователя из сохранённого токена ДО монтирования,
  // чтобы навигационные guard'ы сразу знали статус авторизации
  await auth.init()

  app.use(router)
  app.mount('#app')
}

bootstrap()
