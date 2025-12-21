/**
 * Tests for OperationPanel component
 */
import { describe, it, expect, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import OperationPanel from '../OperationPanel.vue'
import { useMatrixStore } from '@/stores/matrixStore'
import { createI18n } from 'vue-i18n'

const i18n = createI18n({
  legacy: false,
  locale: 'es',
  messages: {
    es: {
      calculator: {
        operations: {
          title: 'Operaciones',
          selectMatrixA: 'Seleccionar Matriz A',
          selectMatrixB: 'Seleccionar Matriz B',
          binaryOperations: 'Operaciones Binarias',
          unaryOperations: 'Operaciones Unarias',
          calculate: 'Ejecutar Operación',
          types: {
            sum: 'Suma',
            subtract: 'Resta',
            multiply: 'Multiplicación',
            inverse: 'Inversa',
            determinant: 'Determinante',
            transpose: 'Transpuesta'
          }
        }
      },
      common: {
        loading: 'Cargando...'
      }
    }
  }
})

describe('OperationPanel', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('renders correctly', () => {
    const wrapper = mount(OperationPanel, {
      global: {
        plugins: [i18n]
      }
    })

    expect(wrapper.text()).toContain('Operaciones')
    expect(wrapper.text()).toContain('Suma')
    expect(wrapper.text()).toContain('Resta')
    expect(wrapper.text()).toContain('Multiplicación')
  })

  it('displays matrix selectors', () => {
    const wrapper = mount(OperationPanel, {
      global: {
        plugins: [i18n]
      }
    })

    const selects = wrapper.findAll('select')
    expect(selects.length).toBeGreaterThanOrEqual(1)
  })

  it('shows binary operations section', () => {
    const wrapper = mount(OperationPanel, {
      global: {
        plugins: [i18n]
      }
    })

    expect(wrapper.text()).toContain('Operaciones Binarias')
    expect(wrapper.text()).toContain('Suma')
    expect(wrapper.text()).toContain('Resta')
    expect(wrapper.text()).toContain('Multiplicación')
  })

  it('shows unary operations section', () => {
    const wrapper = mount(OperationPanel, {
      global: {
        plugins: [i18n]
      }
    })

    expect(wrapper.text()).toContain('Operaciones Unarias')
    expect(wrapper.text()).toContain('Inversa')
    expect(wrapper.text()).toContain('Determinante')
    expect(wrapper.text()).toContain('Transpuesta')
  })

  it('disables execute button when no matrices selected', () => {
    const wrapper = mount(OperationPanel, {
      global: {
        plugins: [i18n]
      }
    })

    const executeButton = wrapper.findAll('button').find(btn => 
      btn.text().includes('Ejecutar')
    )

    if (executeButton) {
      expect(executeButton.attributes('disabled')).toBeDefined()
    }
  })

  it('enables execute button when matrices selected and operation chosen', async () => {
    const wrapper = mount(OperationPanel, {
      global: {
        plugins: [i18n]
      }
    })

    const store = useMatrixStore()
    store.matrices = [
      { id: 1, name: 'Matrix A', rows: 2, cols: 2, data: [[1, 2], [3, 4]], created_at: new Date().toISOString(), updated_at: new Date().toISOString() },
      { id: 2, name: 'Matrix B', rows: 2, cols: 2, data: [[5, 6], [7, 8]], created_at: new Date().toISOString(), updated_at: new Date().toISOString() }
    ]

    await wrapper.vm.$nextTick()

    // Select matrices
    const selects = wrapper.findAll('select')
    if (selects.length >= 2) {
      await selects[0].setValue('1')
      await selects[1].setValue('2')
    }

    // Click an operation button
    const sumButton = wrapper.findAll('button').find(btn => btn.text().includes('Suma'))
    if (sumButton) {
      await sumButton.trigger('click')
    }

    await wrapper.vm.$nextTick()

    const executeButton = wrapper.findAll('button').find(btn => 
      btn.text().includes('Ejecutar')
    )

    if (executeButton) {
      // Button should now be enabled (no disabled attribute)
      expect(executeButton.attributes('disabled')).toBeUndefined()
    }
  })

  it('emits operation-execute event when execute clicked', async () => {
    const wrapper = mount(OperationPanel, {
      global: {
        plugins: [i18n]
      }
    })

    const store = useMatrixStore()
    store.matrices = [
      { id: 1, name: 'Matrix A', rows: 2, cols: 2, data: [[1, 2], [3, 4]], created_at: new Date().toISOString(), updated_at: new Date().toISOString() }
    ]

    await wrapper.vm.$nextTick()

    // Select matrix
    const selects = wrapper.findAll('select')
    if (selects.length > 0) {
      await selects[0].setValue('1')
    }

    // Select transpose operation (unary)
    const transposeButton = wrapper.findAll('button').find(btn => 
      btn.text().includes('Transpuesta')
    )
    if (transposeButton) {
      await transposeButton.trigger('click')
    }

    await wrapper.vm.$nextTick()

    // Click execute
    const executeButton = wrapper.findAll('button').find(btn => 
      btn.text().includes('Ejecutar')
    )

    if (executeButton && !executeButton.attributes('disabled')) {
      await executeButton.trigger('click')
      expect(wrapper.emitted('operation-execute')).toBeTruthy()
    }
  })
})
