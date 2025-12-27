/**
 * Composable para interactuar con la API de MatrixCalc
 * VERSION CON LOGGING DETALLADO PARA DEBUGGING
 */
import axios, { type AxiosError } from 'axios'
import { ref } from 'vue'
import type { 
  Matrix, 
  MatrixCreateDTO, 
  Operation, 
  OperationRequest, 
  Stats, 
  PaginatedResponse,
  APIError 
} from '@/types/matrix'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api'

// LOG INICIAL
console.log('🔧 [MatrixAPI] INICIALIZADO')
console.log('🌐 [MatrixAPI] API_BASE_URL:', API_BASE_URL)
console.log('📍 [MatrixAPI] import.meta.env.VITE_API_URL:', import.meta.env.VITE_API_URL)

export function useMatrixAPI() {
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Helper para manejar errores
  const handleError = (err: unknown): string => {
    console.error('❌ [MatrixAPI] handleError called:', err)
    if (axios.isAxiosError(err)) {
      const axiosError = err as AxiosError<APIError>
      const errorMsg = axiosError.response?.data?.error || axiosError.message
      console.error('❌ [MatrixAPI] Axios Error:', errorMsg)
      console.error('❌ [MatrixAPI] Status:', axiosError.response?.status)
      console.error('❌ [MatrixAPI] Response Data:', axiosError.response?.data)
      return errorMsg
    }
    return String(err)
  }

  // Matrices CRUD
  const getMatrices = async (): Promise<PaginatedResponse<Matrix>> => {
    const funcName = '📋 [getMatrices]'
    console.log(`${funcName} INICIO`)
    loading.value = true
    error.value = null
    try {
      const url = `${API_BASE_URL}/matrices/`
      console.log(`${funcName} Requesting GET ${url}`)
      const response = await axios.get<PaginatedResponse<Matrix>>(url)
      console.log(`${funcName} ✅ SUCCESS - Received ${response.data.count} matrices`)
      return response.data
    } catch (err) {
      console.error(`${funcName} ❌ FAILED`)
      error.value = handleError(err)
      throw err
    } finally {
      loading.value = false
      console.log(`${funcName} FIN`)
    }
  }

  const createMatrix = async (matrix: MatrixCreateDTO): Promise<Matrix> => {
    const funcName = '➕ [createMatrix]'
    console.log(`${funcName} INICIO`)
    console.log(`${funcName} Data:`, JSON.stringify(matrix))
    loading.value = true
    error.value = null
    try {
      const url = `${API_BASE_URL}/matrices/`
      console.log(`${funcName} Requesting POST ${url}`)
      const response = await axios.post<Matrix>(url, matrix)
      console.log(`${funcName} ✅ SUCCESS - Created matrix ID:`, response.data.id)
      return response.data
    } catch (err) {
      console.error(`${funcName} ❌ FAILED`)
      error.value = handleError(err)
      throw err
    } finally {
      loading.value = false
      console.log(`${funcName} FIN`)
    }
  }

  const getMatrix = async (id: number): Promise<Matrix> => {
    console.log(`📖 [getMatrix] ${id} - INICIO`)
    loading.value = true
    error.value = null
    try {
      const response = await axios.get<Matrix>(`${API_BASE_URL}/matrices/${id}/`)
      console.log(`📖 [getMatrix] ${id} - ✅ SUCCESS`)
      return response.data
    } catch (err) {
      console.error(`📖 [getMatrix] ${id} - ❌ FAILED`)
      error.value = handleError(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateMatrix = async (id: number, matrix: Partial<MatrixCreateDTO>): Promise<Matrix> => {
    console.log(`📝 [updateMatrix] ${id} - INICIO`)
    loading.value = true
    error.value = null
    try {
      const response = await axios.patch<Matrix>(`${API_BASE_URL}/matrices/${id}/`, matrix)
      console.log(`📝 [updateMatrix] ${id} - ✅ SUCCESS`)
      return response.data
    } catch (err) {
      console.error(`📝 [updateMatrix] ${id} - ❌ FAILED`)
      error.value = handleError(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteMatrix = async (id: number): Promise<void> => {
    console.log(`🗑️ [deleteMatrix] ${id} - INICIO`)
    loading.value = true
    error.value = null
    try {
      await axios.delete(`${API_BASE_URL}/matrices/${id}/`)
      console.log(`🗑️ [deleteMatrix] ${id} - ✅ SUCCESS`)
    } catch (err) {
      console.error(`🗑️ [deleteMatrix] ${id} - ❌ FAILED`)
      error.value = handleError(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const exportMatrixCSV = async (id: number): Promise<Blob> => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.get(`${API_BASE_URL}/matrices/${id}/export_csv/`, {
        responseType: 'blob'
      })
      return response.data
    } catch (err) {
      error.value = handleError(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const importMatrixCSV = async (file: File, name: string): Promise<Matrix> => {
    loading.value = true
    error.value = null
    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('name', name)
      const response = await axios.post<Matrix>(`${API_BASE_URL}/matrices/import_csv/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      return response.data
    } catch (err) {
      error.value = handleError(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  // Operations
  const getOperations = async (): Promise<PaginatedResponse<Operation>> => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.get<PaginatedResponse<Operation>>(`${API_BASE_URL}/operations-history/`)
      return response.data
    } catch (err) {
      error.value = handleError(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const sumMatrices = async (request: OperationRequest): Promise<Operation> => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.post<Operation>(`${API_BASE_URL}/operations/sum/`, request)
      return response.data
    } catch (err) {
      error.value = handleError(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const subtractMatrices = async (request: OperationRequest): Promise<Operation> => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.post<Operation>(`${API_BASE_URL}/operations/subtract/`, request)
      return response.data
    } catch (err) {
      error.value = handleError(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const multiplyMatrices = async (request: OperationRequest): Promise<Operation> => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.post<Operation>(`${API_BASE_URL}/operations/multiply/`, request)
      return response.data
    } catch (err) {
      error.value = handleError(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const inverseMatrix = async (request: OperationRequest): Promise<Operation> => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.post<Operation>(`${API_BASE_URL}/operations/inverse/`, request)
      return response.data
    } catch (err) {
      error.value = handleError(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const determinantMatrix = async (request: OperationRequest): Promise<Operation> => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.post<Operation>(`${API_BASE_URL}/operations/determinant/`, request)
      return response.data
    } catch (err) {
      error.value = handleError(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const transposeMatrix = async (request: OperationRequest): Promise<Operation> => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.post<Operation>(`${API_BASE_URL}/operations/transpose/`, request)
      return response.data
    } catch (err) {
      error.value = handleError(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  // Stats
  const getStats = async (): Promise<Stats> => {
    console.log('📊 [getStats] - INICIO')
    loading.value = true
    error.value = null
    try {
      const response = await axios.get<Stats>(`${API_BASE_URL}/stats/`)
      console.log('📊 [getStats] - ✅ SUCCESS')
      return response.data
    } catch (err) {
      console.error('📊 [getStats] - ❌ FAILED')
      error.value = handleError(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    error,
    // Matrices
    getMatrices,
    getMatrix,
    createMatrix,
    updateMatrix,
    deleteMatrix,
    exportMatrixCSV,
    importMatrixCSV,
    // Operations
    getOperations,
    sumMatrices,
    subtractMatrices,
    multiplyMatrices,
    inverseMatrix,
    determinantMatrix,
    transposeMatrix,
    // Stats
    getStats
  }
}
