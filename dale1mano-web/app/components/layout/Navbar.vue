<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCookie, navigateTo } from '#app'

const emit = defineEmits<{
  (e: 'openLogin'): void
}>()

const route = useRoute()
const router = useRouter()
const searchText = ref((route.query.search as string) || '')
const searchTimeout = ref<number | null>(null)

const tokenCookie = useCookie('auth_token')
const adminNameCookie = useCookie('admin_name')
const adminRoleCookie = useCookie('admin_role')

// Estado para el menú móvil
const isMobileMenuOpen = ref(false)

watch(
  () => route.query.search,
  (newValue) => {
    searchText.value = typeof newValue === 'string' ? newValue : ''
  }
)

watch(searchText, (value) => {
  if (searchTimeout.value) {
    window.clearTimeout(searchTimeout.value)
  }
  searchTimeout.value = window.setTimeout(() => {
    const query = value.trim()
    const queryParams = query ? { search: query } : {}
    router.replace({ path: '/', query: queryParams })
  }, 250)
})

function onClickAdmin() {
  isMobileMenuOpen.value = false
  emit('openLogin')
}

function handleLogout() {
  const token = useCookie('auth_token')
  const adminId = useCookie('admin_id')
  const adminName = useCookie('admin_name')
  const adminRole = useCookie('admin_role')
  token.value = null
  adminId.value = null
  adminName.value = null
  adminRole.value = null
  isMobileMenuOpen.value = false
  navigateTo('/')
}

