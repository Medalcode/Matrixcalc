"""
Exception handlers personalizados para Django REST Framework.

Mapea las excepciones del modelo numérico a respuestas HTTP apropiadas.
"""

from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework import status

from calculator.utils.exceptions import InvalidMatrixError, NumericError


def custom_exception_handler(exc, context):
    """
    Exception handler personalizado que maneja excepciones del modelo numérico.
    
    Mapeo:
    - InvalidMatrixError → 400 Bad Request
    - NumericError → 422 Unprocessable Entity
    """
    # Llamar al handler por defecto de DRF primero
    response = drf_exception_handler(exc, context)
    
    # Si DRF no manejó la excepción, intentamos manejarla nosotros
    if response is None:
        if isinstance(exc, InvalidMatrixError):
            return Response(
                {
                    'error': 'invalid_matrix',
                    'detail': str(exc)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        elif isinstance(exc, NumericError):
            return Response(
                {
                    'error': 'numeric_error',
                    'detail': str(exc)
                },
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
    
    return response
