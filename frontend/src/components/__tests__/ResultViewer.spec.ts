/**
 * Tests for ResultViewer component
 */
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import ResultViewer from '../ResultViewer.vue'
import { createI18n } from 'vue-i18n'

const i18n = createI18n({
  legacy: false,
  locale: 'es',
  messages: {
    es: {
      calculator: {
        result: {
          title: 'Resultado',
          noResult: 'No hay resultados para mostrar',
          executionTime: 'Tiempo de ejecución'
        }
      }
    }
  }
})

describe('ResultViewer', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })
  it('renders empty state when no result', () => {
    const wrapper = mount(ResultViewer, {
      global: {
        plugins: [i18n],
        mocks: {
          t: (key: string) => key
        }
      },
      props: {
        matrix: undefined
      }
    })

    expect(wrapper.text()).toContain('calculator.result.noResult')
  })

  it('displays matrix result', () => {
    const wrapper = mount(ResultViewer, {
      global: {
        plugins: [i18n],
        mocks: {
          t: (key: string) => key
        }
      },
      props: {
        matrix: {
          id: 1,
          name: 'Test Matrix',
          rows: 2,
          cols: 2,
          data: [[1, 2], [3, 4]],
          created_at: '2025-12-21T00:00:00Z',
          updated_at: '2025-12-21T00:00:00Z'
        }
      }
    })

    expect(wrapper.text()).toContain('calculator.result.title')
    expect(wrapper.text()).toContain('Test Matrix')
  })

  it('displays determinant result', () => {
    const wrapper = mount(ResultViewer, {
      global: {
        plugins: [i18n],
        mocks: {
          t: (key: string) => key
        }
      },
      props: {
        matrix: {
          id: 1,
          name: 'Determinant Result',
          rows: 1,
          cols: 1,
          data: [[42]],
          created_at: '2025-12-21T00:00:00Z',
          updated_at: '2025-12-21T00:00:00Z'
        },
        operation: {
          id: 1,
          operation_type: 'DETERMINANT',
          matrix_a: 1,
          result_matrix: 1,
          execution_time: 0.03,
          created_at: '2025-12-21T00:00:00Z'
        }
      }
    })

    expect(wrapper.text()).toContain('42')
    expect(wrapper.text()).toContain('Determinante')
  })

  it('displays execution time', () => {
    const wrapper = mount(ResultViewer, {
      global: {
        plugins: [i18n],
        mocks: {
          t: (key: string) => key
        }
      },
      props: {
        matrix: {
          id: 1,
          name: 'Sum Result',
          rows: 2,
          cols: 2,
          data: [[1, 2], [3, 4]],
          created_at: '2025-12-21T00:00:00Z',
          updated_at: '2025-12-21T00:00:00Z'
        },
        operation: {
          id: 1,
          operation_type: 'SUM',
          matrix_a: 1,
          matrix_b: 2,
          result_matrix: 1,
          execution_time: 0.125,
          created_at: '2025-12-21T00:00:00Z'
        }
      }
    })

    expect(wrapper.text()).toContain('0.125')
  })

  it('displays matrix grid correctly', () => {
    const wrapper = mount(ResultViewer, {
      global: {
        plugins: [i18n],
        mocks: {
          t: (key: string) => key
        }
      },
      props: {
        matrix: {
          id: 1,
          name: 'Test Matrix',
          rows: 3,
          cols: 3,
          data: [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
          created_at: '2025-12-21T00:00:00Z',
          updated_at: '2025-12-21T00:00:00Z'
        }
      }
    })

    // Check that all matrix values are displayed
    expect(wrapper.html()).toContain('1')
    expect(wrapper.html()).toContain('2')
    expect(wrapper.html()).toContain('3')
    expect(wrapper.html()).toContain('4')
    expect(wrapper.html()).toContain('5')
    expect(wrapper.html()).toContain('6')
    expect(wrapper.html()).toContain('7')
    expect(wrapper.html()).toContain('8')
    expect(wrapper.html()).toContain('9')
  })

  it('handles large matrices', () => {
    const largeMatrix = Array(10).fill(0).map((_, i) => 
      Array(10).fill(0).map((_, j) => i * 10 + j)
    )

    const wrapper = mount(ResultViewer, {
      global: {
        plugins: [i18n],
        mocks: {
          t: (key: string) => key
        }
      },
      props: {
        matrix: {
          id: 1,
          name: 'Large Matrix',
          rows: 10,
          cols: 10,
          data: largeMatrix,
          created_at: '2025-12-21T00:00:00Z',
          updated_at: '2025-12-21T00:00:00Z'
        },
        operation: {
          id: 1,
          operation_type: 'MULTIPLY',
          matrix_a: 1,
          matrix_b: 2,
          result_matrix: 1,
          execution_time: 0.5,
          created_at: '2025-12-21T00:00:00Z'
        }
      }
    })

    expect(wrapper.exists()).toBe(true)
    expect(wrapper.text()).toContain('0.5')
  })
})
