"""Project-specific exceptions for matrix_model.

Define a small hierarchy so the UI can distinguish user/input errors
from internal failures.
"""


class MatrixModelError(ValueError):
    """Base class for errors raised by matrix_model."""


class InvalidMatrixError(MatrixModelError):
    """Raised when matrix input is invalid (parse errors, wrong counts, etc.)."""


class NumericError(MatrixModelError):
    """Raised when numeric operations fail (singular, ill-conditioned, etc.)."""
