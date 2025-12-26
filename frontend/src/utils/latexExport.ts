/**
 * 🎯 LaTeX Export Utilities
 * MatrixCalc v3.0 - Export matrices to LaTeX format
 */

import type { Matrix } from '@/types/matrix';

/**
 * Export a matrix to LaTeX format
 */
export function exportToLaTeX(matrix: Matrix): string {
  const { rows, cols, data, name } = matrix;
  
  // Start LaTeX matrix environment
  let latex = `% Matrix: ${name}\n`;
  latex += `% Dimensions: ${rows} × ${cols}\n\n`;
  latex += `\\begin{bmatrix}\n`;
  
  // Add matrix data
  for (let i = 0; i < rows; i++) {
    const row = data[i];
    if (!row) continue;
    const rowStr = row.map(formatNumber).join(' & ');
    latex += `  ${rowStr}`;
    
    if (i < rows - 1) {
      latex += ' \\\\';
    }
    latex += '\n';
  }
  
  latex += `\\end{bmatrix}`;
  
  return latex;
}

/**
 * Export multiple matrices to LaTeX
 */
export function exportMultipleToLaTeX(matrices: Matrix[]): string {
  let latex = '% MatrixCalc - LaTeX Export\n';
  latex += `% Generated: ${new Date().toISOString()}\n\n`;
  
  matrices.forEach((matrix, index) => {
    if (index > 0) latex += '\n\n';
    latex += `% Matrix ${index + 1}: ${matrix.name}\n`;
    latex += exportToLaTeX(matrix);
  });
  
  return latex;
}

/**
 * Export matrix with equation format
 */
export function exportWithEquation(matrix: Matrix, variableName: string = 'A'): string {
  const matrixLatex = exportToLaTeX(matrix);
  return `${variableName} = ${matrixLatex}`;
}

/**
 * Export complete LaTeX document
 */
export function exportAsDocument(matrix: Matrix): string {
  let latex = '\\documentclass{article}\n';
  latex += '\\usepackage{amsmath}\n';
  latex += '\\usepackage{amssymb}\n\n';
  latex += '\\begin{document}\n\n';
  latex += `\\section*{Matrix: ${matrix.name}}\n\n`;
  latex += `Dimensions: ${matrix.rows} \\times ${matrix.cols}\n\n`;
  latex += '\\[\n';
  latex += exportWithEquation(matrix, matrix.name.replace(/\s+/g, ''));
  latex += '\n\\]\n\n';
  latex += '\\end{document}';
  
  return latex;
}

/**
 * Format number for LaTeX (handle decimals nicely)
 */
function formatNumber(num: number): string {
  // If integer, show as integer
  if (Number.isInteger(num)) {
    return num.toString();
  }
  
  // If decimal, show up to 4 decimal places
  const rounded = Math.round(num * 10000) / 10000;
  return rounded.toString();
}

/**
 * Copy to clipboard helper
 */
export async function copyToClipboard(text: string): Promise<boolean> {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch (err) {
    console.error('Failed to copy to clipboard:', err);
    
    // Fallback for older browsers
    try {
      const textArea = document.createElement('textarea');
      textArea.value = text;
      textArea.style.position = 'fixed';
      textArea.style.left = '-999999px';
      document.body.appendChild(textArea);
      textArea.select();
      document.execCommand('copy');
      document.body.removeChild(textArea);
      return true;
    } catch (fallbackErr) {
      console.error('Fallback copy failed:', fallbackErr);
      return false;
    }
  }
}

/**
 * Download as .tex file
 */
export function downloadAsTexFile(latex: string, filename: string = 'matrix.tex'): void {
  const blob = new Blob([latex], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename.endsWith('.tex') ? filename : `${filename}.tex`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

/**
 * LaTeX templates for different matrix types
 */
export const latexTemplates = {
  pmatrix: (data: string) => `\\begin{pmatrix}\n${data}\n\\end{pmatrix}`,
  bmatrix: (data: string) => `\\begin{bmatrix}\n${data}\n\\end{bmatrix}`,
  vmatrix: (data: string) => `\\begin{vmatrix}\n${data}\n\\end{vmatrix}`, // Determinant
  Bmatrix: (data: string) => `\\begin{Bmatrix}\n${data}\n\\end{Bmatrix}`, // Curly braces
  array: (data: string) => `\\begin{array}{c}\n${data}\n\\end{array}`,
};
