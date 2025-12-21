<template>
  <div class="bg-white rounded-lg shadow p-6">
    <div class="mb-6">
      <h3 class="text-lg font-medium text-gray-900">Panel de Operaciones</h3>
      <p class="text-sm text-gray-500">Selecciona matrices y ejecuta operaciones</p>
    </div>

    <!-- Selected Matrices -->
    <div class="space-y-4 mb-6">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Matriz A</label>
        <div class="flex items-center gap-2">
          <select
            v-model="selectedMatrixAId"
            class="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <option :value="null">Seleccionar matriz...</option>
            <option
              v-for="matrix in availableMatrices"
              :key="matrix.id"
              :value="matrix.id"
            >
              {{ matrix.name }} ({{ matrix.rows }}×{{ matrix.cols }})
            </option>
          </select>
          <button
            v-if="selectedMatrixA"
            @click="viewMatrix(selectedMatrixA)"
            class="p-2 text-gray-500 hover:text-primary-600 border border-gray-300 rounded-md"
            title="Ver matriz"
          >
            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
            </svg>
          </button>
        </div>
      </div>

      <div v-if="requiresTwoMatrices">
        <label class="block text-sm font-medium text-gray-700 mb-2">Matriz B</label>
        <div class="flex items-center gap-2">
          <select
            v-model="selectedMatrixBId"
            class="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <option :value="null">Seleccionar matriz...</option>
            <option
              v-for="matrix in availableMatrices"
              :key="matrix.id"
              :value="matrix.id"
            >
              {{ matrix.name }} ({{ matrix.rows }}×{{ matrix.cols }})
            </option>
          </select>
          <button
            v-if="selectedMatrixB"
            @click="viewMatrix(selectedMatrixB)"
            class="p-2 text-gray-500 hover:text-primary-600 border border-gray-300 rounded-md"
            title="Ver matriz"
          >
            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Operations -->
    <div class="mb-6">
      <label class="block text-sm font-medium text-gray-700 mb-3">Operaciones</label>
      
      <!-- Binary Operations -->
      <div class="mb-4">
        <p class="text-xs text-gray-500 mb-2">Operaciones con dos matrices</p>
        <div class="grid grid-cols-3 gap-2">
          <button
            @click="selectOperation('sum')"
            :disabled="!canPerformBinaryOperation"
            :class="[
              'p-3 rounded-lg border-2 transition-colors',
              selectedOperation === 'sum'
                ? 'border-primary-500 bg-primary-50 text-primary-700'
                : 'border-gray-200 hover:border-primary-300 text-gray-700',
              !canPerformBinaryOperation && 'opacity-50 cursor-not-allowed'
            ]"
          >
            <div class="text-2xl mb-1">+</div>
            <div class="text-xs">Suma</div>
          </button>

          <button
            @click="selectOperation('subtract')"
            :disabled="!canPerformBinaryOperation"
            :class="[
              'p-3 rounded-lg border-2 transition-colors',
              selectedOperation === 'subtract'
                ? 'border-primary-500 bg-primary-50 text-primary-700'
                : 'border-gray-200 hover:border-primary-300 text-gray-700',
              !canPerformBinaryOperation && 'opacity-50 cursor-not-allowed'
            ]"
          >
            <div class="text-2xl mb-1">−</div>
            <div class="text-xs">Resta</div>
          </button>

          <button
            @click="selectOperation('multiply')"
            :disabled="!canPerformBinaryOperation"
            :class="[
              'p-3 rounded-lg border-2 transition-colors',
              selectedOperation === 'multiply'
                ? 'border-primary-500 bg-primary-50 text-primary-700'
                : 'border-gray-200 hover:border-primary-300 text-gray-700',
              !canPerformBinaryOperation && 'opacity-50 cursor-not-allowed'
            ]"
          >
            <div class="text-2xl mb-1">×</div>
            <div class="text-xs">Multiplicación</div>
          </button>
        </div>
      </div>

      <!-- Unary Operations -->
      <div>
        <p class="text-xs text-gray-500 mb-2">Operaciones con una matriz</p>
        <div class="grid grid-cols-3 gap-2">
          <button
            @click="selectOperation('inverse')"
            :disabled="!canPerformUnaryOperation"
            :class="[
              'p-3 rounded-lg border-2 transition-colors',
              selectedOperation === 'inverse'
                ? 'border-primary-500 bg-primary-50 text-primary-700'
                : 'border-gray-200 hover:border-primary-300 text-gray-700',
              !canPerformUnaryOperation && 'opacity-50 cursor-not-allowed'
            ]"
          >
            <div class="text-2xl mb-1">A⁻¹</div>
            <div class="text-xs">Inversa</div>
          </button>

          <button
            @click="selectOperation('determinant')"
            :disabled="!canPerformUnaryOperation"
            :class="[
              'p-3 rounded-lg border-2 transition-colors',
              selectedOperation === 'determinant'
                ? 'border-primary-500 bg-primary-50 text-primary-700'
                : 'border-gray-200 hover:border-primary-300 text-gray-700',
              !canPerformUnaryOperation && 'opacity-50 cursor-not-allowed'
            ]"
          >
            <div class="text-2xl mb-1">|A|</div>
            <div class="text-xs">Determinante</div>
          </button>

          <button
            @click="selectOperation('transpose')"
            :disabled="!canPerformUnaryOperation"
            :class="[
              'p-3 rounded-lg border-2 transition-colors',
              selectedOperation === 'transpose'
                ? 'border-primary-500 bg-primary-50 text-primary-700'
                : 'border-gray-200 hover:border-primary-300 text-gray-700',
              !canPerformUnaryOperation && 'opacity-50 cursor-not-allowed'
            ]"
          >
            <div class="text-2xl mb-1">Aᵀ</div>
            <div class="text-xs">Transpuesta</div>
          </button>
        </div>
      </div>
    </div>

    <!-- Execute Button -->
    <button
      @click="executeOperation"
      :disabled="!canExecute || loading"
      class="w-full px-4 py-3 bg-primary-600 text-white rounded-md hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
    >
      {{ loading ? 'Ejecutando...' : 'Ejecutar Operación' }}
    </button>

    <!-- Validation Messages -->
    <div v-if="validationMessage" class="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-md">
      <p class="text-sm text-yellow-800">{{ validationMessage }}</p>
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
import { useStatsStore } from '@/stores/statsStore'
import { storeToRefs } from 'pinia'
import type { Matrix, Operation } from '@/types/matrix'

