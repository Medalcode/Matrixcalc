"""
Tests for serializers
"""
import pytest
from calculator.serializers import (
    MatrixSerializer,
    MatrixOperationSerializer, MatrixBulkImportSerializer
)
from calculator.models import Matrix, Operation


@pytest.mark.django_db
class TestMatrixSerializer:
    """Test suite for MatrixSerializer"""
    
    def test_serialize_matrix(self, matrix):
        """Test serializing a matrix"""
        serializer = MatrixSerializer(matrix)
        data = serializer.data
        
        assert data['name'] == 'Test Matrix'
        assert data['rows'] == 3
        assert data['cols'] == 3
        assert data['data'] == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        assert 'id' in data
        assert 'created_at' in data
        assert 'updated_at' in data
        assert 'is_square' in data
        assert 'size' in data
    
    def test_deserialize_valid_matrix(self, sample_matrix_data):
        """Test deserializing valid matrix data"""
        serializer = MatrixSerializer(data=sample_matrix_data)
        assert serializer.is_valid()
        matrix = serializer.save()
        
        assert matrix.name == 'Test Matrix'
        assert matrix.rows == 3
        assert matrix.cols == 3
        assert matrix.data == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    
    def test_deserialize_invalid_rows(self):
        """Test validation of invalid rows"""
        data = {
            'name': 'Invalid',
            'rows': 0,
            'cols': 3,
            'data': [[1, 2, 3]]
        }
        serializer = MatrixSerializer(data=data)
        assert not serializer.is_valid()
        assert 'rows' in serializer.errors
    
    def test_deserialize_invalid_cols(self):
        """Test validation of invalid cols"""
        data = {
            'name': 'Invalid',
            'rows': 3,
            'cols': 0,
            'data': [[1], [2], [3]]
        }
        serializer = MatrixSerializer(data=data)
        assert not serializer.is_valid()
        assert 'cols' in serializer.errors
    
    def test_deserialize_mismatched_dimensions(self):
        """Test validation of mismatched dimensions"""
        data = {
            'name': 'Mismatch',
            'rows': 2,
            'cols': 2,
            'data': [[1, 2, 3], [4, 5, 6]]  # 2x3 instead of 2x2
        }
        serializer = MatrixSerializer(data=data)
        assert not serializer.is_valid()
        assert 'data' in serializer.errors
    
    def test_deserialize_invalid_data_type(self):
        """Test validation of invalid data types in matrix"""
        data = {
            'name': 'Invalid Types',
            'rows': 2,
            'cols': 2,
            'data': [['a', 'b'], ['c', 'd']]  # Strings instead of numbers
        }
        serializer = MatrixSerializer(data=data)
        assert not serializer.is_valid()
    
    def test_update_matrix(self, matrix):
        """Test updating a matrix through serializer"""
        new_data = {
            'name': 'Updated Matrix',
            'rows': 3,
            'cols': 3,
            'data': [[9, 8, 7], [6, 5, 4], [3, 2, 1]]
        }
        serializer = MatrixSerializer(matrix, data=new_data)
        assert serializer.is_valid()
        updated_matrix = serializer.save()
        
        assert updated_matrix.name == 'Updated Matrix'
        assert updated_matrix.data == [[9, 8, 7], [6, 5, 4], [3, 2, 1]]
    
    def test_partial_update(self, matrix):
        """Test partial update (PATCH)"""
        serializer = MatrixSerializer(
            matrix, 
            data={'name': 'Partially Updated'}, 
            partial=True
        )
        assert serializer.is_valid()
        updated_matrix = serializer.save()
        
        assert updated_matrix.name == 'Partially Updated'
        assert updated_matrix.data == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]  # Unchanged


@pytest.mark.django_db
class TestMatrixOperationSerializer:
    """Test suite for MatrixOperationSerializer"""
    
    def test_valid_binary_operation(self, matrix_pair):
        """Test valid binary operation data"""
        matrix_a, matrix_b = matrix_pair
        data = {
            'operation': 'sum',
            'matrix_a_id': matrix_a.id,
            'matrix_b_id': matrix_b.id
        }
        serializer = MatrixOperationSerializer(data=data)
        assert serializer.is_valid()
    
    def test_valid_unary_operation(self, matrix):
        """Test valid unary operation data"""
        data = {
            'operation': 'transpose',
            'matrix_a_id': matrix.id
        }
        serializer = MatrixOperationSerializer(data=data)
        assert serializer.is_valid()
    
    def test_invalid_operation_type(self, matrix):
        """Test invalid operation type"""
        data = {
            'operation': 'invalid_op',
            'matrix_a_id': matrix.id
        }
        serializer = MatrixOperationSerializer(data=data)
        assert not serializer.is_valid()
        assert 'operation' in serializer.errors
    
    def test_missing_matrix_a(self):
        """Test missing matrix_a_id"""
        data = {
            'operation': 'transpose'
        }
        serializer = MatrixOperationSerializer(data=data)
        assert not serializer.is_valid()
        assert 'matrix_a_id' in serializer.errors


@pytest.mark.django_db
class TestMatrixBulkImportSerializer:
    """Test suite for MatrixBulkImportSerializer"""
    
    def test_valid_bulk_import(self):
        """Test valid bulk import data"""
        data = {
            'matrices': [
                {
                    'name': 'Matrix 1',
                    'rows': 2,
                    'cols': 2,
                    'data': [[1, 2], [3, 4]]
                },
                {
                    'name': 'Matrix 2',
                    'rows': 2,
                    'cols': 2,
                    'data': [[5, 6], [7, 8]]
                }
            ]
        }
        serializer = MatrixBulkImportSerializer(data=data)
        assert serializer.is_valid()
        result = serializer.save()
        
        assert len(result['created']) == 2
        assert Matrix.objects.count() == 2
    
    def test_bulk_import_with_invalid_matrix(self):
        """Test bulk import with one invalid matrix"""
        data = {
            'matrices': [
                {
                    'name': 'Valid',
                    'rows': 2,
                    'cols': 2,
                    'data': [[1, 2], [3, 4]]
                },
                {
                    'name': 'Invalid',
                    'rows': 0,  # Invalid
                    'cols': 2,
                    'data': [[1, 2]]
                }
            ]
        }
        serializer = MatrixBulkImportSerializer(data=data)
        assert not serializer.is_valid()
