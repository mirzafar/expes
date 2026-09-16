<script setup>
import { CheckCircle2, XCircle, X } from 'lucide-vue-next'
import { useToastStore } from '@/stores/toast'

const toast = useToastStore()
</script>

<template>
  <Teleport to="body">
    <div class="pointer-events-none fixed right-4 top-4 z-50 flex w-full max-w-sm flex-col gap-2">
      <TransitionGroup
        enter-active-class="transition duration-300 ease-out"
        enter-from-class="translate-x-8 opacity-0"
        enter-to-class="translate-x-0 opacity-100"
        leave-active-class="transition duration-200 ease-in"
        leave-from-class="translate-x-0 opacity-100"
        leave-to-class="translate-x-8 opacity-0"
      >
        <div
          v-for="t in toast.toasts"
          :key="t.id"
          class="pointer-events-auto flex items-center gap-3 rounded-xl border border-slate-200/80 bg-white px-4 py-3 shadow-soft"
        >
          <CheckCircle2 v-if="t.type === 'success'" class="h-5 w-5 shrink-0 text-emerald-500" />
          <XCircle v-else class="h-5 w-5 shrink-0 text-rose-500" />
          <p class="flex-1 text-sm font-medium text-slate-700">{{ t.message }}</p>
          <button class="text-slate-300 hover:text-slate-500" @click="toast.remove(t.id)">
            <X class="h-4 w-4" />
          </button>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>
