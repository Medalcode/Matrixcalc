/**
 * LaTeX Matrix Exporter
 * Exports matrices in various LaTeX formats
 */

export type LaTeXFormat = 'bmatrix' | 'pmatrix' | 'vmatrix' | 'Vmatrix' | 'matrix' | 'array'

export interface LaTeXExportOptions {
  format: LaTeXFormat
  precision?: number
  alignment?: 'l' | 'c' | 'r'
  includeWrapper?: boolean
}

/**
 * Format a number for LaTeX output
 */
function formatNumber(value: number, precision: number = 2): string {
  // Handle special cases
  if (!isFinite(value)) return '\\infty'
  if (isNaN(value)) return '\\text{NaN}'
  
  // Round to precision
  const rounded = Number(value.toFixed(precision))
  
  // Remove trailing zeros
  return rounded.toString().replace(/\.?0+$/, '')
}

/**
 * Get LaTeX environment name for format
 */
function getEnvironment(format: LaTeXFormat): string {
  return format
}

/**
 * Get LaTeX delimiters for format
 */
function getDelimiters(format: LaTeXFormat): { left: string; right: string } {
  const delimiters: Record<LaTeXFormat, { left: string; right: string }> = {
    bmatrix: { left: '[', right: ']' },
    pmatrix: { left: '(', right: ')' },
    vmatrix: { left: '|', right: '|' },
    Vmatrix: { left: '\\|', right: '\\|' },
    matrix: { left: '', right: '' },
    array: { left: '', right: '' }
  }
  return delimiters[format]
}

/**
 * Export matrix to LaTeX format
 */
export function exportToLaTeX(
  data: number[][],
  options: LaTeXExportOptions = { format: 'bmatrix' }
): string {
  const {
    format = 'bmatrix',
    precision = 2,
    alignment = 'c',
    includeWrapper = true
  } = options

  if (!data || data.length === 0) {
    throw new Error('Matrix data is empty')
  }

  const firstRow = data[0]
  if (!firstRow || firstRow.length === 0) {
    throw new Error('Matrix data is invalid')
  }

  const rows = data.length
  const cols = firstRow.length

  // Build LaTeX string
  let latex = ''

  // Add wrapper if requested
  if (includeWrapper) {
    latex += '\\[\n'
  }

  // Start environment
  if (format === 'array') {
    // Array format needs column specification
    const colSpec = alignment.repeat(cols)
    latex += `\\begin{array}{${colSpec}}\n`
  } else {
    latex += `\\begin{${getEnvironment(format)}}\n`
  }

  // Add matrix rows
  for (let i = 0; i < rows; i++) {
    const row = data[i]
    if (!row) continue
    
    const formattedRow = row.map(val => formatNumber(val, precision)).join(' & ')
    latex += '  ' + formattedRow
    
    // Add line break except for last row
    if (i < rows - 1) {
      latex += ' \\\\\n'
    } else {
      latex += '\n'
    }
  }

  // End environment
  latex += `\\end{${getEnvironment(format)}}\n`

  // Close wrapper if requested
  if (includeWrapper) {
    latex += '\\]\n'
  }

  return latex
}

/**
 * Export matrix with label and equation number
 */
export function exportToLaTeXEquation(
  data: number[][],
  label: string,
  options: LaTeXExportOptions = { format: 'bmatrix' }
): string {
  const matrixLatex = exportToLaTeX(data, { ...options, includeWrapper: false })
  
  return `\\begin{equation}\\label{${label}}\n${matrixLatex}\\end{equation}\n`
}

/**
 * Export matrix operation (e.g., A + B = C)
 */
export function exportOperation(
  matrixA: number[][],
  matrixB: number[][] | null,
  result: number[][],
  operation: string,
  options: LaTeXExportOptions = { format: 'bmatrix' }
): string {
  const optionsNoWrapper = { ...options, includeWrapper: false }
  
  let latex = '\\[\n'
  latex += exportToLaTeX(matrixA, optionsNoWrapper)
  
  if (matrixB) {
    latex += ` ${operation} `
    latex += exportToLaTeX(matrixB, optionsNoWrapper)
  }
  
  latex += ' = '
  latex += exportToLaTeX(result, optionsNoWrapper)
  latex += '\\]\n'
  
  return latex
}

/**
 * Get format description
 */
export function getFormatDescription(format: LaTeXFormat): string {
  const descriptions: Record<LaTeXFormat, string> = {
    bmatrix: 'Matriz con corchetes [ ]',
    pmatrix: 'Matriz con paréntesis ( )',
    vmatrix: 'Determinante con barras | |',
    Vmatrix: 'Norma con doble barra || ||',
    matrix: 'Matriz sin delimitadores',
    array: 'Array personalizable'
  }
  return descriptions[format]
}

/**
 * Get all available formats
 */
export function getAvailableFormats(): LaTeXFormat[] {
  return ['bmatrix', 'pmatrix', 'vmatrix', 'Vmatrix', 'matrix', 'array']
}

/**
 * Copy LaTeX to clipboard
 */
export async function copyToClipboard(latex: string): Promise<boolean> {
  try {
    await navigator.clipboard.writeText(latex)
    return true
  } catch (error) {
    console.error('Failed to copy to clipboard:', error)
    return false
  }
}

/**
 * Download LaTeX as .tex file
 */
export function downloadAsFile(latex: string, filename: string = 'matrix.tex'): void {
  const blob = new Blob([latex], { type: 'text/plain' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  link.click()
  URL.revokeObjectURL(url)
}
