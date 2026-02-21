"""
Excepciones y Handlers del Dominio para MatrixCalc.

Este módulo centraliza las excepciones personalizadas y el manejador 
de excepciones de Django REST Framework para asegurar respuestas consistentes.
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


class MatrixModelError(ValueError):
    """Clase base para errores del modelo matricial."""


class InvalidMatrixError(MatrixModelError):
    """Error cuando la entrada de la matriz es inválida (parseo, dimensiones, etc.)."""


class NumericError(MatrixModelError):
    """Error cuando una operación numérica falla (singularidad, mal condicionamiento)."""


def custom_exception_handler(exc, context):
    """
    Handler global para mapear excepciones de dominio a respuestas HTTP.
    """
    # Llamar al handler por defecto de DRF primero
    response = exception_handler(exc, context)
    
    # Si DRF no manejó la excepción, manejar excepciones de dominio
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
