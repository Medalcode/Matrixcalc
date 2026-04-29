"""
Tests unitarios para calculator.utils.matrix_model.

Cubre todas las funciones expuestas en __all__.
"""

from unittest.mock import patch

import numpy as np
import pytest

from calculator.utils.exceptions import InvalidMatrixError, NumericError
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
    safe_rank,
    safe_subtract,
    safe_svd,
    safe_transpose,
)

# =============================================================================
# parse_matrix
# =============================================================================


class TestParseMatrix:
    def test_parses_csv_correctly(self):
        result = parse_matrix("1, 2, 3, 4", 2, 2)
        assert isinstance(result, np.ndarray)
        assert result.shape == (2, 2)
        assert np.allclose(result, [[1, 2], [3, 4]])

    def test_parses_single_row(self):
        result = parse_matrix("5, 6, 7", 1, 3)
        assert result.shape == (1, 3)
        assert np.allclose(result, [[5, 6, 7]])

    def test_parses_single_column(self):
        result = parse_matrix("8, 9", 2, 1)
        assert result.shape == (2, 1)
        assert np.allclose(result, [[8], [9]])

    def test_rejects_non_string_text(self):
        with pytest.raises(InvalidMatrixError, match="cadena"):
            parse_matrix(None, 1, 1)
        with pytest.raises(InvalidMatrixError, match="cadena"):
            parse_matrix(123, 1, 1)

    def test_rejects_empty_values(self):
        with pytest.raises(InvalidMatrixError, match="vac"):
            parse_matrix("1,,3", 1, 3)

    def test_rejects_wrong_token_count(self):
        with pytest.raises(InvalidMatrixError, match="Se esperaban"):
            parse_matrix("1,2,3", 2, 2)

    def test_rejects_non_numeric_tokens(self):
        with pytest.raises(InvalidMatrixError, match="num"):
            parse_matrix("a,b,c", 1, 3)

    def test_rejects_non_positive_dimensions(self):
        with pytest.raises(InvalidMatrixError, match="positivos"):
            parse_matrix("1", 0, 1)
        with pytest.raises(InvalidMatrixError, match="positivos"):
            parse_matrix("1", 1, -1)
        with pytest.raises(InvalidMatrixError, match="positivos"):
            parse_matrix("1", 1.5, 2)


# =============================================================================
# safe_add
# =============================================================================


class TestSafeAdd:
    def test_adds_two_matrices(self):
        A = [[1, 2], [3, 4]]
        B = [[5, 6], [7, 8]]
        result = safe_add(A, B)
        assert np.allclose(result, [[6, 8], [10, 12]])

    def test_adds_float64_by_default(self):
        result = safe_add([[1]], [[2]])
        assert result.dtype == np.float64

    def test_rejects_shape_mismatch(self):
        with pytest.raises(InvalidMatrixError, match="Shapes incompatibles"):
            safe_add([[1, 2]], [[1]])


# =============================================================================
# safe_subtract
# =============================================================================


class TestSafeSubtract:
    def test_subtracts_matrices(self):
        result = safe_subtract([[5, 6], [7, 8]], [[1, 2], [3, 4]])
        assert np.allclose(result, [[4, 4], [4, 4]])

    def test_rejects_shape_mismatch(self):
        with pytest.raises(InvalidMatrixError, match="Shapes incompatibles"):
            safe_subtract([[1]], [[1, 2]])


# =============================================================================
# safe_dot
# =============================================================================


class TestSafeDot:
    def test_multiplies_compatible_matrices(self):
        A = [[1, 2], [3, 4]]
        B = [[5, 6], [7, 8]]
        result = safe_dot(A, B)
        assert np.allclose(result, [[19, 22], [43, 50]])

    def test_multiplies_non_square(self):
        A = [[1, 2, 3], [4, 5, 6]]
        B = [[7, 8], [9, 10], [11, 12]]
        result = safe_dot(A, B)
        assert result.shape == (2, 2)

    def test_rejects_inner_dim_mismatch(self):
        with pytest.raises(InvalidMatrixError, match="incompatibles"):
            safe_dot([[1, 2]], [[1], [2], [3]])

    def test_rejects_1d_inputs(self):
        with pytest.raises(InvalidMatrixError, match="2D"):
            safe_dot([1, 2], [3, 4])


# =============================================================================
# safe_inv
# =============================================================================


class TestSafeInv:
    def test_inverts_identity(self):
        result = safe_inv([[1, 0], [0, 1]])
        assert np.allclose(result, [[1, 0], [0, 1]])

    def test_inverts_invertible_matrix(self):
        A = [[4, 7], [2, 6]]
        inv = safe_inv(A)
        assert np.allclose(np.dot(A, inv), np.eye(2), atol=1e-10)

    def test_rejects_non_square(self):
        with pytest.raises(InvalidMatrixError, match="cuadrada"):
            safe_inv([[1, 2, 3]])

    def test_rejects_singular_matrix(self):
        with pytest.raises(NumericError, match="mal condicionada|singular"):
            safe_inv([[1, 2], [2, 4]])


