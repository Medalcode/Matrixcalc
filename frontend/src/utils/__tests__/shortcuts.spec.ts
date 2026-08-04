import { describe, it, expect } from 'vitest'
import {
  formatShortcutKey,
  getShortcutsByCategory,
  getCategories,
  getCategoryName,
  shortcuts,
} from '../shortcuts'

describe('shortcuts utility', () => {
  it('formats mod key string correctly', () => {
    const formatted = formatShortcutKey('mod+s')
    expect(formatted).toBeDefined()
    expect(typeof formatted).toBe('string')
  })

  it('filters shortcuts by category correctly', () => {
    const generalShortcuts = getShortcutsByCategory('general')
    expect(generalShortcuts.every((s) => s.category === 'general')).toBe(true)
    expect(generalShortcuts.length).toBeGreaterThan(0)
  })

  it('returns all categories', () => {
    const categories = getCategories()
    expect(categories).toEqual(['general', 'navigation', 'matrix', 'operations'])
  })

  it('returns valid category display names', () => {
    expect(getCategoryName('general')).toBe('General')
    expect(getCategoryName('navigation')).toBe('Navegación')
    expect(getCategoryName('matrix')).toBe('Matrices')
    expect(getCategoryName('operations')).toBe('Operaciones')
  })

  it('contains valid shortcut definitions', () => {
    expect(shortcuts.length).toBeGreaterThan(0)
    shortcuts.forEach((s) => {
      expect(s.key).toBeDefined()
      expect(s.description).toBeDefined()
      expect(s.action).toBeDefined()
    })
  })
})
