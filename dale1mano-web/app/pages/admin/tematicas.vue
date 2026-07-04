<template>
  <div class="space-y-6 animate-fade-in">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0">
      <div>
        <h2 class="text-xl font-black text-slate-900">Ejes Temáticos y Programas</h2>
        <p class="text-xs text-slate-500">Administra las temáticas que clasifican las actividades y proyectos de la organización.</p>
      </div>
      <button 
        @click="openAddModal"
        class="flex items-center justify-center space-x-2 px-4 py-2.5 rounded-xl text-white text-xs font-black transition-all shadow-md hover:scale-[1.02] active:scale-[0.98] self-start cursor-pointer uppercase tracking-wider"
        style="background: linear-gradient(135deg, #e0531c 0%, #f06732 100%); box-shadow: 0 4px 14px rgba(224,83,28,0.25);"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-4 h-4">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
        </svg>
        <span>Nueva Temática</span>
      </button>
    </div>

    <!-- TABLA DE TEMÁTICAS -->
    <div class="bg-white border border-slate-200 rounded-2xl shadow-2xs overflow-hidden text-left">
      <div class="overflow-x-auto">
        <table class="w-full text-left text-sm">
          <thead>
            <tr class="border-b border-slate-200 bg-slate-50 text-slate-500 font-black text-[10px] uppercase tracking-wider">
              <th class="p-4">Eje Temático</th>
              <th class="p-4">Descripción</th>
              <th class="p-4">Estado</th>
              <th class="p-4 text-center">Acciones</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr 
              v-for="tem in thematics" 
              :key="tem.id_tematica"
              class="hover:bg-slate-50/50 transition-colors"
            >
              <!-- Nombre -->
              <td class="p-4 font-bold text-slate-800">
                {{ tem.nombre }}
              </td>

              <!-- Descripción -->
              <td class="p-4 text-xs text-slate-500 max-w-sm">
                {{ tem.descripcion || 'Sin descripción' }}
              </td>

              <!-- Estado -->
              <td class="p-4">
                <span 
                  class="inline-flex items-center text-[10px] font-black tracking-wide px-2.5 py-0.5 rounded-full uppercase"
                  :class="[
                    tem.estado === 'ACTIVO' ? 'bg-emerald-100 text-emerald-700' : 'bg-rose-100 text-rose-700'
                  ]"
                >
                  {{ tem.estado }}
                </span>
              </td>

              <!-- Acciones -->
              <td class="p-4 text-center">
                <div class="flex items-center justify-center space-x-2">
                  <!-- Editar -->
                  <button 
                    @click="openEditModal(tem)"
                    class="p-2 rounded-lg bg-blue-50 border border-blue-200 text-[#0b31a8] hover:bg-[#0b31a8] hover:text-white hover:border-transparent transition-all cursor-pointer"
                    title="Editar Temática"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L6.832 19.82a4.5 4.5 0 01-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 011.13-1.897L16.863 4.487zm0 0L19.5 7.125" />
                    </svg>
                  </button>

                  <!-- Toggle Estado -->
                  <button 
                    @click="handleToggleStatus(tem)"
                    class="px-2.5 py-1.5 rounded-lg text-[9px] font-black uppercase transition-all border cursor-pointer"
                    :class="[
                      tem.estado === 'ACTIVO' 
                        ? 'bg-amber-50 hover:bg-amber-600 border-amber-200 text-amber-600 hover:text-white hover:border-transparent' 
                        : 'bg-emerald-50 hover:bg-emerald-600 border-emerald-200 text-emerald-600 hover:text-white hover:border-transparent'
                    ]"
                  >
                    {{ tem.estado === 'ACTIVO' ? 'Desactivar' : 'Activar' }}
                  </button>

                  <!-- Eliminar -->
                  <button 
                    @click="handleDelete(tem.id_tematica)"
                    class="p-2 rounded-lg bg-rose-50 border border-rose-100 hover:bg-rose-600 text-rose-600 hover:text-white transition-all cursor-pointer"
                    title="Eliminar Temática"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
                    </svg>
                  </button>
                </div>
              </td>
            </tr>

            <tr v-if="thematics.length === 0">
              <td colspan="4" class="py-12 text-center text-slate-400 text-xs font-medium italic">
                No hay ejes temáticos registrados.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- MODAL: CREAR O EDITAR -->
    <transition name="fade">
      <div 
        v-if="isModalOpen"
        class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs"
      >
        <div class="bg-white border border-slate-200 w-full max-w-md rounded-2xl shadow-xl overflow-hidden max-h-[90vh] flex flex-col animate-fade-in">
          <!-- Header -->
          <div class="px-6 py-4 border-b border-slate-100 flex items-center justify-between bg-slate-50">
            <h3 class="text-sm font-black text-slate-800 uppercase tracking-wide">
              {{ isEditing ? 'Actualizar Temática' : 'Crear Temática' }}
            </h3>
            <button @click="isModalOpen = false" class="text-slate-400 hover:text-slate-600 transition-colors cursor-pointer">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-5 h-5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l18 18" />
              </svg>
            </button>
          </div>

          <!-- Body Form -->
          <form @submit.prevent="submitForm" class="p-6 space-y-4 text-left overflow-y-auto">
            <div class="space-y-1">
              <label class="text-[10px] uppercase font-black text-slate-400 tracking-wider block">Nombre del Eje</label>
              <input 
                v-model="form.nombre" 
                type="text" 
                required
                placeholder="Ej. Salud Mental"
                class="w-full bg-slate-50 border border-slate-200 text-slate-800 text-xs rounded-xl px-4 py-2.5 focus:outline-none focus:border-[#0b31a8] focus:bg-white transition-all"
              />
            </div>

            <div class="space-y-1">
              <label class="text-[10px] uppercase font-black text-slate-400 tracking-wider block">Descripción</label>
              <textarea 
                v-model="form.descripcion" 
                rows="4"
                placeholder="Detalla de qué trata este eje temático..."
                class="w-full bg-slate-50 border border-slate-200 text-slate-800 text-xs rounded-xl px-4 py-2.5 focus:outline-none focus:border-[#0b31a8] focus:bg-white transition-all"
              ></textarea>
            </div>
          </form>

          <!-- Footer -->
          <div class="px-6 py-4 border-t border-slate-100 flex justify-end space-x-3 bg-slate-50">
            <button 
              type="button" 
              @click="isModalOpen = false" 
              class="px-4 py-2 text-xs font-bold text-slate-500 hover:text-slate-850 transition-colors cursor-pointer uppercase"
            >
              Cancelar
            </button>
            <button 
              type="submit" 
              @click="submitForm"
              class="px-5 py-2 text-white text-xs font-black rounded-xl shadow-xs transition-all bg-[#0b31a8] hover:bg-blue-800 cursor-pointer uppercase tracking-wider"
            >
              Guardar Temática
            </button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useAdminData, addToast } from '../../composables/useAdminData'

