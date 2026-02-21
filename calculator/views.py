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


# --- Helpers de Operación ---

def _perform_matrix_operation(operation_type, matrix_a_id, matrix_b_id=None, extra_data=None):
    """
    Helper centralizado para ejecutar operaciones, medir tiempo y persistir resultados.
    """
    try:
        matrix_a = Matrix.objects.get(id=matrix_a_id)
        matrix_b = Matrix.objects.get(id=matrix_b_id) if matrix_b_id else None
    except Matrix.DoesNotExist:
        return Response({'error': 'Una o ambos matrices no existen'}, status=status.HTTP_404_NOT_FOUND)

    try:
        # Preparar operandos
        A = np.array(matrix_a.data, dtype=np.float64)
        B = np.array(matrix_b.data, dtype=np.float64) if matrix_b else None
        
        # Mapeo de funciones de utilidad
        ops_map = {
            'SUM': lambda: (safe_add(A, B), f"Suma: {matrix_a.name} + {matrix_b.name}"),
            'SUBTRACT': lambda: (safe_subtract(A, B), f"Resta: {matrix_a.name} - {matrix_b.name}"),
            'MULTIPLY': lambda: (safe_dot(A, B), f"Producto: {matrix_a.name} × {matrix_b.name}"),
            'INVERSE': lambda: (safe_inv(A), f"Inversa: {matrix_a.name}⁻¹"),
            'DETERMINANT': lambda: (np.array([[float(safe_det(A))]]), f"Det({matrix_a.name})"),
            'TRANSPOSE': lambda: (safe_transpose(A), f"Transpuesta: {matrix_a.name}ᵀ"),
            'RANK': lambda: (np.array([[float(safe_rank(A))]]), f"Rank({matrix_a.name})"),
            'EIGEN': lambda: (None, None), # Caso especial manejado abajo o via safe_eigenvalues directamente
            'SVD': lambda: (None, None),
            'QR': lambda: (None, None),
            'CHOLESKY': lambda: (safe_cholesky(A), f"Cholesky-L({matrix_a.name})"),
        }

        # Ejecución y timing
        start_time = time.time()
        
        # Casos especiales (v3.0) que retornan estructuras complejas
        if operation_type in ['EIGEN', 'SVD', 'QR']:
            if operation_type == 'EIGEN':
                data = safe_eigenvalues(A)
                # Resultado principal: autovalores como columna real
                res_arr = np.array([[v['real']] for v in data['eigenvalues']])
                name = f"Eigenvals({matrix_a.name})"
            elif operation_type == 'SVD':
                data = safe_svd(A)
                res_arr = np.array([[v] for v in data['S']]) # Valores singulares
                name = f"SVD-S({matrix_a.name})"
            elif operation_type == 'QR':
                data = safe_qr(A)
                res_arr = np.array(data['Q'])
                name = f"QR-Q({matrix_a.name})"
            
            extra_data = data # Guardar todo en JSON extra
        else:
            res_arr, name = ops_map[operation_type]()
            if isinstance(res_arr, list): res_arr = np.array(res_arr)

        execution_time_ms = int((time.time() - start_time) * 1000)

        # Persistir
        result_matrix = Matrix.objects.create(
            name=name,
            rows=res_arr.shape[0],
            cols=res_arr.shape[1],
            data=res_arr.tolist()
        )

        operation = Operation.objects.create(
            operation_type=operation_type,
            matrix_a=matrix_a,
            matrix_b=matrix_b,
            result=result_matrix,
            execution_time_ms=execution_time_ms,
            extra_data=extra_data
        )

        return Response(OperationSerializer(operation).data, status=status.HTTP_201_CREATED)

    except (InvalidMatrixError, NumericError):
        raise


# --- ViewSets ---
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
    """Suma dos matrices."""
    return _perform_matrix_operation('SUM', request.data.get('matrix_a_id'), request.data.get('matrix_b_id'))


@api_view(['POST'])
@ratelimit(key='ip', rate='50/m', method='POST')
def subtract_matrices(request):
    """Resta dos matrices."""
    return _perform_matrix_operation('SUBTRACT', request.data.get('matrix_a_id'), request.data.get('matrix_b_id'))


@api_view(['POST'])
@ratelimit(key='ip', rate='50/m', method='POST')
def multiply_matrices(request):
    """Multiplica dos matrices."""
    return _perform_matrix_operation('MULTIPLY', request.data.get('matrix_a_id'), request.data.get('matrix_b_id'))


@api_view(['POST'])
@ratelimit(key='ip', rate='50/m', method='POST')
def inverse_matrix(request):
    """Calcula la inversa de una matriz."""
    return _perform_matrix_operation('INVERSE', request.data.get('matrix_id'))


@api_view(['POST'])
@ratelimit(key='ip', rate='50/m', method='POST')
def determinant_matrix(request):
    """Calcula el determinante de una matriz."""
    # El helper ya guarda el resultado como 1x1, podemos añadir lógica extra si es necesario
    return _perform_matrix_operation('DETERMINANT', request.data.get('matrix_id'))


@api_view(['POST'])
@ratelimit(key='ip', rate='50/m', method='POST')
def transpose_matrix(request):
    """Calcula la transpuesta de una matriz."""
    return _perform_matrix_operation('TRANSPOSE', request.data.get('matrix_id'))










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
    return _perform_matrix_operation('RANK', request.data.get('matrix_id'))


@api_view(['POST'])
@ratelimit(key='ip', rate='20/m', method='POST')
def calculate_eigenvalues(request):
    """Calcula valores y vectores propios."""
    return _perform_matrix_operation('EIGEN', request.data.get('matrix_id'))


@api_view(['POST'])
@ratelimit(key='ip', rate='20/m', method='POST')
def calculate_svd(request):
    """Calcula descomposición SVD (U, S, Vh)."""
    return _perform_matrix_operation('SVD', request.data.get('matrix_id'))


@api_view(['POST'])
@ratelimit(key='ip', rate='20/m', method='POST')
def calculate_qr(request):
    """Calcula descomposición QR."""
    return _perform_matrix_operation('QR', request.data.get('matrix_id'))


@api_view(['POST'])
@ratelimit(key='ip', rate='20/m', method='POST')
def calculate_cholesky(request):
    """Calcula descomposición Cholesky."""
    return _perform_matrix_operation('CHOLESKY', request.data.get('matrix_id'))
