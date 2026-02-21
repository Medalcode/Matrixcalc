"""
Pytest configuration and fixtures for calculator tests
"""
import pytest
import json



@pytest.fixture
def user():
    """Create a test user"""
    from django.contrib.auth.models import User
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )


@pytest.fixture
def sample_matrix_data():
    """Sample matrix data for testing"""
    return {
        'name': 'Test Matrix',
        'rows': 3,
        'cols': 3,
        'data': [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    }


@pytest.fixture
def matrix(db, sample_matrix_data):
    """Create a test matrix"""
    from calculator.models import Matrix
    return Matrix.objects.create(**sample_matrix_data)  # type: ignore[attr-defined]


@pytest.fixture
def identity_matrix(db):
    """Create an identity matrix for testing"""
    from calculator.models import Matrix
    return Matrix.objects.create(  # type: ignore[attr-defined]
        name='Identity 3x3',
        rows=3,
        cols=3,
        data=[[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    )


@pytest.fixture
def matrix_pair(db):
    """Create two matrices for binary operations"""
    from calculator.models import Matrix

    matrix_a = Matrix.objects.create(  # type: ignore[attr-defined]
        name='Matrix A',
        rows=2,
        cols=2,
        data=[[1, 2], [3, 4]]
    )
    matrix_b = Matrix.objects.create(  # type: ignore[attr-defined]
        name='Matrix B',
        rows=2,
        cols=2,
        data=[[5, 6], [7, 8]]
    )
    return matrix_a, matrix_b


@pytest.fixture
def api_client():
    """Create an API client for testing"""
    from rest_framework.test import APIClient
    return APIClient()
