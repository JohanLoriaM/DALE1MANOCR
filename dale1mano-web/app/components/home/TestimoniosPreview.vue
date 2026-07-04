<template>
  <section class="py-20 bg-slate-50 text-slate-800">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <div class="text-center max-w-3xl mx-auto mb-16 space-y-3 relative">
        <h2 class="text-3xl font-black text-slate-900 sm:text-4xl tracking-tight uppercase">
          Testimonios
        </h2>
        <div class="w-24 h-1 bg-orange-500 mx-auto rounded-full"></div>
        
        <!-- Botón para compartir testimonio -->
        <div class="pt-6">
          <button 
            @click="abrirCompartirModal"
            class="inline-flex items-center justify-center space-x-2 px-5 py-2.5 rounded-xl text-white text-xs font-black bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-650 hover:to-amber-650 transition-all duration-300 shadow-md shadow-orange-500/10 hover:shadow-lg hover:scale-[1.02] active:scale-[0.98] cursor-pointer uppercase tracking-wider"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-4 h-4">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
            </svg>
            <span>Compartir mi Testimonio</span>
          </button>
        </div>
      </div>

      <div class="grid grid-cols-1 xl:grid-cols-2 gap-8">
        <div 
          v-for="(video, index) in videos" 
          :key="index" 
          class="flex flex-col md:flex-row bg-white rounded-2xl overflow-hidden shadow-sm border border-slate-200/60 hover:shadow-md transition-all duration-300"
        >
          <!-- Left side: YouTube Video or stylized Profile Card -->
          <div class="w-full md:w-[50%] aspect-video md:aspect-auto md:min-h-[220px] bg-black relative flex items-center justify-center group overflow-hidden">
            
            <!-- If YouTube video exists -->
            <template v-if="video.youtubeId">
              <template v-if="videoActivo !== index">
                <img 
                  :src="`https://img.youtube.com/vi/${video.youtubeId}/maxresdefault.jpg`" 
                  :alt="video.titulo"
                  class="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                  @error="manejarErrorMiniatura"
                />
                <div class="absolute inset-0 bg-slate-900/20 group-hover:bg-slate-900/40 transition-colors duration-300"></div>
                
                <button 
                  @click="videoActivo = index"
                  class="absolute z-10 flex items-center justify-center w-14 h-14 bg-[#e0531c] text-white rounded-full shadow-lg transform group-hover:scale-110 transition-all duration-300 cursor-pointer"
                  aria-label="Reproducir video"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-6 h-6 ml-0.5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M5.25 5.653c0-.856.917-1.398 1.667-.986l11.54 6.348a1.125 1.125 0 010 1.971l-11.54 6.347a1.125 1.125 0 01-1.667-.985V5.653z" />
                  </svg>
                </button>
              </template>

              <iframe 
                v-else
                class="absolute top-0 left-0 w-full h-full" 
                :src="`https://www.youtube.com/embed/${video.youtubeId}?autoplay=1`" 
                title="YouTube video player" 
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                allowfullscreen
              ></iframe>
            </template>

            <!-- If NO YouTube video (styled glassmorphism / volunteer profile card) -->
            <div v-else class="absolute inset-0 w-full h-full bg-gradient-to-br from-[#0b31a8] to-[#1e3a8a] flex flex-col items-center justify-center p-6 text-white space-y-3">
              <div class="w-16 h-16 rounded-full bg-white/10 backdrop-blur-md border border-white/20 flex items-center justify-center font-black text-2xl shadow-inner">
                {{ video.inicial }}
              </div>
              <div class="text-center">
                <p class="font-bold text-sm tracking-wide">{{ video.autor }}</p>
                <p class="text-[10px] text-orange-300 font-bold uppercase tracking-wider mt-0.5">Voluntario Activo</p>
              </div>
              <!-- Quote decorative icon -->
              <span class="absolute bottom-2 right-4 text-5xl font-serif text-white/5 select-none">“</span>
            </div>
          </div>

          <!-- Right side: Content -->
          <div class="w-full md:w-[50%] p-6 flex flex-col justify-between space-y-4 text-left">
            <div class="space-y-2">
              <h3 class="text-lg font-bold text-slate-900 leading-snug line-clamp-2">
                {{ video.titulo }}
              </h3>
              <div class="w-8 h-0.5 bg-orange-400 rounded-full"></div>
            </div>

            <div class="flex-grow flex flex-col justify-start">
              <span class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-1">
                Testimonio
              </span>
              <p class="text-sm text-slate-600 leading-relaxed line-clamp-5 italic">
                "{{ video.descripcion }}"
              </p>
            </div>
          </div>
        </div>
      </div>

    </div>

    <!-- MODAL: ENVIAR TESTIMONIO -->
    <transition name="fade">
      <div 
        v-if="isModalOpen" 
        class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm"
      >
        <div class="bg-white rounded-2xl shadow-2xl max-w-lg w-full overflow-hidden border border-slate-100 transform transition-all duration-300 p-8 space-y-6 text-left relative">
          <button 
            @click="isModalOpen = false" 
            class="absolute top-4 right-4 text-slate-400 hover:text-slate-600 text-2xl font-bold transition-colors cursor-pointer"
          >
            &times;
          </button>

          <div class="space-y-1">
            <h3 class="text-xl font-black text-slate-900">Comparte tu Testimonio</h3>
            <p class="text-xs font-medium text-slate-500">Cuéntale a la comunidad sobre tu experiencia de voluntariado.</p>
          </div>

          <form @submit.prevent="enviarTestimonio" class="space-y-4">
            <!-- Selección de Proyecto -->
            <div class="space-y-1">
              <label class="block text-xs font-bold uppercase tracking-wider text-slate-500">¿En qué proyecto participaste?</label>
              <select 
                v-model="form.id_proyecto" 
                required 
                class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 focus:outline-none focus:border-[#0b31a8] focus:bg-white transition-all cursor-pointer font-medium"
              >
                <option :value="null" disabled>-- Selecciona un Proyecto --</option>
                <option 
                  v-for="proj in activeOrPassedProjects" 
                  :key="proj.id_proyecto" 
                  :value="proj.id_proyecto"
                >
                  {{ proj.titulo }}
                </option>
              </select>
            </div>

            <!-- Contenido -->
            <div class="space-y-1">
              <label class="block text-xs font-bold uppercase tracking-wider text-slate-500">Tu Testimonio</label>
              <textarea 
                v-model="form.contenido" 
                rows="4" 
                required 
                placeholder="Escribe aquí tu experiencia, aprendizajes y lo que significó para ti..."
                class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-[#0b31a8] focus:bg-white transition-all font-medium"
              ></textarea>
            </div>

            <!-- YouTube Video Link -->
            <div class="space-y-1">
              <label class="block text-xs font-bold uppercase tracking-wider text-slate-500">Video Adjunto (Opcional - Enlace de YouTube)</label>
              <input 
                v-model="form.url_video" 
                type="url" 
                placeholder="Ej: https://www.youtube.com/watch?v=..."
                class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-[#0b31a8] focus:bg-white transition-all font-medium"
              />
            </div>

            <div class="pt-4 flex justify-end space-x-2 border-t border-slate-100">
              <button 
                type="button" 
                @click="isModalOpen = false" 
                class="px-4 py-2 border border-slate-200 rounded-xl text-xs font-bold text-slate-500 hover:bg-slate-50 transition-colors cursor-pointer"
              >
                Cancelar
              </button>
              <button 
                type="submit" 
                :disabled="isSubmitting"
                class="px-5 py-2 text-white text-xs font-black rounded-xl shadow-xs bg-[#0b31a8] hover:bg-blue-800 transition-all cursor-pointer"
              >
                <span v-if="isSubmitting">Enviando...</span>
                <span v-else>Enviar Testimonio</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </transition>
  </section>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'
import { useCookie, useRuntimeConfig } from '#app'
import { useAdminData, addToast } from '~/composables/useAdminData'

const { testimonials, projects, users, loadRealData } = useAdminData()
const config = useRuntimeConfig()

// Cookies de sesión
const tokenCookie = useCookie('auth_token')
const adminIdCookie = useCookie('admin_id')

// Estado para reproducir video
const videoActivo = ref(null)

// Estado del Modal
const isModalOpen = ref(false)
const isSubmitting = ref(false)
const form = reactive({
  id_proyecto: null,
  contenido: '',
  url_video: ''
})

// Filtrar proyectos activos o pasados
const activeOrPassedProjects = computed(() => {
  return projects.value.filter(p => p.estado === 'ACTIVO' || p.estado === 'PASADO')
})

// Cargar testimonios dinámicamente (todos los aprobados, tengan o no video)
const videos = computed(() => {
  return testimonials.value
    .filter(t => t.aprobado)
    .map(t => {
      let youtubeId = null
      if (t.url_video) {
        const match = t.url_video.match(/(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})/)
        if (match) {
          youtubeId = match[1]
        }
      }

      const proj = projects.value.find(p => p.id_proyecto === t.id_proyecto)
      const projTitle = proj ? proj.titulo : 'Proyecto Dale1Mano'

      const u = users.value.find(usr => usr.id_usuario === t.id_usuario)
      const autor = u ? u.nombre_completo : 'Voluntario'
      const inicial = autor.charAt(0).toUpperCase()

      return {
        titulo: `${projTitle} - Testimonio`,
        youtubeId: youtubeId,
        descripcion: t.contenido,
        autor: autor,
        inicial: inicial
      }
    })
})

function abrirCompartirModal() {
  if (!tokenCookie.value) {
    alert('Por favor, inicia sesión para poder compartir tu testimonio. Haz clic en "Ingresar" en la barra de navegación.')
    return
  }
  form.id_proyecto = activeOrPassedProjects.value[0]?.id_proyecto || null
  form.contenido = ''
  form.url_video = ''
  isModalOpen.value = true
}

async function enviarTestimonio() {
  if (!form.id_proyecto || !form.contenido.trim()) {
    addToast('Por favor completa los campos requeridos.', 'error')
    return
  }

  isSubmitting.value = true
  try {
    const userId = parseInt(adminIdCookie.value)
    const payload = {
      id_usuario: userId,
      id_proyecto: parseInt(form.id_proyecto),
      contenido: form.contenido.trim(),
      url_video: form.url_video.trim() || null
    }

    await $fetch(`${config.public.apiBase}/testimonios`, {
      method: 'POST',
      body: payload
    })

    addToast('¡Testimonio enviado! Quedará visible en la web una vez que sea moderado.', 'success')
    isModalOpen.value = false
    await loadRealData()
  } catch (err) {
    console.error(err)
    addToast('Error al enviar el testimonio. Inténtalo de nuevo.', 'error')
  } finally {
    isSubmitting.value = false
  }
}

const manejarErrorMiniatura = (event) => {
  const img = event.target
  if (img.src.includes('maxresdefault.jpg')) {
    img.src = img.src.replace('maxresdefault.jpg', 'hqdefault.jpg')
  }
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>