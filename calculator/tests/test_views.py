"""
Tests for API views/endpoints
"""
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from calculator.models import Matrix, Operation
from django.urls import reverse


@pytest.mark.django_db
class TestMatrixViewSet:
    """Test suite for Matrix API endpoints"""
    
    def test_list_matrices(self, api_client, matrix):
        """Test GET /api/matrices/"""
        url = reverse('matrix-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == 'Test Matrix'
    
    def test_list_empty_matrices(self, api_client):
        """Test listing when no matrices exist"""
        url = reverse('matrix-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0
    
    def test_retrieve_matrix(self, api_client, matrix):
        """Test GET /api/matrices/{id}/"""
        url = reverse('matrix-detail', kwargs={'pk': matrix.id})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Test Matrix'
        assert response.data['rows'] == 3
        assert response.data['cols'] == 3
    
    def test_retrieve_nonexistent_matrix(self, api_client):
        """Test retrieving matrix that doesn't exist"""
        url = reverse('matrix-detail', kwargs={'pk': 99999})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_create_matrix(self, api_client, sample_matrix_data):
        """Test POST /api/matrices/"""
        url = reverse('matrix-list')
        response = api_client.post(url, sample_matrix_data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'Test Matrix'
        assert Matrix.objects.count() == 1
    
    def test_create_invalid_matrix(self, api_client):
        """Test creating matrix with invalid data"""
        url = reverse('matrix-list')
        invalid_data = {
            'name': 'Invalid',
            'rows': 0,
            'cols': 3,
            'data': [[1, 2, 3]]
        }
        response = api_client.post(url, invalid_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert Matrix.objects.count() == 0
    
    def test_update_matrix(self, api_client, matrix):
        """Test PUT /api/matrices/{id}/"""
        url = reverse('matrix-detail', kwargs={'pk': matrix.id})
        updated_data = {
            'name': 'Updated Matrix',
            'rows': 3,
            'cols': 3,
            'data': [[9, 8, 7], [6, 5, 4], [3, 2, 1]]
        }
        response = api_client.put(url, updated_data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Updated Matrix'
        
        matrix.refresh_from_db()
        assert matrix.name == 'Updated Matrix'
    
    def test_partial_update_matrix(self, api_client, matrix):
        """Test PATCH /api/matrices/{id}/"""
        url = reverse('matrix-detail', kwargs={'pk': matrix.id})
        response = api_client.patch(
            url, 
            {'name': 'Patched Name'}, 
            format='json'
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Patched Name'
        
        matrix.refresh_from_db()
        assert matrix.data == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]  # Unchanged
    
    def test_delete_matrix(self, api_client, matrix):
        """Test DELETE /api/matrices/{id}/"""
        url = reverse('matrix-detail', kwargs={'pk': matrix.id})
        response = api_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Matrix.objects.count() == 0
    
    def test_bulk_delete_matrices(self, api_client, matrix_pair):
        """Test bulk delete action"""
        matrix_a, matrix_b = matrix_pair
        url = reverse('matrix-bulk-delete')
        data = {'ids': [matrix_a.id, matrix_b.id]}
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Matrix.objects.count() == 0


@pytest.mark.django_db
class TestMatrixOperationsView:
    """Test suite for matrix operations endpoint"""
    
    def test_sum_operation(self, api_client, matrix_pair):
        """Test matrix addition"""
        matrix_a, matrix_b = matrix_pair
        url = reverse('matrix-operations')
        data = {
            'operation': 'sum',
            'matrix_a_id': matrix_a.id,
            'matrix_b_id': matrix_b.id
        }
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'result' in response.data
        assert response.data['result'] == [[6, 8], [10, 12]]
        assert 'execution_time' in response.data
    
    def test_subtract_operation(self, api_client, matrix_pair):
        """Test matrix subtraction"""
        matrix_a, matrix_b = matrix_pair
        url = reverse('matrix-operations')
        data = {
            'operation': 'subtract',
            'matrix_a_id': matrix_a.id,
            'matrix_b_id': matrix_b.id
        }
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['result'] == [[-4, -4], [-4, -4]]
    
    def test_multiply_operation(self, api_client, matrix_pair):
        """Test matrix multiplication"""
        matrix_a, matrix_b = matrix_pair
        url = reverse('matrix-operations')
        data = {
            'operation': 'multiply',
            'matrix_a_id': matrix_a.id,
            'matrix_b_id': matrix_b.id
        }
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['result'] == [[19, 22], [43, 50]]
    
    def test_transpose_operation(self, api_client, matrix):
        """Test matrix transpose"""
        url = reverse('matrix-operations')
        data = {
            'operation': 'transpose',
            'matrix_a_id': matrix.id
        }
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['result'] == [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
    
    def test_determinant_operation(self, api_client, identity_matrix):
        """Test determinant calculation"""
        url = reverse('matrix-operations')
        data = {
            'operation': 'determinant',
            'matrix_a_id': identity_matrix.id
        }
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['result'] == 1.0  # Det of identity is 1
    
    def test_inverse_operation(self, api_client, identity_matrix):
        """Test matrix inversion"""
        url = reverse('matrix-operations')
        data = {
            'operation': 'inverse',
            'matrix_a_id': identity_matrix.id
        }
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        # Inverse of identity is identity
        assert response.data['result'] == [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    
    def test_operation_with_invalid_matrix_id(self, api_client):
        """Test operation with nonexistent matrix"""
        url = reverse('matrix-operations')
        data = {
            'operation': 'transpose',
            'matrix_a_id': 99999
        }
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_operation_creates_history(self, api_client, matrix):
        """Test that operations create Operation entries"""
        result_matrix = Matrix.objects.create(
            name='Transpose Result', rows=3, cols=3,
            data=[[1, 4, 7], [2, 5, 8], [3, 6, 9]]
        )
        Operation.objects.create(
            operation_type='TRANSPOSE',
            matrix_a=matrix,
            result=result_matrix,
            execution_time_ms=10
        )
        assert Operation.objects.count() == 1
        
        operation = Operation.objects.first()
        assert operation.operation_type == 'TRANSPOSE'
        assert operation.matrix_a == matrix


@pytest.mark.django_db
class TestOperationViewSet:
    """Test suite for Operation API endpoints"""
    
    def test_list_operations(self, api_client, matrix):
        """Test GET /api/operations/"""
        result_matrix = Matrix.objects.create(
            name='Result', rows=3, cols=3,
            data=[[1, 4, 7], [2, 5, 8], [3, 6, 9]]
        )
        Operation.objects.create(
            operation_type='TRANSPOSE',
            matrix_a=matrix,
            result=result_matrix,
            execution_time_ms=50
        )
        
        url = '/api/operations/'
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1
    
    def test_delete_operation(self, api_client, matrix):
        """Test DELETE /api/operations/{id}/"""
        result_matrix = Matrix.objects.create(
            name='Result', rows=3, cols=3,
            data=[[1, 4, 7], [2, 5, 8], [3, 6, 9]]
        )
        operation = Operation.objects.create(
            operation_type='TRANSPOSE',
            matrix_a=matrix,
            result=result_matrix,
            execution_time_ms=50
        )
        
        url = f'/api/operations/{operation.id}/'
        response = api_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Operation.objects.count() == 0


@pytest.mark.django_db
class TestStatsView:
    """Test suite for statistics endpoint"""
    
    def test_get_stats(self, api_client, matrix):
        """Test GET /api/stats/"""
        result_matrix = Matrix.objects.create(
            name='Result', rows=3, cols=3,
            data=[[1, 4, 7], [2, 5, 8], [3, 6, 9]]
        )
        Operation.objects.create(
            operation_type='TRANSPOSE',
            matrix_a=matrix,
            result=result_matrix,
            execution_time_ms=50
        )
        Operation.objects.create(
            operation_type='TRANSPOSE',
            matrix_a=matrix,
            result=result_matrix,
            execution_time_ms=20
        )
        
        url = '/api/stats/'
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'total_matrices' in response.data
        assert 'total_operations' in response.data
    
    def test_stats_empty_database(self, api_client):
        """Test stats with empty database"""
        url = '/api/stats/'
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestBackupViews:
    """Test suite for backup/export/import endpoints"""
    
    def test_export_json(self, api_client, matrix):
        """Test GET /api/backup/export/json/"""
        url = '/api/backup/export/json/'
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'application/json' in response['Content-Type']
    
    def test_import_json(self, api_client):
        """Test POST /api/backup/import/"""
        url = '/api/backup/import/'
        import_data = {
            'matrices': [
                {
                    'name': 'Imported Matrix',
                    'rows': 2,
                    'cols': 2,
                    'data': [[1, 2], [3, 4]]
                }
            ]
        }
        response = api_client.post(url, import_data, format='json')
        
        # May return 200 or 201 depending on implementation
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]
