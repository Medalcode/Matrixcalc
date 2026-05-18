"""
Tests for API views/endpoints
"""
import pytest
from rest_framework import status
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
        assert response.data['count'] == 1
        assert response.data['results'][0]['name'] == 'Test Matrix'
    
    def test_list_empty_matrices(self, api_client):
        """Test listing when no matrices exist"""
        url = reverse('matrix-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 0
    
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
    

@pytest.mark.django_db
class TestMatrixOperationsView:
    """Test suite for matrix operations endpoints"""

    def test_sum_operation(self, api_client, matrix_pair):
        """Test matrix addition"""
        matrix_a, matrix_b = matrix_pair
        url = reverse('sum-matrices')
        data = {'matrix_a_id': matrix_a.id, 'matrix_b_id': matrix_b.id}
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['result']['data'] == [[6, 8], [10, 12]]
        assert 'execution_time_ms' in response.data

    def test_subtract_operation(self, api_client, matrix_pair):
        """Test matrix subtraction"""
        matrix_a, matrix_b = matrix_pair
        url = reverse('subtract-matrices')
        data = {'matrix_a_id': matrix_a.id, 'matrix_b_id': matrix_b.id}
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['result']['data'] == [[-4, -4], [-4, -4]]

    def test_multiply_operation(self, api_client, matrix_pair):
        """Test matrix multiplication"""
        matrix_a, matrix_b = matrix_pair
        url = reverse('multiply-matrices')
        data = {'matrix_a_id': matrix_a.id, 'matrix_b_id': matrix_b.id}
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['result']['data'] == [[19, 22], [43, 50]]

    def test_transpose_operation(self, api_client, matrix):
        """Test matrix transpose"""
        url = reverse('transpose-matrix')
        data = {'matrix_id': matrix.id}
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['result']['data'] == [[1, 4, 7], [2, 5, 8], [3, 6, 9]]

    def test_determinant_operation(self, api_client, identity_matrix):
        """Test determinant calculation"""
        url = reverse('determinant-matrix')
        data = {'matrix_id': identity_matrix.id}
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['result']['data'] == [[1.0]]

    def test_inverse_operation(self, api_client, identity_matrix):
        """Test matrix inversion"""
        url = reverse('inverse-matrix')
        data = {'matrix_id': identity_matrix.id}
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['result']['data'] == [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

    def test_operation_with_invalid_matrix_id(self, api_client):
        """Test operation with nonexistent matrix"""
        url = reverse('transpose-matrix')
        data = {'matrix_id': 99999}
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_404_NOT_FOUND


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
        
        url = '/api/operations-history/'
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1
    

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


