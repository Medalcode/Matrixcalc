"""
Views (vistas) para la API REST de MatrixCalc.

Define los ViewSets y vistas función para operaciones matriciales,
con rate limiting y manejo de errores.
"""

import time
import numpy as np
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.db.models import Count, Avg, Q
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.http import HttpResponse, FileResponse
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

from calculator.models import Matrix, Operation
from calculator.serializers import MatrixSerializer, OperationSerializer, StatsSerializer
from calculator.utils import (
    parse_matrix, safe_add, safe_subtract, safe_dot,
    safe_inv, safe_det, safe_transpose,
    safe_rank, safe_eigenvalues, safe_svd, safe_qr, safe_cholesky,
    InvalidMatrixError, NumericError
)


# Helper function para aplicar rate limiting a ViewSets
def ratelimit_viewset(rate):
    def decorator(cls):
        cls = method_decorator(ratelimit(key='ip', rate=rate, method='POST'), name='create')(cls)
        cls = method_decorator(ratelimit(key='ip', rate=rate, method='PUT'), name='update')(cls)
        cls = method_decorator(ratelimit(key='ip', rate=rate, method='PATCH'), name='partial_update')(cls)
        cls = method_decorator(ratelimit(key='ip', rate=rate, method='DELETE'), name='destroy')(cls)
        return cls
    return decorator