# =============================================================================
# safe_det
# =============================================================================


class TestSafeDet:
    def test_det_of_identity(self):
        assert safe_det(np.eye(3)) == pytest.approx(1.0)

    def test_det_of_2x2(self):
        assert safe_det([[1, 2], [3, 4]]) == pytest.approx(-2.0)

    def test_det_of_singular(self):
        assert safe_det([[1, 2], [2, 4]]) == pytest.approx(0.0, abs=1e-10)

    def test_rejects_non_square(self):
        with pytest.raises(InvalidMatrixError, match="cuadrada"):
            safe_det([[1, 2]])


# =============================================================================
# safe_transpose
# =============================================================================


class TestSafeTranspose:
    def test_transposes_2x3(self):
        result = safe_transpose([[1, 2, 3], [4, 5, 6]])
        assert result.shape == (3, 2)
        assert np.allclose(result, [[1, 4], [2, 5], [3, 6]])

    def test_transposes_square(self):
        result = safe_transpose([[1, 2], [3, 4]])
        assert np.allclose(result, [[1, 3], [2, 4]])

    def test_rejects_1d(self):
        with pytest.raises(InvalidMatrixError, match="2D"):
            safe_transpose([1, 2, 3])


# =============================================================================
# safe_rank
# =============================================================================


class TestSafeRank:
    def test_full_rank(self):
        assert safe_rank(np.eye(5)) == 5

    def test_rank_deficient(self):
        A = [[1, 2], [2, 4]]
        assert safe_rank(A) == 1

    def test_zero_matrix(self):
        assert safe_rank([[0, 0], [0, 0]]) == 0


# =============================================================================
# safe_eigenvalues
# =============================================================================


class TestSafeEigenvalues:
    def test_real_eigenvalues(self):
        A = [[2, 0], [0, 3]]
        result = safe_eigenvalues(A)
        vals = sorted(v["real"] for v in result["eigenvalues"])
        assert vals == pytest.approx([2.0, 3.0])
        for v in result["eigenvalues"]:
            assert v["imag"] == 0.0

    def test_complex_eigenvalues(self):
        A = [[0, -1], [1, 0]]
        result = safe_eigenvalues(A)
        complex_vals = [v for v in result["eigenvalues"] if v["is_complex"]]
        assert len(complex_vals) == 2

    def test_eigenvectors_dict_format(self):
        A = [[1, 0], [0, 2]]
        result = safe_eigenvalues(A)
        for row in result["eigenvectors"]:
            for val in row:
                assert "real" in val
                assert "imag" in val

    def test_rejects_non_square(self):
        with pytest.raises(InvalidMatrixError, match="cuadrada"):
            safe_eigenvalues([[1, 2, 3]])


# =============================================================================
# safe_svd
# =============================================================================


class TestSafeSvd:
    def test_svd_reconstruction(self):
        A = [[1, 2], [3, 4], [5, 6]]
        result = safe_svd(A)
        U = np.array(result["U"])
        S = np.zeros((U.shape[0], len(result["S"])))
        np.fill_diagonal(S, result["S"])
        Vh = np.array(result["Vh"])
        reconstructed = U @ S @ Vh
        assert np.allclose(reconstructed, A, atol=1e-10)

    def test_svd_keys_present(self):
        result = safe_svd([[1, 0], [0, 1]])
        assert set(result.keys()) == {"U", "S", "Vh"}


# =============================================================================
# safe_qr
# =============================================================================


class TestSafeQr:
    def test_qr_reconstruction(self):
        A = [[12, -51, 4], [6, 167, -68], [-4, 24, -41]]
        result = safe_qr(A)
        Q = np.array(result["Q"])
        R = np.array(result["R"])
        assert np.allclose(Q @ R, A, atol=1e-10)

    def test_q_orthogonal(self):
        A = [[1, 2], [3, 4]]
        result = safe_qr(A)
        Q = np.array(result["Q"])
        assert np.allclose(Q.T @ Q, np.eye(Q.shape[1]), atol=1e-10)


# =============================================================================
# safe_lu
# =============================================================================


class TestSafeLu:
    def test_lu_reconstruction(self):
        A = [[4, 3], [6, 3]]
        result = safe_lu(A)
        P = np.array(result["P"])
        L = np.array(result["L"])
        U = np.array(result["U"])
        assert np.allclose(P @ L @ U, A)

    def test_l_upper_unit_diag(self):
        result = safe_lu(np.eye(3))
        L = np.array(result["L"])
        assert np.allclose(np.diag(L), np.ones(3))

    def test_lu_3x3(self):
        A = [[2, -1, 0], [-1, 2, -1], [0, -1, 2]]
        result = safe_lu(A)
        P = np.array(result["P"])
        L = np.array(result["L"])
        U = np.array(result["U"])
        assert np.allclose(P @ L @ U, A)

    def test_rejects_non_square(self):
        with pytest.raises(InvalidMatrixError, match="cuadrada"):
            safe_lu([[1, 2, 3]])

    def test_rejects_singular(self):
        with pytest.raises(NumericError, match="singular"):
            safe_lu([[1, 2], [2, 4]])


