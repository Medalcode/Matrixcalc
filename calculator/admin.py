"""
Configuración del Django Admin para calculator.
"""
from django.contrib import admin
from calculator.models import Matrix, Operation


@admin.register(Matrix)
class MatrixAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'dimensions', 'created_at']
    list_filter = ['created_at', 'rows', 'cols']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'


@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = ['id', 'operation_type', 'matrix_a', 'matrix_b', 'created_at', 'execution_time_ms']
    list_filter = ['operation_type', 'created_at']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('matrix_a', 'matrix_b', 'result')
