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


def test_parse_matrix_spaces_and_non_numeric():
    # spaces and a non-numeric token
    text = " 1 , 2 , 3 , x "
    with pytest.raises(ValueError, match="convertir|numéricos"):
        mm.parse_matrix(text, 2, 2)


def test_parse_matrix_wrong_count():
    text = "1,2,3,4,5"
    with pytest.raises(ValueError, match="Se esperaban"):
        mm.parse_matrix(text, 2, 2)


def test_safe_dot_incompatible_shapes():
    A = np.ones((2, 3))
    B = np.ones((2, 3))
    with pytest.raises(ValueError, match="incompatibles"):
        mm.safe_dot(A, B)


def test_safe_subtract_success_and_incompatible():
    A = np.array([[1.0, 2.0], [3.0, 4.0]])
    B = np.array([[0.5, 1.0], [1.5, 2.0]])
    R = mm.safe_subtract(A, B)
    assert np.allclose(R, np.array([[0.5, 1.0], [1.5, 2.0]]))

    C = np.ones((3, 3))
    with pytest.raises(ValueError, match="incompatibles"):
        mm.safe_subtract(A, C)


def test_safe_det_non_square():
    A = np.ones((2, 3))
    with pytest.raises(ValueError, match="cuadrada"):
        mm.safe_det(A)


def test_safe_inv_ill_conditioned_and_non_square():
    # Non-square
    A = np.ones((3, 2))
    with pytest.raises(ValueError, match="cuadrada"):
        mm.safe_inv(A)

    # Singular (duplicate rows)
    S = np.array([[1.0, 2.0], [2.0, 4.0]])
    with pytest.raises(ValueError):
        mm.safe_inv(S)

    # Ill-conditioned matrix: Hilbert matrix of size 12 has a very large condition number
    n = 12
    H = np.fromfunction(lambda i, j: 1.0 / (i + j + 1.0), (n, n))
    # Sanity: ensure it's ill-conditioned above our threshold
    cond = np.linalg.cond(H)
    assert cond > 1e10
    with pytest.raises(ValueError, match="mal condicionada"):
        mm.safe_inv(H)
