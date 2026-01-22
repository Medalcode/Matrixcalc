/**
 * Interfaces TypeScript para la aplicación MatrixCalc
 */

export interface Matrix {
  id: number
  name: string
  rows: number
  cols: number
  data: number[][]
  created_at: string
  updated_at: string
}

export interface MatrixCreateDTO {
  name: string
  rows: number
  cols: number
  data: number[][]
}

export interface Operation {
  id: number
  operation_type: OperationType
  matrix_a: Matrix
  matrix_b?: Matrix | null
  result: Matrix
  extra_data?: any
  execution_time_ms: number
  created_at: string
}

export type OperationType = 
  | 'SUM' 
  | 'SUBTRACT' 
  | 'MULTIPLY' 
  | 'INVERSE' 
  | 'DETERMINANT' 
  | 'TRANSPOSE'
  | 'RANK'
  | 'EIGEN'
  | 'SVD'
  | 'QR'
  | 'CHOLESKY'

export interface OperationRequest {
  matrix_a_id?: number
  matrix_b_id?: number
  matrix_id?: number
}

export interface Stats {
  total_matrices: number
  total_operations: number
  operations_by_type: OperationTypeCount[]
  operations_timeline: TimelineData[]
  storage_mb: number
  average_execution_time_ms: number
  recent_operations_count: number
}

export interface OperationTypeCount {
  operation_type: OperationType
  count: number
  avg_time: number
}

export interface TimelineData {
  date: string
  count: number
}

export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

export interface BackupData {
  version: string
  timestamp: string
  database: string
  total_matrices: number
  total_operations: number
  matrices: Matrix[]
  operations: Operation[]
}

export interface APIError {
  error: string
  detail?: string
}
