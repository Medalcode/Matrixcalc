
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


def safe_eigenvalues(A: Any) -> dict:
    """
    Calcula valores y vectores propios de una matriz cuadrada.
    
    Returns:
        dict: {
            'eigenvalues': [{'real': float, 'imag': float}, ...],
            'eigenvectors': [[...], ...]  # Columnas son los autovectores
        }
    """
    A_np = np.ascontiguousarray(A, dtype=np.float64)
    
    if A_np.ndim != 2 or A_np.shape[0] != A_np.shape[1]:
        raise InvalidMatrixError(f"La matriz debe ser cuadrada para calcular valores propios (shape={A_np.shape}).")

    try:
        vals, vecs = np.linalg.eig(A_np)
        
        # Formatear valores propios (manejo de complejos)
        vals_list = []
        for v in vals:
            if np.iscomplex(v):
                vals_list.append({'real': float(v.real), 'imag': float(v.imag), 'is_complex': True})
            else:
                vals_list.append({'real': float(v.real), 'imag': 0.0, 'is_complex': False})
                
        # Los vectores propios en numpy son las columnas de 'vecs'.
        # Para visualización fácil, convertimos a lista de listas standard (filas)
        # pero mantenemos la estructura numérica.
        # Nota: Los autovectores pueden ser complejos si los autovalores lo son.
        # Por simplicidad en JSON, tomamos la parte real si es complejo, o notificamos.
        # Para v3.0 MVP: Retornamos representación string si es complejo para evitar errores de JSON simples,
        # o estructuras separadas.
        
        # Enfoque robusto: Convertir a listas de componentes reales/imag para vectores también sería ideal,
        # pero muy verboso. Convertiremos a listas de floats tomando parte real si la imaginaria es despreciable,
        # o string complex representation si no.
        
        vecs_formatted = []
        for row in vecs:
            row_formatted = []
            for val in row:
                if np.iscomplex(val) and not np.isclose(val.imag, 0):
                    row_formatted.append(str(val)) # Fallback a string para complejos
                else:
                    row_formatted.append(float(val.real))
            vecs_formatted.append(row_formatted)

        return {
            'eigenvalues': vals_list,
            'eigenvectors': vecs_formatted
        }
    except np.linalg.LinAlgError as exc:
        raise NumericError("El cálculo de valores propios no convergió.") from exc


def safe_rank(A: Any) -> int:
    """Calcula el rango matricial usando SVD."""
    A_np = np.ascontiguousarray(A, dtype=np.float64)
    try:
        return int(np.linalg.matrix_rank(A_np))
    except Exception as exc:
         raise NumericError("Error al calcular el rango de la matriz.") from exc


def safe_svd(A: Any) -> dict:
    """
    Calcula la descomposición en valores singulares (SVD).
    A = U * S * Vh
    
    Returns:
        dict: {'U': list, 'S': list, 'Vh': list}
    """
    A_np = np.ascontiguousarray(A, dtype=np.float64)
    try:
        u, s, vh = np.linalg.svd(A_np, full_matrices=True)
        return {
            'U': u.tolist(),
            'S': s.tolist(), # Valores singulares (vector 1D)
            'Vh': vh.tolist()
        }
    except np.linalg.LinAlgError as exc:
        raise NumericError("El cálculo SVD no convergió.") from exc


def safe_qr(A: Any) -> dict:
    """
    Calcula la descomposición QR.
    A = Q * R
    
    Returns:
        dict: {'Q': list, 'R': list}
    """
    A_np = np.ascontiguousarray(A, dtype=np.float64)
    try:
        q, r = np.linalg.qr(A_np)
        return {
            'Q': q.tolist(),
            'R': r.tolist()
        }
    except np.linalg.LinAlgError as exc:
        raise NumericError("Error en la descomposición QR.") from exc


def safe_cholesky(A: Any) -> list:
    """
    Calcula la descomposición de Cholesky.
    A = L * L.H
    
    Requiere que la matriz sea Hermítica (simétrica si real) y definida positiva.
    """
    A_np = np.ascontiguousarray(A, dtype=np.float64)
    
    if A_np.ndim != 2 or A_np.shape[0] != A_np.shape[1]:
        raise InvalidMatrixError(f"La matriz debe ser cuadrada (shape={A_np.shape}).")
        
    try:
        L = np.linalg.cholesky(A_np)
        return L.tolist()
    except np.linalg.LinAlgError:
        raise NumericError(
            "La matriz no es definida positiva. La descomposición de Cholesky require "
            "una matriz simétrica y definida positiva."
        )
