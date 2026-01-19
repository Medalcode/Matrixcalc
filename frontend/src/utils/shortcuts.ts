/**
 * Keyboard Shortcuts Configuration
 * Defines all available keyboard shortcuts for MatrixCalc
 */

export interface Shortcut {
  key: string
  description: string
  category: 'general' | 'navigation' | 'matrix' | 'operations'
  action: string
}

export const shortcuts: Shortcut[] = [
  // General shortcuts
  {
    key: 'mod+s',
    description: 'Guardar matriz actual',
    category: 'general',
    action: 'save'
  },
  {
    key: 'mod+n',
    description: 'Nueva matriz',
    category: 'general',
    action: 'new'
  },
  {
    key: 'mod+k',
    description: 'Abrir Command Palette',
    category: 'general',
    action: 'commandPalette'
  },
  {
    key: 'mod+z',
    description: 'Deshacer',
    category: 'general',
    action: 'undo'
  },
  {
    key: 'mod+shift+z',
    description: 'Rehacer',
    category: 'general',
    action: 'redo'
  },
  {
    key: 'mod+/',
    description: 'Mostrar ayuda de atajos',
    category: 'general',
    action: 'showHelp'
  },
  {
    key: 'esc',
    description: 'Cerrar modal/dropdown',
    category: 'general',
    action: 'close'
  },
  {
    key: 'mod+d',
    description: 'Toggle Dark Mode',
    category: 'general',
    action: 'toggleTheme'
  },

  // Navigation shortcuts
  {
    key: 'alt+1',
    description: 'Ir a Calculadora',
    category: 'navigation',
    action: 'goToCalculator'
  },
  {
    key: 'alt+2',
    description: 'Ir a Estadísticas',
    category: 'navigation',
    action: 'goToStats'
  },
  {
    key: 'alt+3',
    description: 'Ir a Historial',
    category: 'navigation',
    action: 'goToHistory'
  },
  {
    key: 'alt+4',
    description: 'Ir a Documentación',
    category: 'navigation',
    action: 'goToDocs'
  },
  {
    key: 'alt+5',
    description: 'Ir a Acerca de',
    category: 'navigation',
    action: 'goToAbout'
  },

  // Matrix operations
  {
    key: 'enter',
    description: 'Ejecutar operación seleccionada',
    category: 'operations',
    action: 'execute'
  },
  {
    key: 'mod+e',
    description: 'Exportar matriz actual',
    category: 'matrix',
    action: 'export'
  },
  {
    key: 'mod+i',
    description: 'Importar matriz',
    category: 'matrix',
    action: 'import'
  },
  {
    key: 'del',
    description: 'Eliminar matriz seleccionada',
    category: 'matrix',
    action: 'delete'
  }
]

/**
 * Get formatted shortcut key for display
 * Converts 'mod' to Cmd (Mac) or Ctrl (Windows/Linux)
 */
export function formatShortcutKey(key: string): string {
  const isMac = navigator.platform.toUpperCase().indexOf('MAC') >= 0
  
  return key
    .replace('mod', isMac ? '⌘' : 'Ctrl')
    .replace('shift', isMac ? '⇧' : 'Shift')
    .replace('alt', isMac ? '⌥' : 'Alt')
    .replace('ctrl', isMac ? '⌃' : 'Ctrl')
    .split('+')
    .map(k => k.charAt(0).toUpperCase() + k.slice(1))
    .join(isMac ? '' : '+')
}

/**
 * Get shortcuts by category
 */
export function getShortcutsByCategory(category: Shortcut['category']): Shortcut[] {
  return shortcuts.filter(s => s.category === category)
}

/**
 * Get all categories
 */
export function getCategories(): Array<Shortcut['category']> {
  return ['general', 'navigation', 'matrix', 'operations']
}

/**
 * Get category display name
 */
export function getCategoryName(category: Shortcut['category']): string {
  const names: Record<Shortcut['category'], string> = {
    general: 'General',
    navigation: 'Navegación',
    matrix: 'Matrices',
    operations: 'Operaciones'
  }
  return names[category]
}
