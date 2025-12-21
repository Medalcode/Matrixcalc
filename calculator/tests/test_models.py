"""
Tests for Matrix and MatrixHistory models
"""
import pytest
from django.core.exceptions import ValidationError
from calculator.models import Matrix, Operation
import json


@pytest.mark.django_db
class TestMatrixModel:
    """Test suite for Matrix model"""
    
    def test_create_matrix(self, sample_matrix_data):
        """Test creating a matrix"""
        matrix = Matrix.objects.create(**sample_matrix_data)
        assert matrix.name == 'Test Matrix'
        assert matrix.rows == 3
        assert matrix.cols == 3
        assert matrix.data == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        assert matrix.created_at is not None
        assert matrix.updated_at is not None
    
    def test_matrix_str_representation(self, matrix):
        """Test matrix string representation"""
        assert str(matrix) == 'Test Matrix (3x3)'
    
    def test_matrix_dimensions_property(self, matrix):
        """Test matrix dimensions calculation"""
        assert matrix.dimensions == '3x3'
    
    def test_matrix_validation_rows_cols(self):
        """Test validation of rows and cols"""
        with pytest.raises(ValidationError):
            matrix = Matrix(
                name='Invalid', rows=0, cols=3,
                data=[[1, 2, 3]]
            )
            matrix.full_clean()
    
    def test_matrix_empty_data(self):
        """Test creating matrix with empty data"""
        matrix = Matrix.objects.create(
            name='Empty', rows=2, cols=2, data=[]
        )
        assert matrix.data == []
    
    def test_matrix_update(self, matrix):
        """Test updating matrix data"""
        original_updated = matrix.updated_at
        matrix.data = [[9, 8, 7], [6, 5, 4], [3, 2, 1]]
        matrix.save()
        assert matrix.data[0][0] == 9
        assert matrix.updated_at >= original_updated
    
    def test_matrix_deletion(self, matrix):
        """Test deleting a matrix"""
        matrix_id = matrix.id
        matrix.delete()
        assert not Matrix.objects.filter(id=matrix_id).exists()


@pytest.mark.django_db
class TestOperationModel:
    """Test suite for Operation model"""
    
    def test_create_operation(self, matrix_pair):
        """Test creating an operation entry"""
        matrix_a, matrix_b = matrix_pair
        result = Matrix.objects.create(
            name='Result', rows=2, cols=2,
            data=[[6, 8], [10, 12]]
        )
        operation = Operation.objects.create(
            operation_type='SUM',
            matrix_a=matrix_a,
            matrix_b=matrix_b,
            result=result,
            execution_time_ms=50
        )
        assert operation.operation_type == 'SUM'
        assert operation.matrix_a == matrix_a
        assert operation.matrix_b == matrix_b
        assert operation.result == result
        assert operation.execution_time_ms == 50
        assert operation.created_at is not None
    
    def test_operation_str_representation(self, matrix_pair):
        """Test operation string representation"""
        matrix_a, matrix_b = matrix_pair
        result = Matrix.objects.create(
            name='Result', rows=2, cols=2,
            data=[[19, 22], [43, 50]]
        )
        operation = Operation.objects.create(
            operation_type='MULTIPLY',
            matrix_a=matrix_a,
            matrix_b=matrix_b,
            result=result,
            execution_time_ms=30
        )
        op_str = str(operation)
        assert 'Matrix A' in op_str
        assert 'Matrix B' in op_str
    
    def test_unary_operation(self, matrix):
        """Test unary operation (transpose)"""
        result = Matrix.objects.create(
            name='Transposed', rows=3, cols=3,
            data=[[1, 4, 7], [2, 5, 8], [3, 6, 9]]
        )
        operation = Operation.objects.create(
            operation_type='TRANSPOSE',
            matrix_a=matrix,
            matrix_b=None,
            result=result,
            execution_time_ms=10
        )
        assert operation.matrix_b is None
        assert operation.is_binary_operation is False
    
    def test_binary_operation_check(self, matrix_pair):
        """Test is_binary_operation property"""
        matrix_a, matrix_b = matrix_pair
        result = Matrix.objects.create(
            name='Sum Result', rows=2, cols=2,
            data=[[6, 8], [10, 12]]
        )
        operation = Operation.objects.create(
            operation_type='SUM',
            matrix_a=matrix_a,
            matrix_b=matrix_b,
            result=result,
            execution_time_ms=20
        )
        assert operation.is_binary_operation is True
    
    def test_cascade_delete_matrix(self, matrix):
        """Test that deleting matrix cascades to operations"""
        result = Matrix.objects.create(
            name='Result', rows=3, cols=3,
            data=[[1, 4, 7], [2, 5, 8], [3, 6, 9]]
        )
        Operation.objects.create(
            operation_type='TRANSPOSE',
            matrix_a=matrix,
            result=result,
            execution_time_ms=10
        )
        matrix_id = matrix.id
        matrix.delete()
        # Operation should be deleted due to CASCADE
        assert not Matrix.objects.filter(id=matrix_id).exists()
        assert Operation.objects.count() == 0
