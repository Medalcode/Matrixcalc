/**
 * Tests for MatrixEditor component
 */
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import MatrixEditor from '../MatrixEditor.vue'
import { createI18n } from 'vue-i18n'

// Create i18n instance for tests
const i18n = createI18n({
  legacy: false,
  locale: 'es',
  messages: {
    es: {
      calculator: {
        editor: {
          title: 'Editor de Matriz',
          name: 'Nombre',
          rows: 'Filas',
          cols: 'Columnas',
          namePlaceholder: 'Matriz A',
          quickFill: {
            zeros: 'Llenar con Ceros',
            ones: 'Llenar con Unos',
            identity: 'Matriz Identidad',
            random: 'Valores Aleatorios'
          },
          actions: {
            save: 'Guardar Matriz',
            cancel: 'Cancelar',
            clear: 'Limpiar'
          }
        }
      },
      common: {
        loading: 'Cargando...'
      }
    }
  }
})

describe('MatrixEditor', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('renders correctly', () => {
    const wrapper = mount(MatrixEditor, {
      global: {
        plugins: [i18n]
      }
    })

    expect(wrapper.find('input[placeholder="Matriz A"]').exists()).toBe(true)
    expect(wrapper.text()).toContain('Filas')
    expect(wrapper.text()).toContain('Columnas')
  })

  it('updates matrix name', async () => {
    const wrapper = mount(MatrixEditor, {
      global: {
        plugins: [i18n]
      }
    })

    const nameInput = wrapper.find('input[placeholder="Matriz A"]')
    await nameInput.setValue('Test Matrix')

    expect((nameInput.element as HTMLInputElement).value).toBe('Test Matrix')
  })

  it('updates rows and cols', async () => {
    const wrapper = mount(MatrixEditor, {
      global: {
        plugins: [i18n]
      }
    })

    const rowsInput = wrapper.findAll('input[type="number"]')[0]
    const colsInput = wrapper.findAll('input[type="number"]')[1]

    await rowsInput.setValue('3')
    await colsInput.setValue('4')

    expect((rowsInput.element as HTMLInputElement).value).toBe('3')
    expect((colsInput.element as HTMLInputElement).value).toBe('4')
  })

  it('fills matrix with zeros', async () => {
    const wrapper = mount(MatrixEditor, {
      global: {
        plugins: [i18n]
      }
    })

    const fillZerosButton = wrapper.find('button:contains("Llenar con Ceros")')
    if (fillZerosButton.exists()) {
      await fillZerosButton.trigger('click')
      // Verify matrix cells are filled with zeros
      const inputs = wrapper.findAll('input[type="number"]')
      // Skip first two inputs (rows and cols)
      for (let i = 2; i < inputs.length; i++) {
        expect((inputs[i].element as HTMLInputElement).value).toBe('0')
      }
    }
  })

  it('disables save button when form is invalid', () => {
    const wrapper = mount(MatrixEditor, {
      global: {
        plugins: [i18n]
      },
      props: {
        initialMatrix: {
          name: '',
          rows: 0,
          cols: 0,
          data: []
        }
      }
    })

    const saveButton = wrapper.find('button[type="submit"]')
    expect(saveButton.attributes('disabled')).toBeDefined()
  })

  it('emits save event with matrix data', async () => {
    const wrapper = mount(MatrixEditor, {
      global: {
        plugins: [i18n]
      }
    })

    await wrapper.find('input[placeholder="Matriz A"]').setValue('Test Matrix')
    await wrapper.findAll('input[type="number"]')[0].setValue('2')
    await wrapper.findAll('input[type="number"]')[1].setValue('2')

    const form = wrapper.find('form')
    await form.trigger('submit.prevent')

    expect(wrapper.emitted('save')).toBeTruthy()
  })
})
