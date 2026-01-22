/**
 * Store Pinia para gestión de estadísticas
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useMatrixAPI } from '@/composables/useMatrixAPI'
import type { Stats, Operation } from '@/types/matrix'

export const useStatsStore = defineStore('stats', () => {
  const api = useMatrixAPI()
  
  // State
  const stats = ref<Stats | null>(null)
  const operations = ref<Operation[]>([])
  const operationsCount = ref(0)
  const lastUpdate = ref<Date | null>(null)

  // Getters
  const recentOperations = computed(() => {
    return operations.value.slice(0, 10)
  })

  const operationsByType = computed(() => {
    return stats.value?.operations_by_type || []
  })

  const timeline = computed(() => {
    return stats.value?.operations_timeline || []
  })

  // Actions
  async function fetchStats() {
    try {
      stats.value = await api.getStats()
      lastUpdate.value = new Date()
    } catch (error) {
      console.error('Error fetching stats:', error)
      throw error
    }
  }

  async function fetchOperations() {
    try {
      const response = await api.getOperations()
      operations.value = response.results
      operationsCount.value = response.count
    } catch (error) {
      console.error('Error fetching operations:', error)
      throw error
    }
  }

  async function performOperation(
    type: 'sum' | 'subtract' | 'multiply' | 'inverse' | 'determinant' | 'transpose' | 'rank' | 'eigenvalues' | 'svd' | 'qr' | 'cholesky',
    matrixAId?: number,
    matrixBId?: number
  ) {
    try {
      let operation: Operation

      switch (type) {
        case 'sum':
          operation = await api.sumMatrices({ matrix_a_id: matrixAId, matrix_b_id: matrixBId })
          break
        case 'subtract':
          operation = await api.subtractMatrices({ matrix_a_id: matrixAId, matrix_b_id: matrixBId })
          break
        case 'multiply':
          operation = await api.multiplyMatrices({ matrix_a_id: matrixAId, matrix_b_id: matrixBId })
          break
        case 'inverse':
          operation = await api.inverseMatrix({ matrix_id: matrixAId })
          break
        case 'determinant':
          operation = await api.determinantMatrix({ matrix_id: matrixAId })
          break
        case 'transpose':
          operation = await api.transposeMatrix({ matrix_id: matrixAId })
          break
        case 'rank':
          operation = await api.calculateRank({ matrix_id: matrixAId })
          break
        case 'eigenvalues':
          operation = await api.calculateEigenvalues({ matrix_id: matrixAId })
          break
        case 'svd':
          operation = await api.calculateSVD({ matrix_id: matrixAId })
          break
        case 'qr':
          operation = await api.calculateQR({ matrix_id: matrixAId })
          break
        case 'cholesky':
          operation = await api.calculateCholesky({ matrix_id: matrixAId })
          break
        default:
          throw new Error(`Unknown operation type: ${type}`)
      }

      // Añadir la operación al inicio de la lista
      operations.value.unshift(operation)
      operationsCount.value++

      // Actualizar stats
      await fetchStats()

      return operation
    } catch (error) {
      console.error('Error performing operation:', error)
      throw error
    }
  }

  function clearOperations() {
    operations.value = []
    operationsCount.value = 0
  }

  return {
    // State
    stats,
    operations,
    operationsCount,
    lastUpdate,
    // Getters
    recentOperations,
    operationsByType,
    timeline,
    // Actions
    fetchStats,
    fetchOperations,
    performOperation,
    clearOperations
  }
})
