"""
Tests for serializers
"""
import pytest
import numpy as np
from unittest.mock import patch
from calculator.serializers import MatrixSerializer
from calculator.models import Matrix
from calculator.utils import InvalidMatrixError


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
        assert 'dimensions' in data
        assert data['dimensions'] == '3x3'
    
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

    def test_validate_exceeds_max_dimension(self):
        """Test validation when rows/cols exceed MAX_DIMENSION (100)"""
        data = {
            'name': 'Too Big',
            'rows': 101,
            'cols': 2,
            'data': [[1, 2]] * 101
        }
        serializer = MatrixSerializer(data=data)
        assert not serializer.is_valid()

    def test_validate_data_not_a_list(self):
        """Test validation when data is not a list"""
        data = {
            'name': 'Bad Data',
            'rows': 2,
            'cols': 2,
            'data': 'not_a_list'
        }
        serializer = MatrixSerializer(data=data)
        assert not serializer.is_valid()

    def test_validate_row_count_mismatch(self):
        """Test validation when len(data) != rows"""
        data = {
            'name': 'Row Mismatch',
            'rows': 2,
            'cols': 2,
            'data': [[1, 2], [3, 4], [5, 6]]
        }
        serializer = MatrixSerializer(data=data)
        assert not serializer.is_valid()

    def test_validate_row_not_a_list(self):
        """Test validation when a row is not a list"""
        data = {
            'name': 'Bad Row',
            'rows': 2,
            'cols': 2,
            'data': [[1, 2], 'not_a_list']
        }
        serializer = MatrixSerializer(data=data)
        assert not serializer.is_valid()

    @patch('calculator.serializers.parse_matrix')
    def test_create_parse_matrix_error(self, mock_parse):
        """Test create when parse_matrix raises InvalidMatrixError"""
        mock_parse.side_effect = InvalidMatrixError("parse error")
        data = {
            'name': 'Test Matrix',
            'rows': 3,
            'cols': 3,
            'data': [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        }
        serializer = MatrixSerializer(data=data)
        assert serializer.is_valid()
        with pytest.raises(Exception):
            serializer.save()

    def test_to_representation_with_ndarray(self):
        """Test to_representation when data is an ndarray"""
        matrix = Matrix(name='test', rows=2, cols=2, data=np.array([[1, 2], [3, 4]]))
        serializer = MatrixSerializer()
        representation = serializer.to_representation(matrix)
        assert representation['data'] == [[1, 2], [3, 4]]