function toggleMobileMenu() {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

function closeMobileMenu() {
  isMobileMenuOpen.value = false
}
</script>

<template>
  <nav class="bg-white/75 backdrop-blur-xl border-b border-slate-100 sticky top-0 z-50 transition-all duration-300">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-20 items-center">
        
        <!-- Logo -->
        <div class="flex-shrink-0 flex items-center">
          <NuxtLink to="/" class="group flex items-center space-x-2 focus:outline-none" @click="closeMobileMenu">
            <span class="text-xl font-black tracking-tight text-slate-900 group-hover:text-[#0b31a8] transition-colors duration-300">
              Dale1Mano<span class="text-[#e0531c]">CR</span>
            </span>
          </NuxtLink>
        </div>

        <!-- Desktop Navigation Items -->
        <div class="hidden md:flex space-x-1 items-center">
          <NuxtLink 
            to="/" 
            class="px-4 py-2.5 rounded-xl text-sm font-bold text-slate-600 hover:text-[#0b31a8] hover:bg-slate-50 border-b-2 border-transparent transition-all duration-200"
            active-class="text-[#0b31a8] bg-[#0b31a8]/5 border-[#0b31a8]"
          >
            Inicio
          </NuxtLink>

          <NuxtLink 
            to="/nosotros" 
            class="px-4 py-2.5 rounded-xl text-sm font-bold text-slate-600 hover:text-[#0b31a8] hover:bg-slate-50 border-b-2 border-transparent transition-all duration-200"
            active-class="text-[#0b31a8] bg-[#0b31a8]/5 border-[#0b31a8]"
          >
            Nosotros
          </NuxtLink>

          <NuxtLink 
            to="/programas" 
            class="px-4 py-2.5 rounded-xl text-sm font-bold text-slate-600 hover:text-[#0b31a8] hover:bg-slate-50 border-b-2 border-transparent transition-all duration-200"
            active-class="text-[#0b31a8] bg-[#0b31a8]/5 border-[#0b31a8]"
          >
            Programas
          </NuxtLink>

          <NuxtLink 
            to="/proyectos" 
            class="px-4 py-2.5 rounded-xl text-sm font-bold text-slate-600 hover:text-[#0b31a8] hover:bg-slate-50 border-b-2 border-transparent transition-all duration-200"
            active-class="text-[#0b31a8] bg-[#0b31a8]/5 border-[#0b31a8]"
          >
            Proyectos
          </NuxtLink>

          <NuxtLink 
            to="/unete" 
            class="ml-4 inline-flex items-center justify-center px-5 py-2.5 rounded-xl text-sm font-bold text-white bg-gradient-to-r from-[#e0531c] to-[#f06732] hover:from-[#f06732] hover:to-[#e0531c] shadow-md shadow-orange-500/10 hover:shadow-orange-500/20 hover:scale-[1.02] active:scale-[0.98] transition-all duration-200"
          >
            Únete
          </NuxtLink>
				
          <!-- Sesión / Admin (Desktop) -->
          <template v-if="tokenCookie">
            <span class="text-xs font-bold text-slate-700 ml-4 hidden lg:inline">
              Hola, <span class="text-[#e0531c] font-black">{{ adminNameCookie }}</span>
            </span>

            <NuxtLink 
              v-if="adminRoleCookie === 'ADMIN'"
              to="/admin" 
              class="ml-4 inline-flex items-center justify-center px-4 py-2.5 rounded-xl text-xs font-black text-white bg-gradient-to-r from-[#0b31a8] to-indigo-700 hover:from-blue-800 hover:to-indigo-800 transition-all duration-200 shadow-md shadow-blue-500/10 hover:scale-[1.02]"
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-3.5 h-3.5 mr-1 text-orange-400">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L12 14.25L15 12.75M21 12c0 1.268-.63 2.39-1.593 3.068a3.745 3.745 0 01-1.043 3.296 3.745 3.745 0 01-3.296 1.043A3.745 3.745 0 0112 21c-1.268 0-2.39-.63-3.068-1.593a3.746 3.746 0 01-3.296-1.043 3.745 3.745 0 01-1.043-3.296A3.745 3.745 0 0121 12z" />
              </svg>
              Panel Admin
            </NuxtLink>

            <button 
              @click="handleLogout"
              class="ml-3 inline-flex items-center justify-center px-4 py-2.5 rounded-xl text-xs font-bold text-[#e0531c] border border-orange-200 hover:bg-orange-50 transition-all duration-200 cursor-pointer"
            >
              Salir
            </button>
          </template>

          <button 
            v-else
            class="ml-4 inline-flex items-center justify-center px-5 py-2.5 rounded-xl text-sm font-bold text-white bg-gradient-to-r from-[#0b31a8] to-[#1e3a8a] hover:from-[#1e3a8a] hover:to-[#0b31a8] shadow-md shadow-blue-500/10 hover:shadow-blue-500/20 hover:scale-[1.02] active:scale-[0.98] transition-all duration-200 cursor-pointer" 
            @click="onClickAdmin"
          >
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" class="mr-1.5">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
            </svg>
            Ingresar
          </button>
        </div>

        <!-- Mobile Hamburguer Button -->
        <div class="flex items-center md:hidden">
          <button 
            @click="toggleMobileMenu" 
            class="p-2 rounded-xl text-slate-600 hover:bg-slate-50 focus:outline-none transition-colors"
            aria-label="Toggle menu"
          >
            <svg v-if="!isMobileMenuOpen" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
      </div>
    </div>

    <!-- Mobile Dropdown Menu -->
    <transition name="slide-down">
      <div 
        v-if="isMobileMenuOpen" 
        class="md:hidden border-t border-slate-100 bg-white shadow-lg overflow-hidden py-4 px-6 space-y-3 flex flex-col text-left"
      >
        <NuxtLink 
          to="/" 
          class="py-2.5 text-sm font-semibold text-slate-600 hover:text-[#0b31a8] transition-colors"
          active-class="text-[#0b31a8]"
          @click="closeMobileMenu"
        >
          Inicio
        </NuxtLink>

        <NuxtLink 
          to="/nosotros" 
          class="py-2.5 text-sm font-semibold text-slate-600 hover:text-[#0b31a8] transition-colors"
          active-class="text-[#0b31a8]"
          @click="closeMobileMenu"
        >
          Nosotros
        </NuxtLink>

        <NuxtLink 
          to="/programas" 
          class="py-2.5 text-sm font-semibold text-slate-600 hover:text-[#0b31a8] transition-colors"
          active-class="text-[#0b31a8]"
          @click="closeMobileMenu"
        >
          Programas
        </NuxtLink>

        <NuxtLink 
          to="/proyectos" 
          class="py-2.5 text-sm font-semibold text-slate-600 hover:text-[#0b31a8] transition-colors"
          active-class="text-[#0b31a8]"
          @click="closeMobileMenu"
        >
          Proyectos
        </NuxtLink>

        <NuxtLink 
          to="/unete" 
          class="py-2.5 text-sm font-semibold text-slate-600 hover:text-[#e0531c] transition-colors"
          active-class="text-[#e0531c]"
          @click="closeMobileMenu"
        >
          Únete
        </NuxtLink>

        <div class="border-t border-slate-100 my-2 pt-3 flex flex-col space-y-3">
          <template v-if="tokenCookie">
            <span class="text-xs font-bold text-slate-700">
              Sesión: <span class="text-[#e0531c] font-black">{{ adminNameCookie }}</span>
            </span>

            <NuxtLink 
              v-if="adminRoleCookie === 'ADMIN'"
              to="/admin" 
              class="w-full inline-flex items-center justify-center py-2.5 rounded-xl text-xs font-black text-white bg-gradient-to-r from-[#0b31a8] to-indigo-700"
              @click="closeMobileMenu"
            >
              Panel Admin
            </NuxtLink>

            <button 
              @click="handleLogout"
              class="w-full inline-flex items-center justify-center py-2.5 rounded-xl text-xs font-bold text-[#e0531c] border border-orange-200 hover:bg-orange-50 transition-all duration-200"
            >
              Cerrar Sesión
            </button>
          </template>

          <button 
            v-else
            class="w-full inline-flex items-center justify-center py-3 rounded-xl text-xs font-bold text-white bg-gradient-to-r from-[#0b31a8] to-[#1e3a8a]" 
            @click="onClickAdmin"
          >
            Ingresar al Sistema
          </button>
        </div>
      </div>
    </transition>
  </nav>
</template>

<style scoped>
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s ease-out;
  max-height: 400px;
}
.slide-down-enter-from,
.slide-down-leave-to {
  opacity: 0;
  max-height: 0px;
  transform: translateY(-10px);
}
</style>