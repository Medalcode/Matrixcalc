/**
 * Tests for ResultViewer component
 */
import { describe, it, expect, beforeEach } from 'vitest'
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
        plugins: [i18n]
      },
      props: {
        result: null
      }
    })

    expect(wrapper.text()).toContain('No hay resultados para mostrar')
  })

  it('displays matrix result', () => {
    const wrapper = mount(ResultViewer, {
      global: {
        plugins: [i18n]
      },
      props: {
        result: {
          data: [[1, 2], [3, 4]],
          executionTime: 0.05,
          operation: 'transpose'
        }
      }
    })

    expect(wrapper.text()).toContain('Resultado')
    expect(wrapper.text()).toContain('Tiempo de ejecución')
  })

  it('displays determinant result', () => {
    const wrapper = mount(ResultViewer, {
      global: {
        plugins: [i18n]
      },
      props: {
        result: {
          data: 42,
          executionTime: 0.03,
          operation: 'determinant'
        }
      }
    })

    expect(wrapper.text()).toContain('42')
    expect(wrapper.text()).toContain('Determinante')
  })

  it('displays execution time', () => {
    const wrapper = mount(ResultViewer, {
      global: {
        plugins: [i18n]
      },
      props: {
        result: {
          data: [[1, 2], [3, 4]],
          executionTime: 0.125,
          operation: 'sum'
        }
      }
    })

    expect(wrapper.text()).toContain('0.125')
    expect(wrapper.text()).toContain('Tiempo de ejecución')
  })

  it('displays matrix grid correctly', () => {
    const wrapper = mount(ResultViewer, {
      global: {
        plugins: [i18n]
      },
      props: {
        result: {
          data: [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
          executionTime: 0.05,
          operation: 'multiply'
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
        plugins: [i18n]
      },
      props: {
        result: {
          data: largeMatrix,
          executionTime: 0.5,
          operation: 'multiply'
        }
      }
    })

    expect(wrapper.exists()).toBe(true)
    expect(wrapper.text()).toContain('Tiempo de ejecución')
  })
})