# =============================================================================
# safe_cholesky
# =============================================================================


class TestSafeCholesky:
    def test_cholesky_reconstruction(self):
        A = [[4, 2], [2, 3]]
        result = safe_cholesky(A)
        L = np.array(result)
        assert np.allclose(L @ L.T, A)

    def test_cholesky_3x3(self):
        A = [[25, 15, -5], [15, 18, 0], [-5, 0, 11]]
        result = safe_cholesky(A)
        L = np.array(result)
        assert np.allclose(L @ L.T, A)

    def test_rejects_non_square(self):
        with pytest.raises(InvalidMatrixError, match="cuadrada"):
            safe_cholesky([[1, 2, 3]])

    def test_rejects_non_positive_definite(self):
        with pytest.raises(NumericError, match="definida positiva"):
            safe_cholesky([[-1, 0], [0, -1]])


# =============================================================================
# Exception handler edge cases (hard to trigger naturally)
# =============================================================================


class TestExceptionHandlers:
    """Cover exception handlers in matrix_model.py"""

    def test_parse_matrix_reshape_error(self):
        """parse_matrix: except Exception from reshape (lines 83-84)"""
        with patch(
            "calculator.utils.matrix_model.np.fromiter", return_value=np.array([1.0, 2.0, 3.0])
        ):
            with pytest.raises(InvalidMatrixError, match="redimensionarse"):
                parse_matrix("1, 2, 3, 4", 2, 2)

    def test_safe_inv_cond_failure(self):
        """safe_inv: except Exception from np.linalg.cond (lines 132-134)"""
        with patch(
            "calculator.utils.matrix_model.np.linalg.cond", side_effect=Exception("cond failed")
        ):
            with pytest.raises(NumericError, match="condici"):
                safe_inv([[1, 2], [3, 4]])

    def test_safe_inv_linalg_error(self):
        """safe_inv: except LinAlgError from np.linalg.inv (lines 149-150)"""
        with patch(
            "calculator.utils.matrix_model.np.linalg.inv",
            side_effect=np.linalg.LinAlgError("singular"),
        ):
            with pytest.raises(NumericError, match="singular"):
                safe_inv([[1, 2], [3, 4]])

    def test_safe_det_linalg_error(self):
        """safe_det: except LinAlgError from np.linalg.det (lines 165-166)"""
        with patch(
            "calculator.utils.matrix_model.np.linalg.det",
            side_effect=np.linalg.LinAlgError("det failed"),
        ):
            with pytest.raises(NumericError, match="determinante"):
                safe_det([[1, 2], [3, 4]])

    def test_safe_dot_exception(self):
        """safe_dot: except Exception from np.matmul (lines 185-186)"""
        with patch(
            "calculator.utils.matrix_model.np.matmul", side_effect=Exception("matmul failed")
        ):
            with pytest.raises(NumericError, match="multiplicar"):
                safe_dot([[1, 2], [3, 4]], [[5, 6], [7, 8]])

    def test_safe_eigenvalues_linalg_error(self):
        """safe_eigenvalues: except LinAlgError (lines 242-243)"""
        with patch(
            "calculator.utils.matrix_model.np.linalg.eig",
            side_effect=np.linalg.LinAlgError("eig failed"),
        ):
            with pytest.raises(NumericError, match="valores propios"):
                safe_eigenvalues([[1, 2], [3, 4]])

    def test_safe_rank_exception(self):
        """safe_rank: except Exception from matrix_rank (lines 251-252)"""
        with patch(
            "calculator.utils.matrix_model.np.linalg.matrix_rank",
            side_effect=Exception("rank failed"),
        ):
            with pytest.raises(NumericError, match="rango"):
                safe_rank([[1, 2], [3, 4]])

    def test_safe_svd_linalg_error(self):
        """safe_svd: except LinAlgError from np.linalg.svd (lines 271-272)"""
        with patch(
            "calculator.utils.matrix_model.np.linalg.svd",
            side_effect=np.linalg.LinAlgError("svd failed"),
        ):
            with pytest.raises(NumericError, match="SVD"):
                safe_svd([[1, 2], [3, 4]])

    def test_safe_qr_linalg_error(self):
        """safe_qr: except LinAlgError from np.linalg.qr (lines 290-291)"""
        with patch(
            "calculator.utils.matrix_model.np.linalg.qr",
            side_effect=np.linalg.LinAlgError("qr failed"),
        ):
            with pytest.raises(NumericError, match="QR"):
                safe_qr([[1, 2], [3, 4]])
