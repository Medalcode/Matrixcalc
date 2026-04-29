"""
Utilidades para la aplicación calculator.

Este paquete contiene la lógica numérica para operaciones matriciales
y los exception handlers personalizados.
"""

from calculator.utils.exceptions import (
    InvalidMatrixError,
    MatrixModelError,
    NumericError,
)
from calculator.utils.matrix_model import (
    parse_matrix,
    safe_add,
    safe_cholesky,
    safe_det,
    safe_dot,
    safe_eigenvalues,
    safe_inv,
    safe_lu,
    safe_qr,
    # Nuevas operaciones v3.0
    safe_rank,
    safe_subtract,
    safe_svd,
    safe_transpose,
)

__all__ = [
    "parse_matrix",
    "safe_add",
    "safe_subtract",
    "safe_dot",
    "safe_inv",
    "safe_det",
    "safe_transpose",
    "safe_rank",
    "safe_eigenvalues",
    "safe_svd",
    "safe_qr",
    "safe_lu",
    "safe_cholesky",
    "MatrixModelError",
    "InvalidMatrixError",
    "NumericError",
]
