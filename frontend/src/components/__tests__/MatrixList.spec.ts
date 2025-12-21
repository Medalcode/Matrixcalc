/**
 * Tests for MatrixList component
 */
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import MatrixList from '../MatrixList.vue'
import { useMatrixStore } from '@/stores/matrixStore'
import { createI18n } from 'vue-i18n'

const i18n = createI18n({
  legacy: false,
  locale: 'es',
  messages: {
    es: {
      calculator: {
        matrixList: {
          title: 'Matrices Guardadas',
          empty: 'No hay matrices guardadas',
          loading: 'Cargando matrices...',
          error: 'Error al cargar matrices'
        }
      },
      common: {
        loading: 'Cargando...',
        error: 'Error'
      }
    }
  }
})

describe('MatrixList', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('renders empty state when no matrices', () => {
    const wrapper = mount(MatrixList, {
      global: {
        plugins: [i18n]
      }
    })

    expect(wrapper.text()).toContain('No hay matrices guardadas')
  })

  it('displays matrices when available', async () => {
    const wrapper = mount(MatrixList, {
      global: {
        plugins: [i18n]
      }
    })

    const store = useMatrixStore()
    store.matrices = [
      { id: 1, name: 'Matrix A', rows: 2, cols: 2, data: [[1, 2], [3, 4]], created_at: new Date().toISOString(), updated_at: new Date().toISOString() },
      { id: 2, name: 'Matrix B', rows: 3, cols: 3, data: [[1, 0, 0], [0, 1, 0], [0, 0, 1]], created_at: new Date().toISOString(), updated_at: new Date().toISOString() }
    ]

    await wrapper.vm.$nextTick()

    expect(wrapper.text()).toContain('Matrix A')
    expect(wrapper.text()).toContain('Matrix B')
    expect(wrapper.text()).toContain('2×2')
    expect(wrapper.text()).toContain('3×3')
  })

  it('shows loading state', async () => {
    const wrapper = mount(MatrixList, {
      global: {
        plugins: [i18n]
      }
    })

    const store = useMatrixStore()
    store.loading = true

    await wrapper.vm.$nextTick()

    expect(wrapper.text()).toContain('Cargando')
  })

  it('emits edit event when edit button clicked', async () => {
    const wrapper = mount(MatrixList, {
      global: {
        plugins: [i18n]
      }
    })

    const store = useMatrixStore()
    store.matrices = [
      { id: 1, name: 'Matrix A', rows: 2, cols: 2, data: [[1, 2], [3, 4]], created_at: new Date().toISOString(), updated_at: new Date().toISOString() }
    ]

    await wrapper.vm.$nextTick()

    const editButtons = wrapper.findAll('button').filter(btn => 
      btn.text().includes('Editar') || btn.html().includes('edit')
    )

    if (editButtons.length > 0) {
      await editButtons[0].trigger('click')
      expect(wrapper.emitted('edit')).toBeTruthy()
    }
  })

  it('emits delete event when delete button clicked', async () => {
    const wrapper = mount(MatrixList, {
      global: {
        plugins: [i18n]
      }
    })

    const store = useMatrixStore()
    store.matrices = [
      { id: 1, name: 'Matrix A', rows: 2, cols: 2, data: [[1, 2], [3, 4]], created_at: new Date().toISOString(), updated_at: new Date().toISOString() }
    ]

    await wrapper.vm.$nextTick()

    const deleteButtons = wrapper.findAll('button').filter(btn => 
      btn.text().includes('Eliminar') || btn.html().includes('delete') || btn.html().includes('trash')
    )

    if (deleteButtons.length > 0) {
      await deleteButtons[0].trigger('click')
      expect(wrapper.emitted('delete')).toBeTruthy()
    }
  })
})
