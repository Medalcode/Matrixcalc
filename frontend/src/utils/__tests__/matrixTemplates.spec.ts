import { describe, it, expect } from 'vitest'
import { matrixTemplates, getTemplateByName } from '../matrixTemplates'

describe('matrixTemplates utility', () => {
  it('contains template definitions', () => {
    expect(matrixTemplates.length).toBeGreaterThan(0)
  })

  it('retrieves template by name', () => {
    const zeros = getTemplateByName('Zeros')
    expect(zeros).toBeDefined()
    expect(zeros?.name).toBe('Zeros')
  })

  it('generates zero matrix data correctly', () => {
    const zeros = getTemplateByName('Zeros')
    if (zeros) {
      const data = zeros.generateData(2, 3)
      expect(data).toEqual([
        [0, 0, 0],
        [0, 0, 0],
      ])
    }
  })

  it('generates identity matrix data correctly', () => {
    const identity = getTemplateByName('Identity')
    if (identity) {
      const data = identity.generateData(2, 2)
      expect(data).toEqual([
        [1, 0],
        [0, 1],
      ])
    }
  })
})
