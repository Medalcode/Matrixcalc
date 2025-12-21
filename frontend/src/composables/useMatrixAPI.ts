/**
 * Composable para interactuar con la API de MatrixCalc
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

export function useMatrixAPI() {
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Helper para manejar errores
  const handleError = (err: unknown): string => {
    if (axios.isAxiosError(err)) {
      const axiosError = err as AxiosError<APIError>
      return axiosError.response?.data?.error || axiosError.message
    }
    return String(err)
  }

  // Matrices CRUD
  const getMatrices = async (): Promise<PaginatedResponse<Matrix>> => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.get<PaginatedResponse<Matrix>>(`${API_BASE_URL}/matrices/`)
      return response.data
    } catch (err) {
      error.value = handleError(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const getMatrix = async (id: number): Promise<Matrix> => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.get<Matrix>(`${API_BASE_URL}/matrices/${id}/`)
      return response.data
    } catch (err) {
      error.value = handleError(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const createMatrix = async (matrix: MatrixCreateDTO): Promise<Matrix> => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.post<Matrix>(`${API_BASE_URL}/matrices/`, matrix)
      return response.data
    } catch (err) {
      error.value = handleError(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateMatrix = async (id: number, matrix: Partial<MatrixCreateDTO>): Promise<Matrix> => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.patch<Matrix>(`${API_BASE_URL}/matrices/${id}/`, matrix)
      return response.data
    } catch (err) {
      error.value = handleError(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteMatrix = async (id: number): Promise<void> => {
    loading.value = true
    error.value = null
    try {
      await axios.delete(`${API_BASE_URL}/matrices/${id}/`)
    } catch (err) {
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
    loading.value = true
    error.value = null
    try {
      const response = await axios.get<Stats>(`${API_BASE_URL}/stats/`)
      return response.data
    } catch (err) {
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
