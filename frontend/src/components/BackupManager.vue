<template>
  <div class="bg-white rounded-lg shadow p-6">
    <div class="mb-6">
      <h3 class="text-lg font-medium text-gray-900">{{ t('calculator.backup.title') }}</h3>
      <p class="text-sm text-gray-500">Importa y exporta tus matrices</p>
    </div>

    <!-- Export Section -->
    <div class="mb-6 p-4 border border-gray-200 rounded-lg">
      <h4 class="text-sm font-medium text-gray-900 mb-3">{{ t('calculator.backup.export.title') }}</h4>
      <p class="text-sm text-gray-600 mb-4">
        Descarga todas tus matrices en formato JSON
      </p>
      <button
        @click="exportBackup"
        :disabled="exporting"
        class="w-full px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 disabled:opacity-50"
      >
        {{ exporting ? t('common.loading') : t('calculator.backup.export.all') }}
      </button>
    </div>

    <!-- Import Section -->
    <div class="mb-6 p-4 border border-gray-200 rounded-lg">
      <h4 class="text-sm font-medium text-gray-900 mb-3">{{ t('calculator.backup.import.csv') }}</h4>
      <p class="text-sm text-gray-600 mb-4">
        Carga una matriz desde un archivo CSV
      </p>
      
      <div class="space-y-3">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Nombre de la matriz
          </label>
          <input
            v-model="importName"
            type="text"
            placeholder="Ej: Matriz Importada"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Archivo CSV
          </label>
          <input
            ref="fileInput"
            type="file"
            accept=".csv"
            @change="handleFileSelect"
            class="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-medium file:bg-primary-50 file:text-primary-700 hover:file:bg-primary-100"
          />
        </div>

        <button
          @click="importCSV"
          :disabled="!selectedFile || !importName.trim() || importing"
          class="w-full px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ importing ? t('common.loading') : 'Importar Matriz' }}
        </button>
      </div>
    </div>

    <!-- CSV Format Help -->
    <div class="p-4 bg-blue-50 border border-blue-200 rounded-lg">
      <h4 class="text-sm font-medium text-blue-900 mb-2">Formato CSV</h4>
      <p class="text-xs text-blue-800 mb-2">
        El archivo CSV debe tener el siguiente formato:
      </p>
      <div class="bg-white p-2 rounded border border-blue-200 font-mono text-xs">
        1,2,3<br>
        4,5,6<br>
        7,8,9
      </div>
      <p class="text-xs text-blue-700 mt-2">
        Cada línea representa una fila, los valores separados por comas.
      </p>
    </div>

    <!-- Success Message -->
    <div v-if="successMessage" class="mt-4 p-3 bg-green-50 border border-green-200 rounded-md">
      <p class="text-sm text-green-800">{{ successMessage }}</p>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="mt-4 p-3 bg-red-50 border border-red-200 rounded-md">
      <p class="text-sm text-red-800">{{ error }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useMatrixStore } from '@/stores/matrixStore'

const { t } = useI18n()
import type { Matrix } from '@/types/matrix'

const emit = defineEmits<{
  imported: [matrix: Matrix]
}>()

const matrixStore = useMatrixStore()

const exporting = ref(false)
const importing = ref(false)
const importName = ref('')
const selectedFile = ref<File | null>(null)
const fileInput = ref<HTMLInputElement | null>(null)
const successMessage = ref<string | null>(null)
const error = ref<string | null>(null)

function handleFileSelect(event: Event) {
  const target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0 && target.files[0]) {
    selectedFile.value = target.files[0]
    
    // Auto-fill name from filename if empty
    if (!importName.value.trim()) {
      importName.value = target.files[0].name.replace('.csv', '')
    }
  }
  error.value = null
  successMessage.value = null
}

async function exportBackup() {
  exporting.value = true
  error.value = null
  successMessage.value = null

  try {
    // Fetch all matrices
    await matrixStore.fetchMatrices()
    const matrices = matrixStore.matrices
    
    // Create backup data
    const backupData = {
      version: '2.0',
      timestamp: new Date().toISOString(),
      total_matrices: matrices.length,
      matrices: matrices
    }

    // Create blob and download
    const blob = new Blob([JSON.stringify(backupData, null, 2)], { type: 'application/json' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `matrixcalc_backup_${new Date().toISOString().split('T')[0]}.json`
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(url)
    document.body.removeChild(a)

    successMessage.value = 'Backup exportado exitosamente'
    setTimeout(() => {
      successMessage.value = null
    }, 3000)
  } catch (err) {
    error.value = `Error al exportar backup: ${err}`
  } finally {
    exporting.value = false
  }
}

async function importCSV() {
  if (!selectedFile.value || !importName.value.trim()) return

  importing.value = true
  error.value = null
  successMessage.value = null

  try {
    const matrix = await matrixStore.importMatrixCSV(selectedFile.value, importName.value.trim())
    
    successMessage.value = `Matriz "${matrix.name}" importada exitosamente`
    emit('imported', matrix)

    // Reset form
    importName.value = ''
    selectedFile.value = null
    if (fileInput.value) {
      fileInput.value.value = ''
    }

    setTimeout(() => {
      successMessage.value = null
    }, 3000)
  } catch (err) {
    error.value = `Error al importar CSV: ${err}`
  } finally {
    importing.value = false
  }
}
</script>
