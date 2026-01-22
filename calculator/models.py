"""
Modelos Django para MatrixCalc Web.

Este módulo define los modelos de base de datos para almacenar matrices
y operaciones realizadas sobre ellas.
"""

from django.db import models
from django.core.validators import MinValueValidator


class Matrix(models.Model):
    """
    Modelo para almacenar matrices en la base de datos.
    
    Attributes:
        name: Nombre descriptivo de la matriz
        rows: Número de filas
        cols: Número de columnas
        data: Datos de la matriz en formato JSON (lista de listas)
        created_at: Fecha y hora de creación
        updated_at: Fecha y hora de última actualización
    """
    name = models.CharField(
        max_length=200,
        help_text="Nombre descriptivo de la matriz"
    )
    rows = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Número de filas"
    )
    cols = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Número de columnas"
    )
    data = models.JSONField(
        help_text="Datos de la matriz como lista de listas"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Matriz"
        verbose_name_plural = "Matrices"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['name']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.rows}x{self.cols})"
    
    @property
    def dimensions(self):
        """Retorna las dimensiones de la matriz como string."""
        return f"{self.rows}x{self.cols}"


class Operation(models.Model):
    """
    Modelo para almacenar operaciones matriciales realizadas.
    
    Attributes:
        operation_type: Tipo de operación realizada
        matrix_a: Primera matriz operando
        matrix_b: Segunda matriz operando (opcional para operaciones unarias)
        result: Matriz resultado de la operación
        created_at: Fecha y hora de ejecución
        execution_time_ms: Tiempo de ejecución en milisegundos
    """
    
    # Tipos de operaciones disponibles
    OPERATION_TYPES = [
        ('SUM', 'Suma'),
        ('SUBTRACT', 'Resta'),
        ('MULTIPLY', 'Multiplicación'),
        ('INVERSE', 'Inversa'),
        ('DETERMINANT', 'Determinante'),
        ('TRANSPOSE', 'Transpuesta'),
        # Nuevas operaciones v3.0
        ('RANK', 'Rango'),
        ('EIGEN', 'Valores/Vectores Propios'),
        ('SVD', 'Descomposición Valor Singular'),
        ('QR', 'Descomposición QR'),
        ('LU', 'Descomposición LU'),
        ('CHOLESKY', 'Descomposición Cholesky'),
    ]
    
    operation_type = models.CharField(
        max_length=20,
        choices=OPERATION_TYPES,
        help_text="Tipo de operación realizada"
    )
    matrix_a = models.ForeignKey(
        Matrix,
        on_delete=models.CASCADE,
        related_name='operations_as_a',
        help_text="Primera matriz operando"
    )
    matrix_b = models.ForeignKey(
        Matrix,
        on_delete=models.CASCADE,
        related_name='operations_as_b',
        null=True,
        blank=True,
        help_text="Segunda matriz operando (opcional)"
    )
    result = models.ForeignKey(
        Matrix,
        on_delete=models.CASCADE,
        related_name='operations_as_result',
        help_text="Matriz resultado principal"
    )
    extra_data = models.JSONField(
        null=True,
        blank=True,
        help_text="Datos adicionales o referencias a otras matrices resultado (ej: SVD components)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    execution_time_ms = models.PositiveIntegerField(
        help_text="Tiempo de ejecución en milisegundos"
    )
    
    class Meta:
        verbose_name = "Operación"
        verbose_name_plural = "Operaciones"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['operation_type']),
            models.Index(fields=['created_at']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        if self.matrix_b:
            return f"{self.get_operation_type_display()}: {self.matrix_a.name} y {self.matrix_b.name}"
        return f"{self.get_operation_type_display()}: {self.matrix_a.name}"
    
    @property
    def is_binary_operation(self):
        """Retorna True si la operación requiere dos matrices."""
        return self.operation_type in ['SUM', 'SUBTRACT', 'MULTIPLY']
