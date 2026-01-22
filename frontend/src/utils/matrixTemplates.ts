export interface MatrixTemplate {
  name: string
  description: string
  category: 'basic' | 'special' | 'transformation' | 'example'
  generateData: (rows: number, cols: number) => number[][]
}

export const matrixTemplates: MatrixTemplate[] = [
  {
    name: 'Zeros',
    description: 'Matrix filled with zeros',
    category: 'basic',
    generateData: (rows, cols) => Array(rows).fill(0).map(() => Array(cols).fill(0))
  },
  {
    name: 'Ones',
    description: 'Matrix filled with ones',
    category: 'basic',
    generateData: (rows, cols) => Array(rows).fill(0).map(() => Array(cols).fill(1))
  },
  {
    name: 'Identity',
    description: 'Identity matrix (diagonal ones)',
    category: 'special',
    generateData: (rows, cols) => {
      const size = Math.min(rows, cols)
      return Array(rows).fill(0).map((_, i) =>
        Array(cols).fill(0).map((_, j) => (i === j && i < size) ? 1 : 0)
      )
    }
  },
  {
    name: 'Diagonal',
    description: 'Diagonal matrix with sequential values',
    category: 'special',
    generateData: (rows, cols) => {
      const size = Math.min(rows, cols)
      return Array(rows).fill(0).map((_, i) =>
        Array(cols).fill(0).map((_, j) => (i === j && i < size) ? i + 1 : 0)
      )
    }
  },
  {
    name: 'Random (0-1)',
    description: 'Random values between 0 and 1',
    category: 'basic',
    generateData: (rows, cols) =>
      Array(rows).fill(0).map(() =>
        Array(cols).fill(0).map(() => Math.random())
      )
  },
  {
    name: 'Random (-10 to 10)',
    description: 'Random integer values between -10 and 10',
    category: 'basic',
    generateData: (rows, cols) =>
      Array(rows).fill(0).map(() =>
        Array(cols).fill(0).map(() => Math.floor(Math.random() * 21) - 10)
      )
  },
  {
    name: 'Upper Triangular',
    description: 'Upper triangular matrix with ones',
    category: 'special',
    generateData: (rows, cols) =>
      Array(rows).fill(0).map((_, i) =>
        Array(cols).fill(0).map((_, j) => (j >= i) ? 1 : 0)
      )
  },
  {
    name: 'Lower Triangular',
    description: 'Lower triangular matrix with ones',
    category: 'special',
    generateData: (rows, cols) =>
      Array(rows).fill(0).map((_, i) =>
        Array(cols).fill(0).map((_, j) => (j <= i) ? 1 : 0)
      )
  },
  {
    name: 'Checkerboard',
    description: 'Alternating 0s and 1s in checkerboard pattern',
    category: 'example',
    generateData: (rows, cols) =>
      Array(rows).fill(0).map((_, i) =>
        Array(cols).fill(0).map((_, j) => (i + j) % 2)
      )
  },
  {
    name: 'Rotation 2D (90°)',
    description: '2x2 rotation matrix for 90 degrees',
    category: 'transformation',
    generateData: (rows, cols) => {
      // Create empty matrix first
      const matrix = Array(rows).fill(0).map(() => Array(cols).fill(0))
      
      if (rows >= 2 && cols >= 2) {
        if (matrix[0]) {
          matrix[0][0] = 0
          matrix[0][1] = -1
        }
        if (matrix[1]) {
          matrix[1][0] = 1
          matrix[1][1] = 0
        }
      }
      return matrix
    }
  },
  {
    name: 'Scaling 2D',
    description: '2x2 scaling matrix (2x in x, 3x in y)',
    category: 'transformation',
    generateData: (rows, cols) => {
      // Create empty matrix first
      const matrix = Array(rows).fill(0).map(() => Array(cols).fill(0))

      if (rows >= 2 && cols >= 2) {
        if (matrix[0]) matrix[0][0] = 2
        if (matrix[1]) matrix[1][1] = 3
      }
      return matrix
    }
  },
  {
    name: 'Hilbert Matrix',
    description: 'Hilbert matrix (H[i,j] = 1/(i+j-1))',
    category: 'example',
    generateData: (rows, cols) =>
      Array(rows).fill(0).map((_, i) =>
        Array(cols).fill(0).map((_, j) => 1 / (i + j + 1))
      )
  },
  {
    name: 'Vandermonde',
    description: 'Vandermonde matrix with base [1,2,3,...]',
    category: 'example',
    generateData: (rows, cols) =>
      Array(rows).fill(0).map((_, i) =>
        Array(cols).fill(0).map((_, j) => Math.pow(i + 1, j))
      )
  },
  {
    name: 'Pascal Triangle',
    description: 'Pascal\'s triangle as matrix (binomial coefficients)',
    category: 'example',
    generateData: (rows, cols) => {
      const binomial = (n: number, k: number): number => {
        if (k < 0 || k > n) return 0
        if (k === 0 || k === n) return 1
        let result = 1
        for (let i = 1; i <= k; i++) {
          result = result * (n - k + i) / i
        }
        return Math.round(result)
      }
      return Array(rows).fill(0).map((_, i) =>
        Array(cols).fill(0).map((_, j) => binomial(i, j))
      )
    }
  }
]

export function getTemplatesByCategory(category: string): MatrixTemplate[] {
  return matrixTemplates.filter(t => t.category === category)
}

export function getTemplateByName(name: string): MatrixTemplate | undefined {
  return matrixTemplates.find(t => t.name === name)
}

export const templateCategories = [
  { value: 'basic', label: 'Basic Matrices' },
  { value: 'special', label: 'Special Matrices' },
  { value: 'transformation', label: 'Transformation Matrices' },
  { value: 'example', label: 'Example Matrices' }
] as const
