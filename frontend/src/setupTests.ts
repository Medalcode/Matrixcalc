import { vi } from 'vitest'

vi.mock('axios', () => {
  return {
    default: {
      get: vi.fn(() => Promise.resolve({ data: { results: [], count: 0 } })),
      post: vi.fn((url: string, data: any) => {
        if (url?.includes('/operations/')) {
          return Promise.resolve({ data: { id: 1, operation_type: 'SUM', result_matrix: 1, execution_time_ms: 10 } })
        }
        return Promise.resolve({ data: { id: 1, name: 'Mocked', rows: 2, cols: 2, data: [[0,0],[0,0]] } })
      }),
      patch: vi.fn(() => Promise.resolve({ data: {} })),
      delete: vi.fn(() => Promise.resolve({ data: {} })),
      isAxiosError: vi.fn(() => false)
    }
  }
})

// Mock document.getElementById for animations to avoid console warnings
const originalGetElementById = document.getElementById.bind(document)
document.getElementById = (id: string) => {
  const el = originalGetElementById(id)
  if (!el && id === 'matrix-grid') {
    // Return a dummy element to prevent warnings during tests
    const dummy = document.createElement('div')
    dummy.id = id
    return dummy
  }
  return el
}
