"""
Exception handlers personalizados para la API REST.
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

from calculator.utils.exceptions import InvalidMatrixError, NumericError


def custom_exception_handler(exc, context):
    """
    Exception handler personalizado que mapea excepciones del modelo
    a respuestas HTTP apropiadas.
    """
    # Llamar al handler por defecto de DRF primero
    response = exception_handler(exc, context)
    
    # Si DRF no manejó la excepción, manejar excepciones personalizadas
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
