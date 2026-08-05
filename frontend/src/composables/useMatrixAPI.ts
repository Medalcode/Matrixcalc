/**
 * Composable para interactuar con la API REST de MatrixCalc
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

  const handleError = (err: unknown): string => {
    if (axios.isAxiosError(err)) {
      const axiosError = err as AxiosError<Record<string, unknown>>
      // Sin respuesta del servidor → backend no disponible
      if (!axiosError.response) {
        return 'No se puede conectar con el servidor. Asegúrate de que el backend está en ejecución.'
      }
      const data = axiosError.response.data
      if (!data) return axiosError.message

      if (typeof data === 'string') return data
      if (typeof data.error === 'string') return data.error
      if (typeof data.detail === 'string') return data.detail

      if (typeof data === 'object') {
        const messages: string[] = []
        for (const [key, val] of Object.entries(data)) {
          if (Array.isArray(val)) {
            messages.push(`${key}: ${val.join(', ')}`)
          } else if (typeof val === 'string') {
            messages.push(`${key}: ${val}`)
          }
        }
        if (messages.length > 0) return messages.join(' | ')
        return JSON.stringify(data)
      }
      return axiosError.message
    }
    return String(err)
  }

  const withLoading = async <T>(fn: () => Promise<T>): Promise<T> => {
    loading.value = true
    error.value = null
    try {
      return await fn()
    } catch (err) {
      error.value = handleError(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  // ---------- Matrices CRUD ----------

  const getMatrices = () => withLoading(() => 
    axios.get<PaginatedResponse<Matrix>>(`${API_BASE_URL}/matrices/`).then(res => res.data)
  )

  const getMatrix = (id: number) => withLoading(() => 
    axios.get<Matrix>(`${API_BASE_URL}/matrices/${id}/`).then(res => res.data)
  )

  const createMatrix = (matrix: MatrixCreateDTO) => withLoading(() => 
    axios.post<Matrix>(`${API_BASE_URL}/matrices/`, matrix).then(res => res.data)
  )

  const updateMatrix = (id: number, matrix: Partial<MatrixCreateDTO>) => withLoading(() => 
    axios.patch<Matrix>(`${API_BASE_URL}/matrices/${id}/`, matrix).then(res => res.data)
  )

  const deleteMatrix = (id: number) => withLoading(() => 
    axios.delete(`${API_BASE_URL}/matrices/${id}/`).then(() => undefined)
  )

  const exportMatrixCSV = (id: number) => withLoading(() => 
    axios.get(`${API_BASE_URL}/matrices/${id}/export_csv/`, { responseType: 'blob' }).then(res => res.data)
  )

  const importMatrixCSV = (file: File, name: string) => withLoading(() => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('name', name)
    return axios.post<Matrix>(
      `${API_BASE_URL}/matrices/import_csv/`,
      formData,
      { headers: { 'Content-Type': 'multipart/form-data' } }
    ).then(res => res.data)
  })

  // ---------- Operations ----------

  const _operate = (endpoint: string, request: OperationRequest) => withLoading(() => 
    axios.post<Operation>(`${API_BASE_URL}/operations/${endpoint}/`, request).then(res => res.data)
  )

  const getOperations = () => withLoading(() => 
    axios.get<PaginatedResponse<Operation>>(`${API_BASE_URL}/operations-history/`).then(res => res.data)
  )

  const sumMatrices = (request: OperationRequest) => _operate('sum', request)
  const subtractMatrices = (request: OperationRequest) => _operate('subtract', request)
  const multiplyMatrices = (request: OperationRequest) => _operate('multiply', request)
  const inverseMatrix = (request: OperationRequest) => _operate('inverse', request)
  const determinantMatrix = (request: OperationRequest) => _operate('determinant', request)
  const transposeMatrix = (request: OperationRequest) => _operate('transpose', request)
  const calculateRank = (request: OperationRequest) => _operate('rank', request)
  const calculateEigenvalues = (request: OperationRequest) => _operate('eigenvalues', request)
  const calculateSVD = (request: OperationRequest) => _operate('svd', request)
  const calculateQR = (request: OperationRequest) => _operate('qr', request)
  const calculateCholesky = (request: OperationRequest) => _operate('cholesky', request)

  // ---------- Stats ----------

  const getStats = () => withLoading(() => 
    axios.get<Stats>(`${API_BASE_URL}/stats/`).then(res => res.data)
  )

  return {
    loading,
    error,
    getMatrices,
    getMatrix,
    createMatrix,
    updateMatrix,
    deleteMatrix,
    exportMatrixCSV,
    importMatrixCSV,
    getOperations,
    sumMatrices,
    subtractMatrices,
    multiplyMatrices,
    inverseMatrix,
    determinantMatrix,
    transposeMatrix,
    calculateRank,
    calculateEigenvalues,
    calculateSVD,
    calculateQR,
    calculateCholesky,
    getStats
  }
}
