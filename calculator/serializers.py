"""
Serializers para la API REST de MatrixCalc.

Define la serialización/deserialización de modelos Matrix y Operation,
incluyendo validaciones personalizadas.
"""

import numpy as np
from rest_framework import serializers
from django.conf import settings

from calculator.models import Matrix, Operation
from calculator.utils import parse_matrix, InvalidMatrixError


class MatrixSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Matrix.
    
    Maneja la conversión entre formato JSON de la API y el modelo Django,
    incluyendo validación de dimensiones y datos matriciales.
    """
    dimensions = serializers.ReadOnlyField()
    
    class Meta:
        model = Matrix
        fields = ['id', 'name', 'rows', 'cols', 'data', 'dimensions', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def validate(self, attrs):
        """
        Valida que las dimensiones no excedan el límite configurado
        y que los datos sean consistentes con rows y cols.
        """
        rows = attrs.get('rows')
        cols = attrs.get('cols')
        data = attrs.get('data')
        
        # Validar dimensiones máximas
        max_dim = settings.MATRIX_CONFIG['MAX_DIMENSION']
        if rows > max_dim or cols > max_dim:
            raise serializers.ValidationError(
                f"Las dimensiones de la matriz no pueden exceder {max_dim}x{max_dim}. "
                f"Dimensiones solicitadas: {rows}x{cols}"
            )
        
        # Validar que data sea una lista de listas
        if not isinstance(data, list):
            raise serializers.ValidationError("Los datos deben ser una lista de listas.")
        
        if len(data) != rows:
            raise serializers.ValidationError(
                f"Se esperaban {rows} filas, pero se recibieron {len(data)}."
            )
        
        for i, row in enumerate(data):
            if not isinstance(row, list):
                raise serializers.ValidationError(
                    f"La fila {i} debe ser una lista."
                )
            if len(row) != cols:
                raise serializers.ValidationError(
                    f"Se esperaban {cols} columnas en la fila {i}, pero se recibieron {len(row)}."
                )
            # Validar que todos los valores sean numéricos
            for j, val in enumerate(row):
                if not isinstance(val, (int, float)):
                    raise serializers.ValidationError(
                        f"El valor en posición ({i},{j}) no es numérico: {val}"
                    )
        
        return attrs
    
    def create(self, validated_data):
        """
        Crea una matriz validando los datos con parse_matrix.
        """
        rows = validated_data['rows']
        cols = validated_data['cols']
        data = validated_data['data']
        
        # Convertir lista de listas a string CSV para parse_matrix
        flat_values = [str(val) for row in data for val in row]
        text = ', '.join(flat_values)
        
        try:
            # Validar con parse_matrix (levanta InvalidMatrixError si hay problemas)
            parsed = parse_matrix(text, rows, cols)
            # Convertir de vuelta a lista de listas para almacenar
            validated_data['data'] = parsed.tolist()
        except InvalidMatrixError as e:
            raise serializers.ValidationError(str(e))
        
        return super().create(validated_data)
    
    def to_representation(self, instance):
        """
        Personaliza la representación de salida para asegurar formato correcto.
        """
        representation = super().to_representation(instance)
        # Asegurar que data sea lista de listas (no array numpy)
        if isinstance(instance.data, np.ndarray):
            representation['data'] = instance.data.tolist()
        return representation


class OperationSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Operation.
    
    Incluye información completa de las matrices involucradas
    en formato nested.
    """
    matrix_a = MatrixSerializer(read_only=True)
    matrix_b = MatrixSerializer(read_only=True, allow_null=True)
    result = MatrixSerializer(read_only=True)
    operation_display = serializers.CharField(source='get_operation_type_display', read_only=True)
    
    class Meta:
        model = Operation
        fields = [
            'id',
            'operation_type',
            'operation_display',
            'matrix_a',
            'matrix_b',
            'result',
            'created_at',
            'execution_time_ms'
        ]
        read_only_fields = ['created_at']


class StatsSerializer(serializers.Serializer):
    """
    Serializer para estadísticas agregadas del sistema.
    """
    total_matrices = serializers.IntegerField()
    total_operations = serializers.IntegerField()
    operations_by_type = serializers.ListField(
        child=serializers.DictField()
    )
    operations_timeline = serializers.ListField(
        child=serializers.DictField()
    )
    storage_mb = serializers.FloatField()
    average_execution_time_ms = serializers.FloatField()
    recent_operations_count = serializers.IntegerField()
