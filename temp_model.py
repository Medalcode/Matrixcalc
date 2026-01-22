
"""matrix_model.py

Lógica pura para operaciones matriciales usando NumPy.

Este módulo levanta excepciones de dominio definidas en `exceptions.py`.
Todas las salidas numéricas usan np.float64 y las entradas son validadas.
"""

from typing import Any
import numpy as np

from calculator.utils.exceptions import InvalidMatrixError, NumericError, MatrixModelError

__all__ = [
    "parse_matrix",
    "safe_add",
    "safe_subtract",
    "safe_dot",
    "safe_inv",
    "safe_det",
    "safe_transpose",
    # Nuevas funciones v3.0
    "safe_eigenvalues",
    "safe_rank",
    "safe_svd",
    "safe_qr",
    "safe_lu",
    "safe_cholesky",
]


def parse_matrix(text: str, rows: int, cols: int, dtype=np.float64) -> np.ndarray:
    """
    Parsea una cadena CSV de valores y la convierte a un np.ndarray de dimensiones
    (rows, cols). Lanza ValueError si el formato es incorrecto o si el número
    de valores no coincide con rows * cols.

    Parameters
    ----------
    text : str
        Cadena con valores separados por comas, por ejemplo: "1, 2, 3, 4".
    rows : int
        Número de filas esperado.
    cols : int
        Número de columnas esperado.
    dtype : type, optional
        Tipo numérico de salida (por defecto float).

    Returns
    -------
    np.ndarray
        Array de forma (rows, cols) con los valores convertidos.
    """
    if not isinstance(rows, int) or not isinstance(cols, int) or rows <= 0 or cols <= 0:
        raise InvalidMatrixError("rows y cols deben ser enteros positivos.")

    if text is None:
        raise InvalidMatrixError("Texto de entrada vacío.")

    # 1) Tokenizar y limpiar
    tokens = [tok.strip() for tok in text.split(',')]

    # Detectar valores vacíos explícitos (ej: ",," o ", ")
    if any(tok == "" for tok in tokens):
        raise InvalidMatrixError("Se encontraron valores vacíos en la entrada. Asegúrese de separar valores con comas.")

    expected = rows * cols
    if len(tokens) != expected:
        raise InvalidMatrixError(f"Se esperaban {expected} valores (rows*cols={expected}), pero se recibieron {len(tokens)}.")

    # 2) Conversión a números usando fromiter (rápido y seguro)
    try:
        # Usamos float() como conversor y dtype por defecto es np.float64 para
        # asegurar consistencia numérica entre operaciones.
        arr = np.fromiter((float(t) for t in tokens), dtype=dtype, count=len(tokens))
    except ValueError as exc:
        raise InvalidMatrixError("Error al convertir los valores a número. Asegúrese de usar sólo valores numéricos.") from exc

    # 3) Reshape
    try:
        arr = arr.reshape((rows, cols))
    except Exception as exc:
        raise InvalidMatrixError("Los valores no pueden redimensionarse a las dimensiones solicitadas.") from exc

    return arr


def safe_add(A: Any, B: Any) -> np.ndarray:
    """
    Suma dos matrices A y B utilizando np.add.
    Lanza ValueError si las formas (shapes) de las matrices son incompatibles.
    """
    # Normalizamos a float64 para consistencia numérica
    A_np = np.ascontiguousarray(A, dtype=np.float64)
    B_np = np.ascontiguousarray(B, dtype=np.float64)

    if A_np.shape != B_np.shape:
        raise InvalidMatrixError(f"Shapes incompatibles para suma: A{A_np.shape} vs B{B_np.shape}.")

    return np.add(A_np, B_np)