definePageMeta({
  layout: 'admin'
})

const { thematics, addTematica, editTematica, deleteTematica } = useAdminData()

// Variables reactivas
const isModalOpen = ref(false)
const isEditing = ref(false)
const editingId = ref<number | null>(null)

const form = reactive({
  nombre: '',
  descripcion: ''
})

// Modales abrir/cerrar
function openAddModal() {
  isEditing.value = false
  editingId.value = null
  form.nombre = ''
  form.descripcion = ''
  isModalOpen.value = true
}

function openEditModal(tem: any) {
  isEditing.value = true
  editingId.value = tem.id_tematica
  form.nombre = tem.nombre
  form.descripcion = tem.descripcion
  isModalOpen.value = true
}

// Cambiar estado (Activar/Desactivar)
async function handleToggleStatus(tem: any) {
  const nuevoEstado = tem.estado === 'ACTIVO' ? 'INACTIVO' : 'ACTIVO'
  try {
    await editTematica(tem.id_tematica, { estado: nuevoEstado })
  } catch (err) {
    console.error(err)
  }
}

// Eliminar
async function handleDelete(id: number) {
  if (confirm('¿Estás seguro de que deseas eliminar este eje temático? Esto desvinculará todos los proyectos asociados.')) {
    try {
      await deleteTematica(id)
    } catch (err) {
      console.error(err)
    }
  }
}

// Guardar
async function submitForm() {
  if (!form.nombre.trim()) {
    addToast('El nombre de la temática es obligatorio.', 'error')
    return
  }

  try {
    if (isEditing.value && editingId.value) {
      await editTematica(editingId.value, {
        nombre: form.nombre,
        descripcion: form.descripcion
      })
    } else {
      await addTematica({
        nombre: form.nombre,
        descripcion: form.descripcion,
        estado: 'ACTIVO'
      })
    }
    isModalOpen.value = false
  } catch (err) {
    console.error(err)
  }
}
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.4s ease-out forwards;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
