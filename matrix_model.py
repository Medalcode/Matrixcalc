"""
matrix_model.py

Módulo de lógica pura para operaciones matriciales usando NumPy.
Contiene funciones para parsear cadenas a matrices, sumar matrices, calcular
inversa y determinante con validaciones y mensajes de error claros.

Este módulo no tiene dependencias de GUI y lanza ValueError con mensajes
legibles en caso de error — ideal para que la capa de vista los capture
y los muestre al usuario.
"""
from typing import Any
import numpy as np

__all__ = [
    "parse_matrix",
    "safe_add",
    "safe_dot",
    "safe_inv",
    "safe_det",
]


def parse_matrix(text: str, rows: int, cols: int, dtype=float) -> np.ndarray:
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
        raise ValueError("rows y cols deben ser enteros positivos.")

    if text is None:
        raise ValueError("Texto de entrada vacío.")

    # 1) Tokenizar y limpiar
    tokens = [tok.strip() for tok in text.split(',')]

    # Detectar valores vacíos explícitos (ej: ",," o ", ")
    if any(tok == "" for tok in tokens):
        raise ValueError("Se encontraron valores vacíos en la entrada. Asegúrese de separar valores con comas.")

    expected = rows * cols
    if len(tokens) != expected:
        raise ValueError(f"Se esperaban {expected} valores (rows*cols={expected}), pero se recibieron {len(tokens)}.")

    # 2) Conversión a números usando fromiter (rápido y seguro)
    try:
        # Usamos float() como conversor porque dtype puede ser un tipo Python o numpy dtype
        arr = np.fromiter((float(t) for t in tokens), dtype=dtype, count=len(tokens))
    except ValueError as exc:
        raise ValueError("Error al convertir los valores a número. Asegúrese de usar sólo valores numéricos.") from exc

    # 3) Reshape
    try:
        arr = arr.reshape((rows, cols))
    except Exception as exc:
        raise ValueError("Los valores no pueden redimensionarse a las dimensiones solicitadas.") from exc

    return arr


def safe_add(A: Any, B: Any) -> np.ndarray:
    """
    Suma dos matrices A y B utilizando np.add.
    Lanza ValueError si las formas (shapes) de las matrices son incompatibles.
    """
    A_np = np.asarray(A)
    B_np = np.asarray(B)

    if A_np.shape != B_np.shape:
        raise ValueError(f"Shapes incompatibles para suma: A{A_np.shape} vs B{B_np.shape}.")

    return np.add(A_np, B_np)


def safe_inv(A: Any) -> np.ndarray:
    """
    Calcula la inversa de A de forma segura.
    Lanza ValueError si la matriz no es cuadrada o si es singular/mal condicionada.
    """
    A_np = np.asarray(A, dtype=float)

    if A_np.ndim != 2 or A_np.shape[0] != A_np.shape[1]:
        raise ValueError(f"La matriz debe ser cuadrada para calcular la inversa (shape={A_np.shape}).")

    # Comprobar condicionamiento numérico
    try:
        cond = np.linalg.cond(A_np)
    except Exception:
        # Si no se puede calcular la condición, tratarlo como no invertible
        raise ValueError("No se pudo evaluar la condición de la matriz; es posible que sea singular o inválida.")

    # Umbral: si la condición es mayor que 1/eps es indicativo de mal condicionamiento
    eps = np.finfo(A_np.dtype).eps
    threshold = 1.0 / eps
    if not np.isfinite(cond) or cond > threshold:
        raise ValueError(f"La matriz está mal condicionada o es singular (condición={cond:.3e}). No es segura para invertir.")

    try:
        inv = np.linalg.inv(A_np)
        return inv
    except np.linalg.LinAlgError as exc:
        raise ValueError("La matriz es singular y no tiene inversa.") from exc


def safe_det(A: Any) -> float:
    """
    Calcula el determinante de A (np.linalg.det).
    Lanza ValueError si la matriz no es cuadrada.
    """
    A_np = np.asarray(A, dtype=float)

    if A_np.ndim != 2 or A_np.shape[0] != A_np.shape[1]:
        raise ValueError(f"La matriz debe ser cuadrada para calcular el determinante (shape={A_np.shape}).")

    return float(np.linalg.det(A_np))


def safe_dot(A: Any, B: Any) -> np.ndarray:
    """
    Realiza la multiplicación matricial A @ B (np.matmul) validando shapes.
    Lanza ValueError si las dimensiones no son compatibles para la multiplicación.
    """
    A_np = np.asarray(A)
    B_np = np.asarray(B)

    if A_np.ndim != 2 or B_np.ndim != 2:
        raise ValueError(f"Ambos operandos deben ser matrices 2D. Got shapes: A{A_np.shape}, B{B_np.shape}")

    if A_np.shape[1] != B_np.shape[0]:
        raise ValueError(f"Shapes incompatibles para multiplicación: A{A_np.shape} x B{B_np.shape}. Requiera A.columns == B.rows.")

    try:
        return np.matmul(A_np, B_np)
    except Exception as exc:
        raise ValueError("Error al multiplicar las matrices.") from exc
