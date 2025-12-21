"""
Utilidades para la aplicación calculator.

Este paquete contiene la lógica numérica para operaciones matriciales
y los exception handlers personalizados.
"""

from calculator.utils.matrix_model import (
    parse_matrix,
    safe_add,
    safe_subtract,
    safe_dot,
    safe_inv,
    safe_det,
    safe_transpose,
)
from calculator.utils.exceptions import (
    MatrixModelError,
    InvalidMatrixError,
    NumericError,
)

__all__ = [
    'parse_matrix',
    'safe_add',
    'safe_subtract',
    'safe_dot',
    'safe_inv',
    'safe_det',
    'safe_transpose',
    'MatrixModelError',
    'InvalidMatrixError',
    'NumericError',
]
