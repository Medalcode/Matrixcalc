import numpy as np
import pytest

import matrix_model as mm


def test_parse_matrix_missing_values():
    # 2x2 expected -> only 3 values provided
    text = "1, 2, 3"
    with pytest.raises(ValueError) as exc:
        mm.parse_matrix(text, 2, 2)
    assert "Se esperaban" in str(exc.value)


def test_parse_matrix_non_numeric():
    text = "1, 2, a, 4"
    with pytest.raises(ValueError) as exc:
        mm.parse_matrix(text, 2, 2)
    assert "convertir" in str(exc.value) or "numéricos" in str(exc.value)


def test_safe_add_incompatible_shapes():
    A = np.ones((2, 2))
    B = np.ones((3, 3))
    with pytest.raises(ValueError) as exc:
        mm.safe_add(A, B)
    assert "Shapes incompatibles" in str(exc.value)


def test_safe_inv_non_square():
    A = np.ones((2, 3))
    with pytest.raises(ValueError) as exc:
        mm.safe_inv(A)
    assert "cuadrada" in str(exc.value)


def test_safe_inv_singular_or_bad_condition():
    # Singular matrix (rows are linearly dependent)
    A = np.array([[1.0, 2.0], [2.0, 4.0]])
    with pytest.raises(ValueError) as exc:
        mm.safe_inv(A)
    msg = str(exc.value)
    # The implementation may raise for bad conditioning or singularity; accept either message
    assert ("mal condicionada" in msg) or ("singular" in msg) or ("No se pudo evaluar" in msg)
