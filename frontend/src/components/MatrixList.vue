<template>
  <div class="bg-white rounded-lg shadow">
    <div class="p-6 border-b border-gray-200">
      <div class="flex items-center justify-between">
        <div>
          <h3 class="text-lg font-medium text-gray-900">{{ t('calculator.matrixList.title') }}</h3>
          <p class="text-sm text-gray-500">{{ totalCount }} matrices en total</p>
        </div>
        <button
          @click="refreshList"
          :disabled="loading"
          class="px-3 py-2 text-sm bg-primary-600 text-white rounded-md hover:bg-primary-700 disabled:opacity-50"
        >
          {{ loading ? t('common.loading') : 'Actualizar' }}
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading && matrices.length === 0" class="p-8 text-center">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
      <p class="mt-2 text-sm text-gray-500">{{ t('common.loading') }}</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="p-6">
      <div class="bg-red-50 border border-red-200 rounded-md p-4">
        <p class="text-sm text-red-800">{{ t('common.error') }}: {{ error }}</p>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else-if="matrices.length === 0" class="p-8 text-center">
      <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
      </svg>
      <p class="mt-2 text-sm text-gray-500">{{ t('calculator.matrixList.empty') }}</p>
      <p class="text-xs text-gray-400">Crea una nueva matriz para comenzar</p>
    </div>

    <!-- Matrix List -->
    <ul v-else class="divide-y divide-gray-200">
      <li
        v-for="matrix in sortedMatrices"
        :key="matrix.id"
        class="p-4 hover:bg-gray-50 transition-colors"
      >
        <div class="flex items-center justify-between">
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2">
              <h4 class="text-sm font-medium text-gray-900 truncate">{{ matrix.name }}</h4>
              <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800">
                {{ matrix.rows }}×{{ matrix.cols }}
              </span>
            </div>
            <p class="text-xs text-gray-500 mt-1">
              Creada: {{ formatDate(matrix.created_at) }}
            </p>
          </div>

          <!-- Actions -->
          <div class="flex items-center gap-2 ml-4">
            <button
              @click="viewMatrix(matrix)"
              class="p-2 text-gray-400 hover:text-primary-600 rounded-md hover:bg-gray-100"
              title="Ver matriz"
            >
              <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
            </button>
            
            <button
              @click="editMatrix(matrix)"
              class="p-2 text-gray-400 hover:text-blue-600 rounded-md hover:bg-gray-100"
              title="Editar"
            >
              <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
            </button>

            <button
              @click="selectForOperation(matrix)"
              class="p-2 text-gray-400 hover:text-green-600 rounded-md hover:bg-gray-100"
              title="Usar en operación"
            >
              <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
              </svg>
            </button>

            <button
              @click="exportCSV(matrix)"
              class="p-2 text-gray-400 hover:text-indigo-600 rounded-md hover:bg-gray-100"
              title="Exportar CSV"
            >
              <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </button>

            <button
              @click="confirmDelete(matrix)"
              class="p-2 text-gray-400 hover:text-red-600 rounded-md hover:bg-gray-100"
              title="Eliminar"
            >
              <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
        </div>
      </li>
    </ul>

    <!-- Delete Confirmation Modal -->
    <div
      v-if="deleteCandidate"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click.self="cancelDelete"
    >
      <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4">
        <h3 class="text-lg font-medium text-gray-900 mb-2">Confirmar Eliminación</h3>
        <p class="text-sm text-gray-500 mb-4">
          ¿Estás seguro de que quieres eliminar la matriz "{{ deleteCandidate.name }}"?
          Esta acción no se puede deshacer.
        </p>
        <div class="flex gap-2 justify-end">
          <button
            @click="cancelDelete"
            class="px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50"
          >
            Cancelar
          </button>
          <button
            @click="deleteMatrix"
            :disabled="deleting"
            class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 disabled:opacity-50"
          >
            {{ deleting ? 'Eliminando...' : 'Eliminar' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useMatrixStore } from '@/stores/matrixStore'

const { t } = useI18n()
import { storeToRefs } from 'pinia'
import type { Matrix } from '@/types/matrix'

const emit = defineEmits<{
  view: [matrix: Matrix]
  edit: [matrix: Matrix]
  select: [matrix: Matrix]
}>()

const matrixStore = useMatrixStore()
const { matrices, totalCount, sortedMatrices } = storeToRefs(matrixStore)

const loading = ref(false)
const error = ref<string | null>(null)
const deleteCandidate = ref<Matrix | null>(null)
const deleting = ref(false)

onMounted(async () => {
  await refreshList()
})

async function refreshList() {
  loading.value = true
  error.value = null
  try {
    await matrixStore.fetchMatrices()
  } catch (err) {
    error.value = String(err)
  } finally {
    loading.value = false
  }
}

function formatDate(dateString: string): string {
  const date = new Date(dateString)
  return date.toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function viewMatrix(matrix: Matrix) {
  emit('view', matrix)
}

function editMatrix(matrix: Matrix) {
  emit('edit', matrix)
}

function selectForOperation(matrix: Matrix) {
  emit('select', matrix)
}

async function exportCSV(matrix: Matrix) {
  try {
    await matrixStore.exportMatrixCSV(matrix.id, `${matrix.name}.csv`)
  } catch (err) {
    error.value = `Error al exportar: ${err}`
  }
}

function confirmDelete(matrix: Matrix) {
  deleteCandidate.value = matrix
}

function cancelDelete() {
  deleteCandidate.value = null
}

async function deleteMatrix() {
  if (!deleteCandidate.value) return

  deleting.value = true
  try {
    await matrixStore.deleteMatrix(deleteCandidate.value.id)
    deleteCandidate.value = null
  } catch (err) {
    error.value = `Error al eliminar: ${err}`
  } finally {
    deleting.value = false
  }
}
</script>
