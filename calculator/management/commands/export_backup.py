"""
Management command para exportar backup completo.
"""
import json
from django.core.management.base import BaseCommand
from django.core import serializers
from django.utils import timezone
from django.conf import settings
from calculator.models import Matrix, Operation


class Command(BaseCommand):
    help = 'Exporta todas las matrices y operaciones a JSON'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            help='Ruta del archivo de salida',
        )
    
    def handle(self, *args, **options):
        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
        output_path = options.get('output') or settings.BACKUP_DIR / f'backup_{timestamp}.json'
        
        self.stdout.write(f"Exportando backup a: {output_path}")
        
        # Serializar modelos
        matrices = Matrix.objects.all().order_by('id')
        operations = Operation.objects.all().select_related(
            'matrix_a', 'matrix_b', 'result'
        ).order_by('id')
        
        matrices_data = json.loads(serializers.serialize('json', matrices))
        operations_data = json.loads(serializers.serialize('json', operations))
        
        # Estructura del backup
        backup_data = {
            'version': '2.0',
            'timestamp': timezone.now().isoformat(),
            'database': 'postgresql',
            'total_matrices': len(matrices_data),
            'total_operations': len(operations_data),
            'matrices': matrices_data,
            'operations': operations_data
        }
        
        # Guardar a archivo
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2, ensure_ascii=False)
        
        self.stdout.write(
            self.style.SUCCESS(
                f"✓ Backup exportado: {len(matrices_data)} matrices, {len(operations_data)} operaciones"
            )
        )
        self.stdout.write(f"Archivo: {output_path}")
