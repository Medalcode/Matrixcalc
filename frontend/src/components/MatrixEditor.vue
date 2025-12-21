<template>
  <div class="bg-white rounded-lg shadow p-6">
    <div class="mb-4">
      <h3 class="text-lg font-medium text-gray-900">Editor de Matriz</h3>
      <p class="text-sm text-gray-500">Crea o edita una matriz</p>
    </div>

    <!-- Matrix Name and Dimensions -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Nombre</label>
        <input
          v-model="matrixName"
          type="text"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
          placeholder="Ej: Matriz A"
        />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Filas</label>
        <input
          v-model.number="rows"
          type="number"
          min="1"
          max="100"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
          @change="resizeMatrix"
        />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Columnas</label>
        <input
          v-model.number="cols"
          type="number"
          min="1"
          max="100"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
          @change="resizeMatrix"
        />
      </div>
    </div>

    <!-- Matrix Grid -->
    <div class="mb-4 overflow-x-auto">
      <div class="inline-block min-w-full">
        <div 
          class="grid gap-1"
          :style="{ gridTemplateColumns: `repeat(${cols}, minmax(60px, 1fr))` }"
        >
          <input
            v-for="(value, index) in flatMatrix"
            :key="index"
            v-model.number="flatMatrix[index]"
            type="number"
            step="any"
            class="px-2 py-1 border border-gray-300 rounded text-center focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            @input="updateMatrix"
          />
        </div>
      </div>
    </div>

    <!-- Quick Fill Actions -->
    <div class="flex flex-wrap gap-2 mb-4">
      <button
        @click="fillZeros"
        class="px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded hover:bg-gray-200"
      >
        Llenar con 0
      </button>
      <button
        @click="fillOnes"
        class="px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded hover:bg-gray-200"
      >
        Llenar con 1
      </button>
      <button
        @click="fillIdentity"
        :disabled="rows !== cols"
        class="px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Matriz Identidad
      </button>
      <button
        @click="fillRandom"
        class="px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded hover:bg-gray-200"
      >
        Aleatorio (0-10)
      </button>
    </div>

    <!-- Actions -->
    <div class="flex gap-2">
      <button
        @click="saveMatrix"
        :disabled="loading || !isValidMatrix"
        class="flex-1 px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {{ loading ? 'Guardando...' : editMode ? 'Actualizar' : 'Guardar' }}
      </button>
      <button
        v-if="editMode"
        @click="cancelEdit"
        class="px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50"
      >
        Cancelar
      </button>
      <button
        v-else
        @click="clearMatrix"
        class="px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50"
      >
        Limpiar
      </button>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="mt-4 p-3 bg-red-50 border border-red-200 rounded-md">
      <p class="text-sm text-red-800">{{ error }}</p>
    </div>

    <!-- Success Message -->
    <div v-if="successMessage" class="mt-4 p-3 bg-green-50 border border-green-200 rounded-md">
      <p class="text-sm text-green-800">{{ successMessage }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useMatrixStore } from '@/stores/matrixStore'
import type { Matrix } from '@/types/matrix'

const props = defineProps<{
  matrix?: Matrix
}>()

const emit = defineEmits<{
  saved: [matrix: Matrix]
  cancelled: []
}>()

const matrixStore = useMatrixStore()

const matrixName = ref(props.matrix?.name || '')
const rows = ref(props.matrix?.rows || 3)
const cols = ref(props.matrix?.cols || 3)
const flatMatrix = ref<number[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const successMessage = ref<string | null>(null)

const editMode = computed(() => !!props.matrix)

const isValidMatrix = computed(() => {
  return matrixName.value.trim().length > 0 && 
         rows.value > 0 && 
         cols.value > 0 &&
         flatMatrix.value.length === rows.value * cols.value &&
         flatMatrix.value.every(v => !isNaN(v))
})

// Initialize matrix
function initializeMatrix() {
  if (props.matrix) {
    flatMatrix.value = props.matrix.data.flat()
  } else {
    flatMatrix.value = Array(rows.value * cols.value).fill(0)
  }
}

// Resize matrix when dimensions change
function resizeMatrix() {
  const newSize = rows.value * cols.value
  const currentSize = flatMatrix.value.length

  if (newSize > currentSize) {
    // Add zeros for new cells
    flatMatrix.value = [...flatMatrix.value, ...Array(newSize - currentSize).fill(0)]
  } else if (newSize < currentSize) {
    // Truncate
    flatMatrix.value = flatMatrix.value.slice(0, newSize)
  }
}

function updateMatrix() {
  // Ensure all values are numbers
  flatMatrix.value = flatMatrix.value.map(v => isNaN(v) ? 0 : v)
}

// Quick fill functions
function fillZeros() {
  flatMatrix.value = Array(rows.value * cols.value).fill(0)
}

function fillOnes() {
  flatMatrix.value = Array(rows.value * cols.value).fill(1)
}

function fillIdentity() {
  if (rows.value !== cols.value) return
  
  flatMatrix.value = Array(rows.value * cols.value).fill(0).map((_, index) => {
    const row = Math.floor(index / cols.value)
    const col = index % cols.value
    return row === col ? 1 : 0
  })
}

function fillRandom() {
  flatMatrix.value = Array(rows.value * cols.value).fill(0).map(() => 
    Math.floor(Math.random() * 11)
  )
}

function clearMatrix() {
  matrixName.value = ''
  rows.value = 3
  cols.value = 3
  fillZeros()
  error.value = null
  successMessage.value = null
}

// Convert flat array to 2D array
function get2DMatrix(): number[][] {
  const matrix: number[][] = []
  for (let i = 0; i < rows.value; i++) {
    matrix.push(flatMatrix.value.slice(i * cols.value, (i + 1) * cols.value))
  }
  return matrix
}

async function saveMatrix() {
  if (!isValidMatrix.value) return

  loading.value = true
  error.value = null
  successMessage.value = null

  try {
    const matrixData = {
      name: matrixName.value.trim(),
      rows: rows.value,
      cols: cols.value,
      data: get2DMatrix()
    }

    if (editMode.value && props.matrix) {
      const updated = await matrixStore.updateMatrix(props.matrix.id, matrixData)
      successMessage.value = 'Matriz actualizada exitosamente'
      emit('saved', updated)
    } else {
      const newMatrix = await matrixStore.createMatrix(matrixData)
      successMessage.value = 'Matriz guardada exitosamente'
      emit('saved', newMatrix)
      clearMatrix()
    }

    setTimeout(() => {
      successMessage.value = null
    }, 3000)
  } catch (err) {
    error.value = String(err)
  } finally {
    loading.value = false
  }
}

function cancelEdit() {
  emit('cancelled')
}

// Watch for prop changes
watch(() => props.matrix, () => {
  if (props.matrix) {
    matrixName.value = props.matrix.name
    rows.value = props.matrix.rows
    cols.value = props.matrix.cols
    flatMatrix.value = props.matrix.data.flat()
  }
}, { immediate: true })

// Initialize on mount
initializeMatrix()
</script>
