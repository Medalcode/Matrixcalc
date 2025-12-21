/**
 * Tests for useMatrixAPI composable
 */
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useMatrixAPI } from '../useMatrixAPI'
import axios from 'axios'

// Mock axios
vi.mock('axios')

describe('useMatrixAPI', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  describe('getMatrices', () => {
    it('should fetch matrices successfully', async () => {
      const mockResponse = {
        results: [
          { id: 1, name: 'Matrix A', rows: 2, cols: 2, data: [[1, 2], [3, 4]], created_at: '', updated_at: '' },
          { id: 2, name: 'Matrix B', rows: 2, cols: 2, data: [[5, 6], [7, 8]], created_at: '', updated_at: '' }
        ],
        count: 2,
        next: null,
        previous: null
      }

      vi.mocked(axios.get).mockResolvedValue({ data: mockResponse })

      const { getMatrices, loading, error } = useMatrixAPI()
      
      const result = await getMatrices()

      expect(loading.value).toBe(false)
      expect(error.value).toBeNull()
      expect(result).toEqual(mockResponse)
      expect(axios.get).toHaveBeenCalledWith('http://127.0.0.1:8000/api/matrices/')
    })

    it('should handle fetch error', async () => {
      vi.mocked(axios.get).mockRejectedValue(new Error('Network error'))

      const { getMatrices, error } = useMatrixAPI()
      
      try {
        await getMatrices()
      } catch (e) {
        // Expected to throw
      }

      expect(error.value).toContain('Network error')
    })
  })

  describe('createMatrix', () => {
    it('should create matrix successfully', async () => {
      const newMatrix = {
        name: 'Test Matrix',
        rows: 2,
        cols: 2,
        data: [[1, 2], [3, 4]]
      }
      const createdMatrix = { id: 1, ...newMatrix }

      vi.mocked(axios.post).mockResolvedValue({ data: createdMatrix })

      const { createMatrix, loading, error } = useMatrixAPI()
      
      const result = await createMatrix(newMatrix)

      expect(loading.value).toBe(false)
      expect(error.value).toBeNull()
      expect(result).toEqual(createdMatrix)
      expect(axios.post).toHaveBeenCalledWith(
        'http://127.0.0.1:8000/api/matrices/',
        newMatrix
      )
    })

    it('should handle create error', async () => {
      vi.mocked(axios.post).mockRejectedValue(new Error('Validation error'))

      const { createMatrix, error } = useMatrixAPI()
      
      try {
        await createMatrix({
          name: 'Invalid',
          rows: 0,
          cols: 2,
          data: []
        })
      } catch (e) {
        // Expected to throw
      }

      expect(error.value).toContain('Validation error')
    })
  })

  describe('updateMatrix', () => {
    it('should update matrix successfully', async () => {
      const updatedMatrix = {
        id: 1,
        name: 'Updated Matrix',
        rows: 2,
        cols: 2,
        data: [[9, 8], [7, 6]],
        created_at: '',
        updated_at: ''
      }

      vi.mocked(axios.patch).mockResolvedValue({ data: updatedMatrix })

      const { updateMatrix, loading, error } = useMatrixAPI()
      
      const result = await updateMatrix(1, updatedMatrix)

      expect(loading.value).toBe(false)
      expect(error.value).toBeNull()
      expect(result).toEqual(updatedMatrix)
      expect(axios.patch).toHaveBeenCalledWith(
        'http://127.0.0.1:8000/api/matrices/1/',
        updatedMatrix
      )
    })
  })

  describe('deleteMatrix', () => {
    it('should delete matrix successfully', async () => {
      vi.mocked(axios.delete).mockResolvedValue({ data: null })

      const { deleteMatrix, loading, error } = useMatrixAPI()
      
      await deleteMatrix(1)

      expect(loading.value).toBe(false)
      expect(error.value).toBeNull()
      expect(axios.delete).toHaveBeenCalledWith(
        'http://127.0.0.1:8000/api/matrices/1/'
      )
    })

    it('should handle delete error', async () => {
      vi.mocked(axios.delete).mockRejectedValue(new Error('Not found'))

      const { deleteMatrix, error } = useMatrixAPI()
      
      try {
        await deleteMatrix(999)
      } catch (e) {
        // Expected to throw
      }

      expect(error.value).toContain('Not found')
    })
  })

  describe('sumMatrices', () => {
    it('should perform sum operation successfully', async () => {
      const result = {
        data: [[6, 8], [10, 12]],
        executionTime: 0.05,
        operation: 'sum'
      }

      vi.mocked(axios.post).mockResolvedValue({ data: result })

      const { sumMatrices, loading, error } = useMatrixAPI()
      
      const response = await sumMatrices(1, 2)

      expect(loading.value).toBe(false)
      expect(error.value).toBeNull()
      expect(response).toEqual(result)
    })

    it('should handle operation error', async () => {
      vi.mocked(axios.post).mockRejectedValue(
        new Error('Matrix dimensions do not match')
      )

      const { sumMatrices, error } = useMatrixAPI()
      
      try {
        await sumMatrices(1, 2)
      } catch (e) {
        // Expected to throw
      }

      expect(error.value).toContain('dimensions')
    })
  })

  describe('getStats', () => {
    it('should fetch statistics successfully', async () => {
      const mockStats = {
        total_matrices: 10,
        total_operations: 50,
        average_execution_time: 0.03,
        total_storage: 1024,
        operations_by_type: {
          sum: 15,
          multiply: 10,
          transpose: 25
        }
      }

      vi.mocked(axios.get).mockResolvedValue({ data: mockStats })

      const { getStats, loading, error } = useMatrixAPI()
      
      const result = await getStats()

      expect(loading.value).toBe(false)
      expect(error.value).toBeNull()
      expect(result).toEqual(mockStats)
      expect(axios.get).toHaveBeenCalledWith('http://127.0.0.1:8000/api/stats/')
    })
  })

  describe('exportMatrixCSV', () => {
    it('should export CSV successfully', async () => {
      const mockBlob = new Blob(['test data'], { type: 'text/csv' })
      vi.mocked(axios.get).mockResolvedValue({ data: mockBlob })

      const { exportMatrixCSV } = useMatrixAPI()
      
      await exportMatrixCSV()

      expect(axios.get).toHaveBeenCalled()
    })
  })

  describe('importMatrixCSV', () => {
    it('should import CSV successfully', async () => {
      const mockFile = new File(['test'], 'test.csv', { type: 'text/csv' })
      const response = { created: 1, updated: 0, errors: [] }

      vi.mocked(axios.post).mockResolvedValue({ data: response })

      const { importMatrixCSV } = useMatrixAPI()
      
      const result = await importMatrixCSV(mockFile)

      expect(result).toEqual(response)
      expect(axios.post).toHaveBeenCalled()
    })
  })
})
