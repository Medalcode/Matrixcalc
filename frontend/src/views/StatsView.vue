<template>
  <div class="min-h-screen bg-gray-50 py-6">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="mb-6">
        <h1 class="text-3xl font-bold text-gray-900">Estadísticas del Sistema</h1>
        <p class="mt-2 text-sm text-gray-600">
          Métricas y análisis de operaciones matriciales
        </p>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="bg-white shadow rounded-lg p-6">
        <p class="text-gray-500 text-center">Cargando estadísticas...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4">
        <p class="text-red-800">Error: {{ error }}</p>
      </div>

      <!-- Stats Grid -->
      <div v-else-if="stats" class="space-y-6">
        <!-- Summary Cards -->
        <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <svg class="h-6 w-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />
                  </svg>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">Total Matrices</dt>
                    <dd class="text-lg font-medium text-gray-900">{{ stats.total_matrices }}</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <svg class="h-6 w-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                  </svg>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">Total Operaciones</dt>
                    <dd class="text-lg font-medium text-gray-900">{{ stats.total_operations }}</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <svg class="h-6 w-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">Tiempo Promedio</dt>
                    <dd class="text-lg font-medium text-gray-900">{{ stats.average_execution_time_ms.toFixed(2) }}ms</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <svg class="h-6 w-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4" />
                  </svg>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">Almacenamiento</dt>
                    <dd class="text-lg font-medium text-gray-900">{{ stats.storage_mb.toFixed(2) }} MB</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Operations by Type -->
        <div class="bg-white shadow rounded-lg p-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Operaciones por Tipo</h3>
          <div class="space-y-3">
            <div v-for="item in stats.operations_by_type" :key="item.operation_type" class="flex items-center justify-between">
              <div class="flex-1">
                <div class="flex items-center justify-between mb-1">
                  <span class="text-sm font-medium text-gray-700">{{ getOperationName(item.operation_type) }}</span>
                  <span class="text-sm text-gray-500">{{ item.count }} ops</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    class="bg-primary-600 h-2 rounded-full" 
                    :style="{ width: `${(item.count / stats.total_operations) * 100}%` }"
                  ></div>
                </div>
              </div>
              <div class="ml-4 text-right">
                <span class="text-xs text-gray-500">{{ item.avg_time.toFixed(2) }}ms</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="bg-white shadow rounded-lg p-6">
        <p class="text-gray-500 text-center py-12">
          No hay datos estadísticos disponibles
        </p>
      </div>

      <!-- Dashboard Charts -->
      <div class="mt-6">
        <DashboardStats />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useStatsStore } from '@/stores/statsStore'
import { storeToRefs } from 'pinia'
import DashboardStats from '@/components/DashboardStats.vue'
import type { OperationType } from '@/types/matrix'

const statsStore = useStatsStore()
const { stats } = storeToRefs(statsStore)
const loading = ref(false)
const error = ref<string | null>(null)

onMounted(async () => {
  loading.value = true
  try {
    await statsStore.fetchStats()
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
