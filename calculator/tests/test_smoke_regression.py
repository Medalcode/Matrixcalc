"""
Pruebas integrales de humo (Smoke Tests) y regresión para MatrixCalc API.

Cubre escenarios end-to-end completos, flujos negativos y casos borde.
"""

import pytest
from django.urls import reverse
from rest_framework import status
from calculator.models import Matrix, Operation


@pytest.mark.django_db
class TestSmokeAndRegression:
    """Suite de pruebas de humo y regresión para flujos críticos del sistema."""

    def test_e2e_matrix_lifecycle_and_operations(self, api_client):
        """
        Prueba de humo E2E:
        1. Crear Matriz A
        2. Crear Matriz B
        3. Realizar suma A + B
        4. Realizar transposición Aᵀ
        5. Exportar Matriz A a CSV y JSON
        6. Verificar la preservación del historial en Operation log
        """
        # 1. Crear Matriz A
        resp_a = api_client.post(
            reverse("matrix-list"),
            {"name": "Matrix Alpha", "rows": 2, "cols": 2, "data": [[1.0, 2.0], [3.0, 4.0]]},
            format="json",
        )
        assert resp_a.status_code == status.HTTP_201_CREATED
        id_a = resp_a.data["id"]

        # 2. Crear Matriz B
        resp_b = api_client.post(
            reverse("matrix-list"),
            {"name": "Matrix Beta", "rows": 2, "cols": 2, "data": [[5.0, 6.0], [7.0, 8.0]]},
            format="json",
        )
        assert resp_b.status_code == status.HTTP_201_CREATED
        id_b = resp_b.data["id"]

        # 3. Realizar Operación SUMA
        resp_sum = api_client.post(
            reverse("sum-matrices"),
            {"matrix_a_id": id_a, "matrix_b_id": id_b},
            format="json",
        )
        assert resp_sum.status_code == status.HTTP_201_CREATED
        assert resp_sum.data["operation_type"] == "SUM"
        assert resp_sum.data["result"]["data"] == [[6.0, 8.0], [10.0, 12.0]]

        # 4. Realizar Operación TRANSPUESTA (espera matrix_id)
        resp_trans = api_client.post(
            reverse("transpose-matrix"),
            {"matrix_id": id_a},
            format="json",
        )
        assert resp_trans.status_code == status.HTTP_201_CREATED
        assert resp_trans.data["result"]["data"] == [[1.0, 3.0], [2.0, 4.0]]

        # 5. Exportar Matriz A a CSV y JSON
        resp_csv = api_client.get(reverse("matrix-export-csv", kwargs={"pk": id_a}))
        assert resp_csv.status_code == status.HTTP_200_OK
        assert "text/csv" in resp_csv["Content-Type"]
        assert "1.0,2.0" in resp_csv.content.decode("utf-8")

        resp_json = api_client.get(reverse("matrix-export-json", kwargs={"pk": id_a}))
        assert resp_json.status_code == status.HTTP_200_OK
        assert resp_json.data["name"] == "Matrix Alpha"

        # 6. Verificar historial en Operation log
        assert Operation.objects.count() == 2

    def test_negative_incompatible_multiplication(self, api_client):
        """Caso borde negativo: Intentar multiplicar matrices con dimensiones incompatibles."""
        m1 = Matrix.objects.create(name="2x3", rows=2, cols=3, data=[[1, 2, 3], [4, 5, 6]])
        m2 = Matrix.objects.create(name="2x2", rows=2, cols=2, data=[[1, 2], [3, 4]])

        resp = api_client.post(
            reverse("multiply-matrices"),
            {"matrix_a_id": m1.id, "matrix_b_id": m2.id},
            format="json",
        )
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in resp.data

    def test_negative_singular_matrix_inversion(self, api_client):
        """Caso borde negativo: Invertir una matriz singular (determinante = 0)."""
        singular = Matrix.objects.create(name="Singular", rows=2, cols=2, data=[[1, 2], [2, 4]])

        resp = api_client.post(
            reverse("inverse-matrix"),
            {"matrix_id": singular.id},
            format="json",
        )
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "error" in resp.data

    def test_negative_nonexistent_matrix(self, api_client):
        """Caso negativo: Intentar operar sobre un ID inexistente."""
        resp = api_client.post(
            reverse("inverse-matrix"),
            {"matrix_id": 999999},
            format="json",
        )
        assert resp.status_code == status.HTTP_404_NOT_FOUND

    def test_matrix_validation_limits(self, api_client):
        """Validación de límites: Rechazar dimensiones superiores a MAX_DIMENSION (100)."""
        resp = api_client.post(
            reverse("matrix-list"),
            {"name": "Too Big", "rows": 105, "cols": 105, "data": [[0]]},
            format="json",
        )
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