@ratelimit_viewset('100/m')
class MatrixViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD de matrices.
    
    Permite listar, crear, actualizar y eliminar matrices.
    Incluye acciones personalizadas para exportar/importar CSV.
    """
    queryset = Matrix.objects.all()
    serializer_class = MatrixSerializer
    filterset_fields = ['name', 'rows', 'cols']
    ordering_fields = ['created_at', 'name', 'rows', 'cols']
    ordering = ['-created_at']
    
    @action(detail=True, methods=['get'])
    def export_csv(self, request, pk=None):
        """
        Exporta una matriz a formato CSV.
        
        Returns:
            HttpResponse con contenido CSV descargable
        """
        matrix = self.get_object()
        
        # Convertir data a CSV
        csv_lines = []
        for row in matrix.data:
            csv_lines.append(','.join(str(val) for val in row))
        csv_content = '\n'.join(csv_lines)
        
        response = HttpResponse(csv_content, content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="matrix_{matrix.id}_{matrix.name}.csv"'
        return response
    
    @action(detail=True, methods=['get'])
    def export_json(self, request, pk=None):
        """
        Exporta una matriz a formato JSON.
        
        Returns:
            Response con datos de la matriz en JSON
        """
        matrix = self.get_object()
        serializer = self.get_serializer(matrix)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    @method_decorator(ratelimit(key='ip', rate='20/m', method='POST'))
    def import_csv(self, request):
        """
        Importa una matriz desde un archivo CSV.
        
        Expected data:
            - file: Archivo CSV
            - name: Nombre para la matriz
        
        Returns:
            Response con matriz creada
        """
        if 'file' not in request.FILES:
            return Response(
                {'error': 'No se proporcionó archivo'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        file = request.FILES['file']
        name = request.data.get('name', f'Matriz importada {timezone.now().strftime("%Y%m%d_%H%M%S")}')
        
        try:
            # Leer contenido del archivo
            content = file.read().decode('utf-8')
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            
            if not lines:
                return Response(
                    {'error': 'El archivo CSV está vacío'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Parsear filas
            data = []
            for line in lines:
                row = [float(val.strip()) for val in line.split(',')]
                data.append(row)
            
            rows = len(data)
            cols = len(data[0]) if data else 0
            
            # Validar que todas las filas tengan el mismo número de columnas
            for i, row in enumerate(data):
                if len(row) != cols:
                    return Response(
                        {'error': f'Inconsistencia en columnas en fila {i+1}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Crear matriz
            matrix = Matrix.objects.create(
                name=name,
                rows=rows,
                cols=cols,
                data=data
            )
            
            serializer = self.get_serializer(matrix)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': f'Error al importar CSV: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )


class OperationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet de solo lectura para historial de operaciones.
    
    Permite listar y ver detalles de operaciones realizadas,
    con filtros por tipo y fecha.
    """
    queryset = Operation.objects.all().select_related('matrix_a', 'matrix_b', 'result')
    serializer_class = OperationSerializer
    filterset_fields = ['operation_type']
    ordering_fields = ['created_at', 'execution_time_ms']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        Permite filtrar por rango de fechas via query params.
        """
        queryset = super().get_queryset()
        
        # Filtro por rango de fechas
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        
        if date_from:
            queryset = queryset.filter(created_at__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__lte=date_to)
        
        return queryset


# Vistas función para operaciones matriciales

@api_view(['POST'])
@ratelimit(key='ip', rate='50/m', method='POST')
def sum_matrices(request):
    """
    Suma dos matrices.
    
    Body:
        - matrix_a_id: ID de la primera matriz
        - matrix_b_id: ID de la segunda matriz
    
    Returns:
        Matriz resultado y registro de operación
    """
    matrix_a_id = request.data.get('matrix_a_id')
    matrix_b_id = request.data.get('matrix_b_id')
    
    if not matrix_a_id or not matrix_b_id:
        return Response(
            {'error': 'Se requieren matrix_a_id y matrix_b_id'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        matrix_a = Matrix.objects.get(id=matrix_a_id)
        matrix_b = Matrix.objects.get(id=matrix_b_id)
    except Matrix.DoesNotExist:
        return Response(
            {'error': 'Una o ambas matrices no existen'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    try:
        # Convertir a numpy arrays
        A = np.array(matrix_a.data, dtype=np.float64)
        B = np.array(matrix_b.data, dtype=np.float64)
        
        # Ejecutar operación con timing
        start_time = time.time()
        result_array = safe_add(A, B)
        execution_time_ms = int((time.time() - start_time) * 1000)
        
        # Guardar resultado como nueva matriz
        result_matrix = Matrix.objects.create(
            name=f"Suma: {matrix_a.name} + {matrix_b.name}",
            rows=result_array.shape[0],
            cols=result_array.shape[1],
            data=result_array.tolist()
        )
        
        # Crear registro de operación
        operation = Operation.objects.create(
            operation_type='SUM',
            matrix_a=matrix_a,
            matrix_b=matrix_b,
            result=result_matrix,
            execution_time_ms=execution_time_ms
        )
        
        serializer = OperationSerializer(operation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except (InvalidMatrixError, NumericError) as e:
        # El custom exception handler manejará esto
        raise


@api_view(['POST'])
@ratelimit(key='ip', rate='50/m', method='POST')
def subtract_matrices(request):
    """Resta dos matrices."""
    matrix_a_id = request.data.get('matrix_a_id')
    matrix_b_id = request.data.get('matrix_b_id')
    
    if not matrix_a_id or not matrix_b_id:
        return Response(
            {'error': 'Se requieren matrix_a_id y matrix_b_id'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        matrix_a = Matrix.objects.get(id=matrix_a_id)
        matrix_b = Matrix.objects.get(id=matrix_b_id)
    except Matrix.DoesNotExist:
        return Response(
            {'error': 'Una o ambas matrices no existen'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    try:
        A = np.array(matrix_a.data, dtype=np.float64)
        B = np.array(matrix_b.data, dtype=np.float64)
        
        start_time = time.time()
        result_array = safe_subtract(A, B)
        execution_time_ms = int((time.time() - start_time) * 1000)
        
        result_matrix = Matrix.objects.create(
            name=f"Resta: {matrix_a.name} - {matrix_b.name}",
            rows=result_array.shape[0],
            cols=result_array.shape[1],
            data=result_array.tolist()
        )
        
        operation = Operation.objects.create(
            operation_type='SUBTRACT',
            matrix_a=matrix_a,
            matrix_b=matrix_b,
            result=result_matrix,
            execution_time_ms=execution_time_ms
        )
        
        serializer = OperationSerializer(operation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except (InvalidMatrixError, NumericError) as e:
        raise


@api_view(['POST'])
@ratelimit(key='ip', rate='50/m', method='POST')
def multiply_matrices(request):
    """Multiplica dos matrices."""
    matrix_a_id = request.data.get('matrix_a_id')
    matrix_b_id = request.data.get('matrix_b_id')
    
    if not matrix_a_id or not matrix_b_id:
        return Response(
            {'error': 'Se requieren matrix_a_id y matrix_b_id'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        matrix_a = Matrix.objects.get(id=matrix_a_id)
        matrix_b = Matrix.objects.get(id=matrix_b_id)
    except Matrix.DoesNotExist:
        return Response(
            {'error': 'Una o ambas matrices no existen'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    try:
        A = np.array(matrix_a.data, dtype=np.float64)
        B = np.array(matrix_b.data, dtype=np.float64)
        
        start_time = time.time()
        result_array = safe_dot(A, B)
        execution_time_ms = int((time.time() - start_time) * 1000)
        
        result_matrix = Matrix.objects.create(
            name=f"Producto: {matrix_a.name} × {matrix_b.name}",
            rows=result_array.shape[0],
            cols=result_array.shape[1],
            data=result_array.tolist()
        )
        
        operation = Operation.objects.create(
            operation_type='MULTIPLY',
            matrix_a=matrix_a,
            matrix_b=matrix_b,
            result=result_matrix,
            execution_time_ms=execution_time_ms
        )
        
        serializer = OperationSerializer(operation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except (InvalidMatrixError, NumericError) as e:
        raise


@api_view(['POST'])
@ratelimit(key='ip', rate='50/m', method='POST')
def inverse_matrix(request):
    """Calcula la inversa de una matriz."""
    matrix_id = request.data.get('matrix_id')
    
    if not matrix_id:
        return Response(
            {'error': 'Se requiere matrix_id'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        matrix = Matrix.objects.get(id=matrix_id)
    except Matrix.DoesNotExist:
        return Response(
            {'error': 'La matriz no existe'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    try:
        A = np.array(matrix.data, dtype=np.float64)
        
        start_time = time.time()
        result_array = safe_inv(A)
        execution_time_ms = int((time.time() - start_time) * 1000)
        
        result_matrix = Matrix.objects.create(
            name=f"Inversa: {matrix.name}⁻¹",
            rows=result_array.shape[0],
            cols=result_array.shape[1],
            data=result_array.tolist()
        )
        
        operation = Operation.objects.create(
            operation_type='INVERSE',
            matrix_a=matrix,
            result=result_matrix,
            execution_time_ms=execution_time_ms
        )
        
        serializer = OperationSerializer(operation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except (InvalidMatrixError, NumericError) as e:
        raise


@api_view(['POST'])
@ratelimit(key='ip', rate='50/m', method='POST')
def determinant_matrix(request):
    """Calcula el determinante de una matriz."""
    matrix_id = request.data.get('matrix_id')
    
    if not matrix_id:
        return Response(
            {'error': 'Se requiere matrix_id'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        matrix = Matrix.objects.get(id=matrix_id)
    except Matrix.DoesNotExist:
        return Response(
            {'error': 'La matriz no existe'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    try:
        A = np.array(matrix.data, dtype=np.float64)
        
        start_time = time.time()
        det_value = safe_det(A)
        execution_time_ms = int((time.time() - start_time) * 1000)
        
        # Para determinante, guardamos el escalar como matriz 1x1
        result_matrix = Matrix.objects.create(
            name=f"Det({matrix.name})",
            rows=1,
            cols=1,
            data=[[float(det_value)]]
        )
        
        operation = Operation.objects.create(
            operation_type='DETERMINANT',
            matrix_a=matrix,
            result=result_matrix,
            execution_time_ms=execution_time_ms
        )
        
        # Incluir el valor del determinante directamente
        serializer = OperationSerializer(operation)
        response_data = serializer.data
        response_data['determinant_value'] = float(det_value)
        
        return Response(response_data, status=status.HTTP_201_CREATED)
    except (InvalidMatrixError, NumericError) as e:
        raise


@api_view(['POST'])
@ratelimit(key='ip', rate='50/m', method='POST')
def transpose_matrix(request):
    """Calcula la transpuesta de una matriz."""
    matrix_id = request.data.get('matrix_id')
    
    if not matrix_id:
        return Response(
            {'error': 'Se requiere matrix_id'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        matrix = Matrix.objects.get(id=matrix_id)
    except Matrix.DoesNotExist:
        return Response(
            {'error': 'La matriz no existe'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    try:
        A = np.array(matrix.data, dtype=np.float64)
        
        start_time = time.time()
        result_array = safe_transpose(A)
        execution_time_ms = int((time.time() - start_time) * 1000)
        
        result_matrix = Matrix.objects.create(
            name=f"Transpuesta: {matrix.name}ᵀ",
            rows=result_array.shape[0],
            cols=result_array.shape[1],
            data=result_array.tolist()
        )
        
        operation = Operation.objects.create(
            operation_type='TRANSPOSE',
            matrix_a=matrix,
            result=result_matrix,
            execution_time_ms=execution_time_ms
        )
        
        serializer = OperationSerializer(operation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except (InvalidMatrixError, NumericError) as e:
        raise


@api_view(['GET'])
@ratelimit(key='ip', rate='30/m', method='GET')
def stats_view(request):
    """
    Retorna estadísticas agregadas del sistema.
    
    Returns:
        - total_matrices: Total de matrices guardadas
        - total_operations: Total de operaciones realizadas
        - operations_by_type: Conteo por tipo de operación
        - operations_timeline: Operaciones por día (últimos 30 días)
        - storage_mb: Tamaño aproximado de almacenamiento
        - average_execution_time_ms: Tiempo promedio de ejecución
        - recent_operations_count: Operaciones en los últimos 7 días
    """
    # Totales
    total_matrices = Matrix.objects.count()
    total_operations = Operation.objects.count()
    
    # Operaciones por tipo
    operations_by_type = Operation.objects.values('operation_type').annotate(
        count=Count('id'),
        avg_time=Avg('execution_time_ms')
    ).order_by('-count')
    
    # Timeline de operaciones (últimos 30 días)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    operations_timeline = Operation.objects.filter(
        created_at__gte=thirty_days_ago
    ).extra(
        select={'date': "DATE(created_at)"}
    ).values('date').annotate(
        count=Count('id')
    ).order_by('date')
    
    # Storage aproximado (en MB)
    # Nota: Para PostgreSQL podríamos usar pg_database_size, aquí usamos estimación
    storage_mb = (total_matrices * 0.01) + (total_operations * 0.001)  # Estimación burda
    
    # Tiempo promedio de ejecución
    avg_exec_time = Operation.objects.aggregate(
        avg_time=Avg('execution_time_ms')
    )['avg_time'] or 0
    
    # Operaciones recientes (últimos 7 días)
    seven_days_ago = timezone.now() - timedelta(days=7)
    recent_operations_count = Operation.objects.filter(
        created_at__gte=seven_days_ago
    ).count()
    
    # Preparar datos para serializer
    stats_data = {
        'total_matrices': total_matrices,
        'total_operations': total_operations,
        'operations_by_type': list(operations_by_type),
        'operations_timeline': list(operations_timeline),
        'storage_mb': round(storage_mb, 2),
        'average_execution_time_ms': round(avg_exec_time, 2),
        'recent_operations_count': recent_operations_count
    }
    
    serializer = StatsSerializer(data=stats_data)
    serializer.is_valid(raise_exception=True)
    
    return Response(serializer.data)


@api_view(['POST'])
@ratelimit(key='ip', rate='30/m', method='POST')
def calculate_rank(request):
    """Calcula el rango de una matriz."""
    matrix_id = request.data.get('matrix_id')
    
    if not matrix_id:
        return Response({'error': 'Se requiere matrix_id'}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        matrix = Matrix.objects.get(id=matrix_id)
        A = np.array(matrix.data, dtype=np.float64)
        
        start_time = time.time()
        rank_val = safe_rank(A)
        execution_time_ms = int((time.time() - start_time) * 1000)
        
        # Guardar resultado como matriz 1x1
        result_matrix = Matrix.objects.create(
            name=f"Rank({matrix.name})",
            rows=1, cols=1,
            data=[[float(rank_val)]]
        )
        
        operation = Operation.objects.create(
            operation_type='RANK',
            matrix_a=matrix,
            result=result_matrix,
            execution_time_ms=execution_time_ms,
            extra_data={'rank': rank_val}
        )
        
        return Response(OperationSerializer(operation).data, status=status.HTTP_201_CREATED)
    except Matrix.DoesNotExist:
         return Response({'error': 'La matriz no existe'}, status=status.HTTP_404_NOT_FOUND)
    except (InvalidMatrixError, NumericError):
        raise


@api_view(['POST'])
@ratelimit(key='ip', rate='20/m', method='POST')
def calculate_eigenvalues(request):
    """Calcula valores y vectores propios."""
    matrix_id = request.data.get('matrix_id')
    
    if not matrix_id:
        return Response({'error': 'Se requiere matrix_id'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        matrix = Matrix.objects.get(id=matrix_id)
        A = np.array(matrix.data, dtype=np.float64)
        
        start_time = time.time()
        eig_data = safe_eigenvalues(A)
        execution_time_ms = int((time.time() - start_time) * 1000)
        
        # Para resultado principal guardamos los autovalores como matriz diagonal (si son reales)
        # o como lista de 1 columna. Usaremos 1 columna con la parte Real.
        vals = eig_data['eigenvalues']
        rows = len(vals)
        real_vals_col = [[v['real']] for v in vals]
        
        result_matrix = Matrix.objects.create(
            name=f"Eigenvals({matrix.name})",
            rows=rows, cols=1,
            data=real_vals_col
        )
        
        operation = Operation.objects.create(
            operation_type='EIGEN',
            matrix_a=matrix,
            result=result_matrix,
            execution_time_ms=execution_time_ms,
            extra_data=eig_data # Guarda todo: vals complejos y vectores
        )
        
        return Response(OperationSerializer(operation).data, status=status.HTTP_201_CREATED)
    except Matrix.DoesNotExist:
         return Response({'error': 'La matriz no existe'}, status=status.HTTP_404_NOT_FOUND)
    except (InvalidMatrixError, NumericError):
        raise


@api_view(['POST'])
@ratelimit(key='ip', rate='20/m', method='POST')
def calculate_svd(request):
    """Calcula descomposición SVD (U, S, Vh)."""
    matrix_id = request.data.get('matrix_id')
    
    if not matrix_id:
        return Response({'error': 'Se requiere matrix_id'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        matrix = Matrix.objects.get(id=matrix_id)
        A = np.array(matrix.data, dtype=np.float64)
        
        start_time = time.time()
        svd_data = safe_svd(A)
        execution_time_ms = int((time.time() - start_time) * 1000)
        
        # Guardamos S (Valores singulares) como matriz resultado principal
        s_vals = svd_data['S']
        result_matrix = Matrix.objects.create(
            name=f"SVD-S({matrix.name})",
            rows=len(s_vals), cols=1,
            data=[[v] for v in s_vals]
        )
        
        operation = Operation.objects.create(
            operation_type='SVD',
            matrix_a=matrix,
            result=result_matrix,
            execution_time_ms=execution_time_ms,
            extra_data=svd_data # Contiene U, S, Vh completos
        )
        
        return Response(OperationSerializer(operation).data, status=status.HTTP_201_CREATED)
    except Matrix.DoesNotExist:
         return Response({'error': 'La matriz no existe'}, status=status.HTTP_404_NOT_FOUND)
    except (InvalidMatrixError, NumericError):
         raise


@api_view(['POST'])
@ratelimit(key='ip', rate='20/m', method='POST')
def calculate_qr(request):
    """Calcula descomposición QR."""
    matrix_id = request.data.get('matrix_id')
    
    if not matrix_id:
        return Response({'error': 'Se requiere matrix_id'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        matrix = Matrix.objects.get(id=matrix_id)
        A = np.array(matrix.data, dtype=np.float64)
        
        start_time = time.time()
        qr_data = safe_qr(A)
        execution_time_ms = int((time.time() - start_time) * 1000)
        
        # Guardamos Q como resultado principal
        q_data = qr_data['Q']
        result_matrix = Matrix.objects.create(
            name=f"QR-Q({matrix.name})",
            rows=len(q_data), cols=len(q_data[0]),
            data=q_data
        )
        
        operation = Operation.objects.create(
            operation_type='QR',
            matrix_a=matrix,
            result=result_matrix,
            execution_time_ms=execution_time_ms,
            extra_data=qr_data # Contiene Q y R
        )
        
        return Response(OperationSerializer(operation).data, status=status.HTTP_201_CREATED)
    except Matrix.DoesNotExist:
         return Response({'error': 'La matriz no existe'}, status=status.HTTP_404_NOT_FOUND)
    except (InvalidMatrixError, NumericError):
         raise


@api_view(['POST'])
@ratelimit(key='ip', rate='20/m', method='POST')
def calculate_cholesky(request):
    """Calcula descomposición Cholesky."""
    matrix_id = request.data.get('matrix_id')
    
    if not matrix_id:
        return Response({'error': 'Se requiere matrix_id'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        matrix = Matrix.objects.get(id=matrix_id)
        A = np.array(matrix.data, dtype=np.float64)
        
        start_time = time.time()
        L_data = safe_cholesky(A)
        execution_time_ms = int((time.time() - start_time) * 1000)
        
        # Guardamos L como resultado principal
        result_matrix = Matrix.objects.create(
            name=f"Cholesky-L({matrix.name})",
            rows=len(L_data), cols=len(L_data[0]),
            data=L_data
        )
        
        operation = Operation.objects.create(
            operation_type='CHOLESKY',
            matrix_a=matrix,
            result=result_matrix,
            execution_time_ms=execution_time_ms,
            # No extra data necesaria, L es el unico resultado
        )
        
        return Response(OperationSerializer(operation).data, status=status.HTTP_201_CREATED)
    except Matrix.DoesNotExist:
         return Response({'error': 'La matriz no existe'}, status=status.HTTP_404_NOT_FOUND)
    except (InvalidMatrixError, NumericError):
         raise
