<script setup>
import { computed } from 'vue'
import { useRoute, RouterView } from 'vue-router'
import AppSidebar from '@/components/layout/AppSidebar.vue'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppMobileNav from '@/components/layout/AppMobileNav.vue'
import AddTransactionModal from '@/components/AddTransactionModal.vue'
import Toaster from '@/components/ui/Toaster.vue'

const route = useRoute()
const title = computed(() => route.meta.title || '')
</script>

<template>
  <div class="flex h-screen overflow-hidden bg-slate-50">
    <!-- Sidebar (скрывается на мобильных) -->
    <div class="hidden lg:block">
      <AppSidebar />
    </div>

    <!-- Основная область -->
    <div class="flex min-w-0 flex-1 flex-col">
      <AppHeader :title="title" />
      <main class="flex-1 overflow-y-auto px-4 py-6 pb-24 sm:px-6 lg:pb-6">
        <div class="mx-auto max-w-6xl">
          <RouterView />
        </div>
      </main>
    </div>

    <!-- Мобильная навигация -->
    <AppMobileNav />

    <!-- Глобальные оверлеи -->
    <AddTransactionModal />
    <Toaster />
  </div>
</template>
