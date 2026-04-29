"""
Tests for API views/endpoints
"""

from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from calculator.models import Matrix, Operation


@pytest.mark.django_db
class TestMatrixViewSet:
    """Test suite for Matrix API endpoints"""

    def test_list_matrices(self, api_client, matrix):
        """Test GET /api/matrices/"""
        url = reverse("matrix-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert response.data["results"][0]["name"] == "Test Matrix"

    def test_list_empty_matrices(self, api_client):
        """Test listing when no matrices exist"""
        url = reverse("matrix-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 0

    def test_retrieve_matrix(self, api_client, matrix):
        """Test GET /api/matrices/{id}/"""
        url = reverse("matrix-detail", kwargs={"pk": matrix.id})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Test Matrix"
        assert response.data["rows"] == 3
        assert response.data["cols"] == 3

    def test_retrieve_nonexistent_matrix(self, api_client):
        """Test retrieving matrix that doesn't exist"""
        url = reverse("matrix-detail", kwargs={"pk": 99999})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_matrix(self, api_client, sample_matrix_data):
        """Test POST /api/matrices/"""
        url = reverse("matrix-list")
        response = api_client.post(url, sample_matrix_data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "Test Matrix"
        assert Matrix.objects.count() == 1

    def test_create_invalid_matrix(self, api_client):
        """Test creating matrix with invalid data"""
        url = reverse("matrix-list")
        invalid_data = {"name": "Invalid", "rows": 0, "cols": 3, "data": [[1, 2, 3]]}
        response = api_client.post(url, invalid_data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert Matrix.objects.count() == 0

    def test_update_matrix(self, api_client, matrix):
        """Test PUT /api/matrices/{id}/"""
        url = reverse("matrix-detail", kwargs={"pk": matrix.id})
        updated_data = {
            "name": "Updated Matrix",
            "rows": 3,
            "cols": 3,
            "data": [[9, 8, 7], [6, 5, 4], [3, 2, 1]],
        }
        response = api_client.put(url, updated_data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Updated Matrix"

        matrix.refresh_from_db()
        assert matrix.name == "Updated Matrix"

    def test_partial_update_matrix(self, api_client, matrix):
        """Test PATCH /api/matrices/{id}/"""
        url = reverse("matrix-detail", kwargs={"pk": matrix.id})
        response = api_client.patch(url, {"name": "Patched Name"}, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Patched Name"

        matrix.refresh_from_db()
        assert matrix.data == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]  # Unchanged

    def test_delete_matrix(self, api_client, matrix):
        """Test DELETE /api/matrices/{id}/"""
        url = reverse("matrix-detail", kwargs={"pk": matrix.id})
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Matrix.objects.count() == 0

    def test_export_csv(self, api_client, matrix):
        """Test GET /api/matrices/{id}/export_csv/"""
        url = reverse("matrix-export-csv", kwargs={"pk": matrix.id})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response["Content-Type"] == "text/csv"
        assert "attachment" in response["Content-Disposition"]
        assert response.content.decode() == "1,2,3\n4,5,6\n7,8,9"

    def test_export_json(self, api_client, matrix):
        """Test GET /api/matrices/{id}/export_json/"""
        url = reverse("matrix-export-json", kwargs={"pk": matrix.id})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Test Matrix"
        assert response.data["data"] == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    def test_import_csv_success(self, api_client):
        """Test POST /api/matrices/import_csv/ with valid file"""
        from django.core.files.uploadedfile import SimpleUploadedFile

        url = reverse("matrix-import-csv")
        csv_content = b"1,2,3\n4,5,6\n7,8,9"
        file = SimpleUploadedFile("test.csv", csv_content, content_type="text/csv")
        response = api_client.post(
            url, {"file": file, "name": "Imported Matrix"}, format="multipart"
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "Imported Matrix"
        assert response.data["rows"] == 3
        assert response.data["cols"] == 3
        assert Matrix.objects.filter(name="Imported Matrix").exists()

    def test_import_csv_no_file(self, api_client):
        """Test POST /api/matrices/import_csv/ without file"""
        url = reverse("matrix-import-csv")
        response = api_client.post(url, {"name": "No File"}, format="multipart")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "No se proporcionó" in response.data["error"]

    def test_import_csv_empty_file(self, api_client):
        """Test POST /api/matrices/import_csv/ with empty file"""
        from django.core.files.uploadedfile import SimpleUploadedFile

        url = reverse("matrix-import-csv")
        file = SimpleUploadedFile("empty.csv", b"", content_type="text/csv")
        response = api_client.post(url, {"file": file, "name": "Empty"}, format="multipart")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_import_csv_inconsistent_columns(self, api_client):
        """Test POST /api/matrices/import_csv/ with inconsistent column counts"""
        from django.core.files.uploadedfile import SimpleUploadedFile

        url = reverse("matrix-import-csv")
        csv_content = b"1,2\n3,4,5"
        file = SimpleUploadedFile("bad.csv", csv_content, content_type="text/csv")
        response = api_client.post(url, {"file": file}, format="multipart")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Inconsistencia" in response.data["error"]

    def test_import_csv_parse_error(self, api_client):
        """Test POST /api/matrices/import_csv/ with non-numeric data"""
        from django.core.files.uploadedfile import SimpleUploadedFile

        url = reverse("matrix-import-csv")
        csv_content = b"a,b\nc,d"
        file = SimpleUploadedFile("bad.csv", csv_content, content_type="text/csv")
        response = api_client.post(url, {"file": file}, format="multipart")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_import_csv_default_name(self, api_client):
        """Test POST /api/matrices/import_csv/ without explicit name"""
        from django.core.files.uploadedfile import SimpleUploadedFile

        url = reverse("matrix-import-csv")
        csv_content = b"1,2\n3,4"
        file = SimpleUploadedFile("data.csv", csv_content, content_type="text/csv")
        response = api_client.post(url, {"file": file}, format="multipart")

        assert response.status_code == status.HTTP_201_CREATED
        assert "Matriz importada" in response.data["name"]


@pytest.mark.django_db
class TestMatrixOperationsView:
    """Test suite for matrix operations endpoints"""

    def test_sum_operation(self, api_client, matrix_pair):
        """Test matrix addition"""
        matrix_a, matrix_b = matrix_pair
        url = reverse("sum-matrices")
        data = {"matrix_a_id": matrix_a.id, "matrix_b_id": matrix_b.id}
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["result"]["data"] == [[6, 8], [10, 12]]
        assert "execution_time_ms" in response.data

    def test_subtract_operation(self, api_client, matrix_pair):
        """Test matrix subtraction"""
        matrix_a, matrix_b = matrix_pair
        url = reverse("subtract-matrices")
        data = {"matrix_a_id": matrix_a.id, "matrix_b_id": matrix_b.id}
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["result"]["data"] == [[-4, -4], [-4, -4]]

    def test_multiply_operation(self, api_client, matrix_pair):
        """Test matrix multiplication"""
        matrix_a, matrix_b = matrix_pair
        url = reverse("multiply-matrices")
        data = {"matrix_a_id": matrix_a.id, "matrix_b_id": matrix_b.id}
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["result"]["data"] == [[19, 22], [43, 50]]

    def test_transpose_operation(self, api_client, matrix):
        """Test matrix transpose"""
        url = reverse("transpose-matrix")
        data = {"matrix_id": matrix.id}
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["result"]["data"] == [[1, 4, 7], [2, 5, 8], [3, 6, 9]]

    def test_determinant_operation(self, api_client, identity_matrix):
        """Test determinant calculation"""
        url = reverse("determinant-matrix")
        data = {"matrix_id": identity_matrix.id}
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["result"]["data"] == [[1.0]]

    def test_inverse_operation(self, api_client, identity_matrix):
        """Test matrix inversion"""
        url = reverse("inverse-matrix")
        data = {"matrix_id": identity_matrix.id}
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["result"]["data"] == [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

    def test_operation_with_invalid_matrix_id(self, api_client):
        """Test operation with nonexistent matrix"""
        url = reverse("transpose-matrix")
        data = {"matrix_id": 99999}
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_rank_operation(self, api_client, matrix):
        """Test rank calculation"""
        url = reverse("rank-matrix")
        data = {"matrix_id": matrix.id}
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["result"]["data"] == [[2.0]]
        assert "extra_data" not in response.data or response.data["extra_data"] is None

    def test_eigenvalues_operation(self, api_client, matrix):
        """Test eigenvalues calculation"""
        url = reverse("eigenvalues-matrix")
        data = {"matrix_id": matrix.id}
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert len(response.data["result"]["data"]) == 3

    def test_svd_operation(self, api_client, matrix):
        """Test SVD decomposition"""
        url = reverse("svd-matrix")
        data = {"matrix_id": matrix.id}
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["result"]["data"] is not None
        assert response.data["extra_data"] is not None
        assert set(response.data["extra_data"].keys()) == {"U", "S", "Vh"}

    def test_qr_operation(self, api_client, matrix):
        """Test QR decomposition"""
        url = reverse("qr-matrix")
        data = {"matrix_id": matrix.id}
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["extra_data"] is not None
        assert set(response.data["extra_data"].keys()) == {"Q", "R"}

    def test_cholesky_operation(self, api_client):
        """Test Cholesky decomposition with positive definite matrix"""
        from calculator.models import Matrix

        pd_matrix = Matrix.objects.create(name="PosDef", rows=2, cols=2, data=[[4, 2], [2, 3]])
        url = reverse("cholesky-matrix")
        data = {"matrix_id": pd_matrix.id}
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert len(response.data["result"]["data"]) == 2

    def test_operation_shape_mismatch_error(self, api_client):
        """Test operation error propagation (InvalidMatrixError)"""
        from calculator.models import Matrix

        m1 = Matrix.objects.create(name="A", rows=2, cols=2, data=[[1, 2], [3, 4]])
        m2 = Matrix.objects.create(name="B", rows=1, cols=3, data=[[5, 6, 7]])
        url = reverse("sum-matrices")
        data = {"matrix_a_id": m1.id, "matrix_b_id": m2.id}
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_singular_matrix_inverse_error(self, api_client):
        """Inverting a singular matrix returns 422 (NumericError)"""
        from calculator.models import Matrix

        singular = Matrix.objects.create(name="Singular", rows=2, cols=2, data=[[1, 2], [2, 4]])
        url = reverse("inverse-matrix")
        data = {"matrix_id": singular.id}
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.data.get("error") == "numeric_error"


@pytest.mark.django_db
class TestOperationViewSet:
    """Test suite for Operation API endpoints"""

    def _create_operation(self, matrix, op_type="TRANSPOSE", days_ago=0):
        """Helper to create an operation with a specific date"""
        from django.utils import timezone

        result = Matrix.objects.create(
            name="Result", rows=3, cols=3, data=[[1, 4, 7], [2, 5, 8], [3, 6, 9]]
        )
        op = Operation.objects.create(
            operation_type=op_type, matrix_a=matrix, result=result, execution_time_ms=50
        )
        if days_ago > 0:
            past = timezone.now() - timedelta(days=days_ago)
            Operation.objects.filter(pk=op.pk).update(created_at=past)
        return op

    def test_list_operations(self, api_client, matrix):
        """Test GET /api/operations/"""
        self._create_operation(matrix)
        url = "/api/operations-history/"
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_filter_by_date_from(self, api_client, matrix):
        """Test GET /api/operations-history/?date_from=..."""
        self._create_operation(matrix, days_ago=10)
        self._create_operation(matrix, days_ago=2)

        url = "/api/operations-history/?date_from=" + (timezone.now() - timedelta(days=5)).strftime(
            "%Y-%m-%d"
        )
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK

    def test_filter_by_date_range(self, api_client, matrix):
        """Test GET /api/operations-history/?date_from=...&date_to=..."""
        self._create_operation(matrix, days_ago=10)

        past = timezone.now() - timedelta(days=15)
        url = f"/api/operations-history/?date_from={past.strftime('%Y-%m-%d')}&date_to={(timezone.now() - timedelta(days=5)).strftime('%Y-%m-%d')}"
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestStatsView:
    """Test suite for statistics endpoint"""

    def test_get_stats(self, api_client, matrix):
        """Test GET /api/stats/"""
        result_matrix = Matrix.objects.create(
            name="Result", rows=3, cols=3, data=[[1, 4, 7], [2, 5, 8], [3, 6, 9]]
        )
        Operation.objects.create(
            operation_type="TRANSPOSE", matrix_a=matrix, result=result_matrix, execution_time_ms=50
        )
        Operation.objects.create(
            operation_type="TRANSPOSE", matrix_a=matrix, result=result_matrix, execution_time_ms=20
        )

        url = "/api/stats/"
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert "total_matrices" in response.data
        assert "total_operations" in response.data

    def test_stats_empty_database(self, api_client):
        """Test stats with empty database"""
        url = "/api/stats/"
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
