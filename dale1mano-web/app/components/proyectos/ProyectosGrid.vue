<template>
  <section class="py-12 bg-white">
    <div class="max-w-7xl mx-auto px-6 md:px-12 space-y-10">
      
      <FiltroProyectos 
        :filtroActual="filtro" 
        @cambiarFiltro="filtro = $event" 
      />

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
        <ProyectoCard 
          v-for="proj in proyectosFiltrados" 
          :key="proj.id" 
          :proyecto="proj"
          :activo="filtro === 'activos'"
          @abrirInscripcion="abrirModal"
        />
      </div>

      <div v-if="proyectosFiltrados.length === 0" class="text-center py-12 text-slate-400 text-sm">
        No hay proyectos registrados en esta sección en este momento.
      </div>

      <Transition name="fade">
        <div v-if="modalAbierto" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm">
          <div class="bg-white rounded-2xl shadow-2xl max-w-lg w-full overflow-hidden border border-slate-100 transform transition-all">
            
            <div class="bg-slate-700 px-6 py-4 flex justify-between items-center text-white">
              <h3 class="font-bold text-base tracking-wide">Formulario de inscripción</h3>
              <button @click="cerrarModal" class="text-slate-300 hover:text-white text-xl font-bold transition-colors">&times;</button>
            </div>

            <form @submit.prevent="enviarFormulario" class="p-6 space-y-4 text-slate-700">
              <div>
                <label class="block text-xs font-bold text-slate-500 mb-1">Nombre Completo</label>
                <input 
                  v-model="form.nombre" 
                  type="text" 
                  placeholder="Ingrese su nombre" 
                  class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm bg-slate-100 cursor-not-allowed focus:outline-none" 
                  readonly 
                  required 
                />
              </div>

              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label class="block text-xs font-bold text-slate-500 mb-1">Cédula</label>
                  <input v-model="form.cedula" type="text" placeholder="Ingrese su número de cédula" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:border-blue-500" required />
                </div>
                <div>
                  <label class="block text-xs font-bold text-slate-500 mb-1">Número telefónico</label>
                  <input 
                    v-model="form.telefono" 
                    type="tel" 
                    maxlength="12"
                    placeholder="+506XXXXXXXX" 
                    class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:border-blue-500" 
                    required 
                  />
                </div>
              </div>

              <div>
                <label class="block text-xs font-bold text-slate-500 mb-1">Fecha Nacimiento</label>
                <input v-model="form.fechaNacimiento" type="date" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:border-blue-500" required />
              </div>

              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label class="block text-xs font-bold text-slate-500 mb-1">Género</label>
                  <select v-model="form.genero" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm bg-white focus:outline-none focus:border-blue-500">
                    <option value="Masculino">Masculino</option>
                    <option value="Femenino">Femenino</option>
                    <option value="Otro">Otro</option>
                  </select>
                </div>
                <div>
                  <label class="block text-xs font-bold text-slate-500 mb-1">Cantidad de miembros a asistir</label>
                  <input v-model.number="form.cantidad" type="number" min="1" placeholder="Ingrese la cantidad de miembros" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:border-blue-500" required />
                </div>
              </div>

              <div class="pt-4 flex justify-end space-x-2 border-t border-slate-100">
                <button type="button" @click="cerrarModal" class="px-4 py-2 border border-slate-200 rounded-lg text-xs font-bold text-slate-500 hover:bg-slate-50 transition-colors">
                  Cancelar
                </button>
                <button type="submit" class="px-5 py-2 bg-[#0b31a8] hover:bg-blue-800 text-white rounded-lg text-xs font-bold shadow-sm transition-colors">
                  🚀 Inscribirse
                </button>
              </div>
            </form>
          </div>
        </div>
      </Transition>

    </div>
  </section>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useCookie, navigateTo } from '#app'
import { useAdminData } from '~/composables/useAdminData'
import FiltroProyectos from './FiltroProyectos.vue'
import ProyectoCard from './ProyectoCard.vue'

const { projects, thematics, enrollUserInProject } = useAdminData()

const config = useRuntimeConfig()
const filtro = ref('activos')
const modalAbierto = ref(false)
const proyectoSeleccionado = ref(null)
const isLoading = ref(false)

// Cookies de sesión
const tokenCookie = useCookie('auth_token')
const adminNameCookie = useCookie('admin_name')
const adminIdCookie = useCookie('admin_id')

const form = ref({
  nombre: '',
  cedula: '',
  telefono: '+506',
  fechaNacimiento: '',
  genero: 'Masculino',
  cantidad: 1
})

