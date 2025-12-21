<template>
  <div class="min-h-screen bg-gray-50 py-6">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="mb-6">
        <h1 class="text-3xl font-bold text-gray-900">Historial de Operaciones</h1>
        <p class="mt-2 text-sm text-gray-600">
          Consulta el historial de operaciones realizadas
        </p>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="bg-white shadow rounded-lg p-6">
        <p class="text-gray-500 text-center">Cargando operaciones...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4">
        <p class="text-red-800">Error: {{ error }}</p>
      </div>

      <!-- Operations List -->
      <div v-else-if="operations.length > 0" class="bg-white shadow rounded-lg overflow-hidden">
        <ul class="divide-y divide-gray-200">
          <li v-for="op in operations" :key="op.id" class="p-4 hover:bg-gray-50">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium text-gray-900">
                  {{ getOperationName(op.operation_type) }}
                </p>
                <p class="text-sm text-gray-500">
                  {{ new Date(op.created_at).toLocaleString() }}
                </p>
              </div>
              <div class="text-right">
                <p class="text-sm text-gray-900">
                  Tiempo: {{ op.execution_time_ms }}ms
                </p>
                <p class="text-sm text-gray-500">
                  ID: {{ op.id }}
                </p>
              </div>
            </div>
          </li>
        </ul>
      </div>

      <!-- Empty State -->
      <div v-else class="bg-white shadow rounded-lg p-6">
        <p class="text-gray-500 text-center py-12">
          No hay operaciones registradas
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useStatsStore } from '@/stores/statsStore'
import { storeToRefs } from 'pinia'
import type { OperationType } from '@/types/matrix'

const statsStore = useStatsStore()
const { operations } = storeToRefs(statsStore)
const loading = ref(false)
const error = ref<string | null>(null)

onMounted(async () => {
  loading.value = true
  try {
    await statsStore.fetchOperations()
  } catch (err) {
    error.value = String(err)
  } finally {
    loading.value = false
  }
})

function getOperationName(type: OperationType): string {
  const names: Record<OperationType, string> = {
    'SUM': 'Suma',
    'SUBTRACT': 'Resta',
    'MULTIPLY': 'Multiplicación',
    'INVERSE': 'Inversa',
    'DETERMINANT': 'Determinante',
    'TRANSPOSE': 'Transpuesta'
  }
  return names[type] || type
}
</script>