def safe_subtract(A: Any, B: Any) -> np.ndarray:
    """
    Resta la matriz B de la matriz A (A - B) utilizando NumPy.
    Verifica shapes para compatibilidad y lanza ValueError si son incompatibles.
    """
    A_np = np.ascontiguousarray(A, dtype=np.float64)
    B_np = np.ascontiguousarray(B, dtype=np.float64)

    if A_np.shape != B_np.shape:
        raise InvalidMatrixError(f"Shapes incompatibles para resta: A{A_np.shape} vs B{B_np.shape}.")

    return np.subtract(A_np, B_np)


def safe_inv(A: Any) -> np.ndarray:
    """
    Calcula la inversa de A de forma segura.
    Lanza ValueError si la matriz no es cuadrada o si es singular/mal condicionada.
    """
    # Convertimos a float64 para mayor robustez numérica
    A_np = np.ascontiguousarray(A, dtype=np.float64)

    if A_np.ndim != 2 or A_np.shape[0] != A_np.shape[1]:
        raise ValueError(f"La matriz debe ser cuadrada para calcular la inversa (shape={A_np.shape}).")

    # Comprobar condicionamiento numérico
    try:
        cond = np.linalg.cond(A_np)
    except Exception:
        # Si no se puede calcular la condición, tratarlo como no invertible
        raise NumericError("No se pudo evaluar la condición de la matriz; es posible que sea singular o inválida.")

    # Umbral práctico para detectar matrices mal condicionadas.
    # La heurística anterior (1/eps) produce valores extremadamente grandes
    # (orden 1e16 para float64). Para la mayoría de aplicaciones numéricas
    # consideramos una matriz mal condicionada si su número de condición supera
    # 1e12 — este umbral es una elección pragmática que detecta problemas
    # numéricos reales sin ser excesivamente restrictivo.
    threshold = 1e12
    if not np.isfinite(cond) or cond > threshold:
        raise NumericError(f"La matriz está mal condicionada o es singular (condición={cond:.3e}). No es segura para invertir.")

    try:
        inv = np.linalg.inv(A_np)
        return inv
    except np.linalg.LinAlgError as exc:
        raise NumericError("La matriz es singular y no tiene inversa.") from exc


def safe_det(A: Any) -> float:
    """
    Calcula el determinante de A (np.linalg.det).
    Lanza ValueError si la matriz no es cuadrada.
    """
    A_np = np.ascontiguousarray(A, dtype=np.float64)

    if A_np.ndim != 2 or A_np.shape[0] != A_np.shape[1]:
        raise InvalidMatrixError(f"La matriz debe ser cuadrada para calcular el determinante (shape={A_np.shape}).")

    try:
        return float(np.linalg.det(A_np))
    except Exception as exc:
        raise NumericError("Error al calcular el determinante.") from exc


def safe_dot(A: Any, B: Any) -> np.ndarray:
    """
    Realiza la multiplicación matricial A @ B (np.matmul) validando shapes.
    Lanza ValueError si las dimensiones no son compatibles para la multiplicación.
    """
    A_np = np.ascontiguousarray(A, dtype=np.float64)
    B_np = np.ascontiguousarray(B, dtype=np.float64)

    if A_np.ndim != 2 or B_np.ndim != 2:
        raise InvalidMatrixError(f"Ambos operandos deben ser matrices 2D. Got shapes: A{A_np.shape}, B{B_np.shape}")

    if A_np.shape[1] != B_np.shape[0]:
        raise InvalidMatrixError(f"Shapes incompatibles para multiplicación: A{A_np.shape} x B{B_np.shape}. Requiera A.columns == B.rows.")

    try:
        return np.matmul(A_np, B_np)
    except Exception as exc:
        raise NumericError("Error al multiplicar las matrices.") from exc


def safe_transpose(A: Any) -> np.ndarray:
    """Return the transpose of A as a contiguous np.float64 2D array.

    Raises InvalidMatrixError if input is not 2D.
    """
    A_np = np.ascontiguousarray(A, dtype=np.float64)
    if A_np.ndim != 2:
        raise InvalidMatrixError(f"El operando debe ser una matriz 2D (shape={A_np.shape}).")
    return A_np.T
