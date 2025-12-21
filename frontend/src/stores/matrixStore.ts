/**
 * Store Pinia para gestión de matrices
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useMatrixAPI } from '@/composables/useMatrixAPI'
import type { Matrix, MatrixCreateDTO } from '@/types/matrix'

export const useMatrixStore = defineStore('matrix', () => {
  const api = useMatrixAPI()
  
  // State
  const matrices = ref<Matrix[]>([])
  const currentMatrix = ref<Matrix | null>(null)
  const selectedMatrixA = ref<Matrix | null>(null)
  const selectedMatrixB = ref<Matrix | null>(null)
  const totalCount = ref(0)

  // Getters
  const sortedMatrices = computed(() => {
    return [...matrices.value].sort((a, b) => 
      new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
    )
  })

  const getMatrixById = computed(() => (id: number) => {
    return matrices.value.find(m => m.id === id)
  })

  // Actions
  async function fetchMatrices() {
    try {
      const response = await api.getMatrices()
      matrices.value = response.results
      totalCount.value = response.count
    } catch (error) {
      console.error('Error fetching matrices:', error)
      throw error
    }
  }

  async function fetchMatrix(id: number) {
    try {
      currentMatrix.value = await api.getMatrix(id)
      return currentMatrix.value
    } catch (error) {
      console.error('Error fetching matrix:', error)
      throw error
    }
  }

  async function createMatrix(matrix: MatrixCreateDTO) {
    try {
      const newMatrix = await api.createMatrix(matrix)
      matrices.value.unshift(newMatrix)
      totalCount.value++
      return newMatrix
    } catch (error) {
      console.error('Error creating matrix:', error)
      throw error
    }
  }

  async function updateMatrix(id: number, matrix: Partial<MatrixCreateDTO>) {
    try {
      const updated = await api.updateMatrix(id, matrix)
      const index = matrices.value.findIndex(m => m.id === id)
      if (index !== -1) {
        matrices.value[index] = updated
      }
      if (currentMatrix.value?.id === id) {
        currentMatrix.value = updated
      }
      return updated
    } catch (error) {
      console.error('Error updating matrix:', error)
      throw error
    }
  }

  async function deleteMatrix(id: number) {
    try {
      await api.deleteMatrix(id)
      matrices.value = matrices.value.filter(m => m.id !== id)
      totalCount.value--
      if (currentMatrix.value?.id === id) {
        currentMatrix.value = null
      }
      if (selectedMatrixA.value?.id === id) {
        selectedMatrixA.value = null
      }
      if (selectedMatrixB.value?.id === id) {
        selectedMatrixB.value = null
      }
    } catch (error) {
      console.error('Error deleting matrix:', error)
      throw error
    }
  }

  async function exportMatrixCSV(id: number, filename: string) {
    try {
      const blob = await api.exportMatrixCSV(id)
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = filename
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (error) {
      console.error('Error exporting matrix:', error)
      throw error
    }
  }

  async function importMatrixCSV(file: File, name: string) {
    try {
      const newMatrix = await api.importMatrixCSV(file, name)
      matrices.value.unshift(newMatrix)
      totalCount.value++
      return newMatrix
    } catch (error) {
      console.error('Error importing matrix:', error)
      throw error
    }
  }

  function selectMatrixA(matrix: Matrix | null) {
    selectedMatrixA.value = matrix
  }

  function selectMatrixB(matrix: Matrix | null) {
    selectedMatrixB.value = matrix
  }

  function clearSelections() {
    selectedMatrixA.value = null
    selectedMatrixB.value = null
  }

  return {
    // State
    matrices,
    currentMatrix,
    selectedMatrixA,
    selectedMatrixB,
    totalCount,
    // Getters
    sortedMatrices,
    getMatrixById,
    // Actions
    fetchMatrices,
    fetchMatrix,
    createMatrix,
    updateMatrix,
    deleteMatrix,
    exportMatrixCSV,
    importMatrixCSV,
    selectMatrixA,
    selectMatrixB,
    clearSelections
  }
})
