<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from '#app'

const router = useRouter()
const config = useRuntimeConfig()

const nombre = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const isLoading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

async function handleRegister() {
  errorMessage.value = ''
  successMessage.value = ''

  if (!nombre.value || !email.value || !password.value || !confirmPassword.value) {
    errorMessage.value = 'Por favor, completa todos los campos.'
    return
  }

  const nameRegex = /^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$/
  if (!nameRegex.test(nombre.value.trim())) {
    errorMessage.value = 'El nombre completo solo debe contener letras y espacios.'
    return
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(email.value.trim())) {
    errorMessage.value = 'Por favor, ingresa un correo electrónico válido.'
    return
  }

  if (password.value !== confirmPassword.value) {
    errorMessage.value = 'Las contraseñas no coinciden.'
    return
  }

  if (password.value.length < 6) {
    errorMessage.value = 'La contraseña debe tener al menos 6 caracteres.'
    return
  }

  try {
    isLoading.value = true
    const url = `${config.public.apiBase}/auth/registro`
    
    await $fetch<any>(url, {
      method: 'POST',
      body: {
        nombre: nombre.value.trim(),
        email: email.value.trim(),
        password: password.value
      }
    })

    successMessage.value = '¡Usuario registrado exitosamente! Redirigiéndote al inicio...'
    
    // Limpiar formulario
    nombre.value = ''
    email.value = ''
    password.value = ''
    confirmPassword.value = ''

    setTimeout(() => {
      router.push('/')
    }, 2000)

  } catch (error: any) {
    errorMessage.value = error.data?.error || 'Ocurrió un error al registrar el usuario.'
    console.error('Error de registro:', error)
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-slate-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8 bg-white p-8 rounded-2xl shadow-xl border border-slate-100">
      <div class="text-center">
        <h2 class="mt-6 text-3xl font-black text-slate-900 tracking-tight">
          Únete a Dale 1 Mano
        </h2>
        <p class="mt-2 text-sm text-slate-500 font-medium">
          Crea tu cuenta y forma parte del voluntariado hoy mismo
        </p>
      </div>

      <!-- Alertas -->
      <div class="space-y-3">
        <div v-if="errorMessage" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl text-xs font-bold flex items-center space-x-2">
          <span>⚠️</span>
          <span class="flex-1 leading-normal">{{ errorMessage }}</span>
        </div>
        <div v-if="successMessage" class="bg-emerald-50 border border-emerald-200 text-emerald-700 px-4 py-3 rounded-xl text-xs font-bold flex items-center space-x-2">
          <span>✅</span>
          <span class="flex-1 leading-normal">{{ successMessage }}</span>
        </div>
      </div>

      <form class="mt-8 space-y-4" @submit.prevent="handleRegister">
        <div class="space-y-1">
          <label for="reg-nombre" class="block text-xs font-bold uppercase tracking-wider text-slate-500">
            Nombre Completo
          </label>
          <input
            id="reg-nombre"
            v-model="nombre"
            type="text"
            required
            placeholder="Juan Pérez"
            :disabled="isLoading"
            class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm text-slate-800 focus:outline-none focus:border-[#0b31a8] focus:bg-white disabled:opacity-50 transition-all font-medium"
          />
        </div>

        <div class="space-y-1">
          <label for="reg-email" class="block text-xs font-bold uppercase tracking-wider text-slate-500">
            Correo Electrónico
          </label>
          <input
            id="reg-email"
            v-model="email"
            type="email"
            required
            placeholder="juan@correo.com"
            :disabled="isLoading"
            class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm text-slate-800 focus:outline-none focus:border-[#0b31a8] focus:bg-white disabled:opacity-50 transition-all font-medium"
          />
        </div>

        <div class="space-y-1">
          <label for="reg-password" class="block text-xs font-bold uppercase tracking-wider text-slate-500">
            Contraseña
          </label>
          <input
            id="reg-password"
            v-model="password"
            type="password"
            required
            placeholder="••••••••"
            :disabled="isLoading"
            class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm text-slate-800 focus:outline-none focus:border-[#0b31a8] focus:bg-white disabled:opacity-50 transition-all font-medium"
          />
        </div>

        <div class="space-y-1">
          <label for="reg-confirm-password" class="block text-xs font-bold uppercase tracking-wider text-slate-500">
            Confirmar Contraseña
          </label>
          <input
            id="reg-confirm-password"
            v-model="confirmPassword"
            type="password"
            required
            placeholder="••••••••"
            :disabled="isLoading"
            class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm text-slate-800 focus:outline-none focus:border-[#0b31a8] focus:bg-white disabled:opacity-50 transition-all font-medium"
          />
        </div>

        <div class="pt-4 space-y-3">
          <button
            type="submit"
            :disabled="isLoading"
            class="w-full bg-[#0b31a8] hover:bg-[#09278a] text-white font-bold py-3 px-4 rounded-xl text-sm tracking-wide shadow-md shadow-blue-900/10 hover:shadow-lg disabled:opacity-60 transition-all flex items-center justify-center space-x-2"
          >
            <span v-if="isLoading" class="flex items-center space-x-2">
              <svg class="animate-spin h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span>Registrando...</span>
            </span>
            <span v-else>Crear cuenta</span>
          </button>

          <div class="text-center pt-2 text-xs font-medium text-slate-500">
            ¿Ya tienes una cuenta?
            <button 
              type="button" 
              @click="navigateTo('/?login=true')" 
              class="text-[#e0531c] hover:underline font-bold ml-1 cursor-pointer bg-transparent border-none focus:outline-none"
            >
              Inicia sesión aquí
            </button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>