<template>
  <div class="min-h-screen flex flex-col bg-gray-50 text-gray-800">
    <LayoutNavbar @openLogin="handleOpenLogin" />

    <main class="flex-grow">
      <slot />
    </main>

    <LayoutFooter />
    
    <LoginModal 
      :isOpen="isLoginModalOpen" 
      @close="isLoginModalOpen = false" 
      @loginSuccess="handleLoginSuccess"
    />

    <!-- TOAST NOTIFICATIONS (Premium glassmorphism con acento lateral) -->
    <div class="fixed top-6 right-6 z-[9999] flex flex-col space-y-3 max-w-sm w-full">
      <transition-group name="toast">
        <div
          v-for="toast in toasts"
          :key="toast.id"
          class="p-4 rounded-xl border flex items-start space-x-3 shadow-xl backdrop-blur-md transition-all duration-300 border-l-4"
          :class="[
            toast.type === 'success' ? 'bg-emerald-50/95 border-emerald-100 border-l-emerald-500 text-emerald-900' :
            toast.type === 'error'   ? 'bg-rose-50/95 border-rose-100 border-l-rose-500 text-rose-900' :
            toast.type === 'warning' ? 'bg-amber-50/95 border-amber-100 border-l-amber-500 text-amber-900' :
            'bg-blue-50/95 border-blue-100 border-l-blue-500 text-blue-900'
          ]"
        >
          <div class="flex-shrink-0 mt-0.5">
            <svg v-if="toast.type === 'success'" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-5 h-5 text-emerald-600">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <svg v-else-if="toast.type === 'error'" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-5 h-5 text-rose-600">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <svg v-else-if="toast.type === 'warning'" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-5 h-5 text-amber-600">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-5 h-5 text-blue-600">
              <path stroke-linecap="round" stroke-linejoin="round" d="M11.25 11.25l.041-.02a.75.75 0 111.063.852l-.708 2.836a.75.75 0 001.063.852l.041-.028M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div class="flex-1 text-xs font-bold leading-relaxed">{{ toast.message }}</div>
        </div>
      </transition-group>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useAdminData } from '../composables/useAdminData'
import { navigateTo, useRoute } from '#app'

// Estado para controlar la apertura del modal
const isLoginModalOpen = ref(false)
const { toasts } = useAdminData()
const route = useRoute()

// Observar el query parameter para abrir el modal de login
watch(
  () => route.query.login,
  (newVal) => {
    if (newVal === 'true') {
      isLoginModalOpen.value = true
    }
  },
  { immediate: true }
)

function handleLoginSuccess(adminData: { adminId: number; nombre: string; rol: string }) {
  isLoginModalOpen.value = false
  
  if (adminData.rol === 'ADMIN') {
    navigateTo('/admin') 
  } else {
    navigateTo('/')
  }
}

function handleOpenLogin() {
  console.log('Layout: openLogin event received. Opening modal...')
  isLoginModalOpen.value = true
}
</script>

<style>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}
.toast-enter-from {
  opacity: 0;
  transform: translateX(80px) scale(0.95);
}
.toast-leave-to {
  opacity: 0;
  transform: translateX(120px);
}
</style>