const emit = defineEmits<{
  result: [operation: Operation]
  viewMatrix: [matrix: Matrix]
}>()

const matrixStore = useMatrixStore()
const statsStore = useStatsStore()
const { matrices } = storeToRefs(matrixStore)

const selectedMatrixAId = ref<number | null>(null)
const selectedMatrixBId = ref<number | null>(null)
const selectedOperation = ref<'sum' | 'subtract' | 'multiply' | 'inverse' | 'determinant' | 'transpose' | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)
const successMessage = ref<string | null>(null)

const availableMatrices = computed(() => matrices.value)

const selectedMatrixA = computed(() => 
  matrices.value.find(m => m.id === selectedMatrixAId.value) || null
)

const selectedMatrixB = computed(() => 
  matrices.value.find(m => m.id === selectedMatrixBId.value) || null
)

const requiresTwoMatrices = computed(() => 
  selectedOperation.value && ['sum', 'subtract', 'multiply'].includes(selectedOperation.value)
)

const canPerformUnaryOperation = computed(() => !!selectedMatrixA.value)

const canPerformBinaryOperation = computed(() => 
  !!selectedMatrixA.value && !!selectedMatrixB.value
)

const validationMessage = computed(() => {
  if (!selectedOperation.value) return null
  
  if (requiresTwoMatrices.value) {
    if (!selectedMatrixA.value || !selectedMatrixB.value) {
      return 'Selecciona dos matrices para esta operación'
    }
    
    if (selectedOperation.value === 'sum' || selectedOperation.value === 'subtract') {
      if (selectedMatrixA.value.rows !== selectedMatrixB.value.rows || 
          selectedMatrixA.value.cols !== selectedMatrixB.value.cols) {
        return 'Las matrices deben tener las mismas dimensiones'
      }
    }
    
    if (selectedOperation.value === 'multiply') {
      if (selectedMatrixA.value.cols !== selectedMatrixB.value.rows) {
        return `El número de columnas de A (${selectedMatrixA.value.cols}) debe ser igual al número de filas de B (${selectedMatrixB.value.rows})`
      }
    }
  } else {
    if (!selectedMatrixA.value) {
      return 'Selecciona una matriz para esta operación'
    }
    
    if (selectedOperation.value === 'inverse' || selectedOperation.value === 'determinant') {
      if (selectedMatrixA.value.rows !== selectedMatrixA.value.cols) {
        return 'La matriz debe ser cuadrada para esta operación'
      }
    }
  }
  
  return null
})

const canExecute = computed(() => 
  !!selectedOperation.value && !validationMessage.value
)

function selectOperation(operation: typeof selectedOperation.value) {
  selectedOperation.value = operation
  error.value = null
  successMessage.value = null
}

async function executeOperation() {
  if (!canExecute.value || !selectedOperation.value) return

  loading.value = true
  error.value = null
  successMessage.value = null

  try {
    const operation = await statsStore.performOperation(
      selectedOperation.value,
      selectedMatrixAId.value!,
      selectedMatrixBId.value || undefined
    )

    successMessage.value = `Operación completada en ${operation.execution_time_ms}ms`
    emit('result', operation)

    // Refresh matrices list
    await matrixStore.fetchMatrices()

    setTimeout(() => {
      successMessage.value = null
    }, 3000)
  } catch (err) {
    error.value = String(err)
  } finally {
    loading.value = false
  }
}

function viewMatrix(matrix: Matrix) {
  emit('viewMatrix', matrix)
}

// Watch for matrix store selections
watch(() => matrixStore.selectedMatrixA, (newVal) => {
  if (newVal) selectedMatrixAId.value = newVal.id
})

watch(() => matrixStore.selectedMatrixB, (newVal) => {
  if (newVal) selectedMatrixBId.value = newVal.id
})
</script>