const proyectosFiltrados = ref([])

// Vigilante para forzar el prefijo +506 y limitar a máximo 8 caracteres numéricos después del prefijo
watch(() => form.value.telefono, (newVal) => {
  if (!newVal.startsWith('+506')) {
    form.value.telefono = '+506' + newVal.replace(/^\+?5?0?6?/, '')
  }
  const suffix = form.value.telefono.slice(4)
  const numericSuffix = suffix.replace(/[^0-9]/g, '')
  form.value.telefono = '+506' + numericSuffix.slice(0, 8)
})

async function cargarProyectos() {
  try {
    isLoading.value = true
    const estadoAPI = filtro.value === 'activos' ? 'ACTIVO' : 'PASADO'
    
    let data
    try {
      const url = `${config.public.apiBase}/proyectos?estado=${estadoAPI}`
      data = await $fetch(url)
    } catch (e) {
      console.warn('API de proyectos no disponible, cargando fallback.')
      data = projects.value
        .filter(p => p.estado === estadoAPI)
        .map(p => {
          const tem = thematics.value.find(t => t.id_tematica === p.id_tematica)
          return {
            id_proyecto: p.id_proyecto,
            titulo: p.titulo,
            descripcion: p.descripcion,
            fecha_inicio: p.fecha_inicio,
            fecha_fin: p.fecha_fin,
            tematica: tem ? tem.nombre : 'General'
          }
        })
    }
    
    proyectosFiltrados.value = data.map(proj => {
      const dateObjStart = new Date(proj.fecha_inicio)
      const dateObjEnd = new Date(proj.fecha_fin)
      
      const fechaStr = dateObjStart.toLocaleDateString('es-ES', { 
        day: 'numeric', 
        month: 'short', 
        year: 'numeric' 
      })
      
      const horaStr = `de ${dateObjStart.toLocaleTimeString('es-ES', { 
        hour: '2-digit', 
        minute: '2-digit' 
      })} a ${dateObjEnd.toLocaleTimeString('es-ES', { 
        hour: '2-digit', 
        minute: '2-digit' 
      })}`

      return {
        id: proj.id_proyecto,
        tipo: filtro.value,
        titulo: proj.titulo,
        fecha: fechaStr,
        hora: horaStr,
        lugar: `Eje: ${proj.tematica || 'General'}`,
        descripcion: proj.descripcion
      }
    })
  } catch (error) {
    console.error('Error al cargar proyectos:', error)
    proyectosFiltrados.value = []
  } finally {
    isLoading.value = false
  }
}

watch([filtro, projects], () => {
  cargarProyectos()
}, { deep: true })

onMounted(() => {
  cargarProyectos()
})

const abrirModal = (proyecto) => {
  if (!tokenCookie.value) {
    alert('Debes iniciar sesión para inscribirte en un proyecto.')
    navigateTo('/?login=true')
    return
  }
  proyectoSeleccionado.value = proyecto
  form.value.nombre = adminNameCookie.value || ''
  form.value.telefono = '+506'
  modalAbierto.value = true
}

const cerrarModal = () => {
  modalAbierto.value = false
  proyectoSeleccionado.value = null
  form.value = { nombre: '', cedula: '', telefono: '+506', fechaNacimiento: '', genero: 'Masculino', cantidad: 1 }
}

const enviarFormulario = async () => {
  // Validaciones
  const nameRegex = /^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$/
  if (!nameRegex.test(form.value.nombre.trim())) {
    alert('El nombre completo solo debe contener letras y espacios.')
    return
  }

  const cedulaRegex = /^[0-9]+$/
  if (!cedulaRegex.test(form.value.cedula.trim())) {
    alert('La cédula solo debe contener números.')
    return
  }

  const telefonoRegex = /^\+506[0-9]{8}$/
  if (!telefonoRegex.test(form.value.telefono.trim())) {
    alert('El número telefónico debe tener el formato +506 seguido de exactamente 8 dígitos.')
    return
  }

  if (form.value.cantidad < 1) {
    alert('La cantidad de miembros debe ser al menos 1.')
    return
  }

  try {
    const userId = parseInt(adminIdCookie.value)
    if (proyectoSeleccionado.value) {
      await enrollUserInProject(userId, proyectoSeleccionado.value.id)
    }

    alert(`¡Inscripción exitosa para ${form.value.nombre}! Te esperamos en el proyecto.`)
    cerrarModal()
  } catch (error) {
    console.error(error)
    alert('Ocurrió un error en la inscripción.')
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