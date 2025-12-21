"""
Management command para importar backup.
"""
import json
from django.core.management.base import BaseCommand
from django.core import serializers
from django.db import transaction


class Command(BaseCommand):
    help = 'Importa matrices y operaciones desde backup JSON'
    
    def add_arguments(self, parser):
        parser.add_argument(
            'backup_file',
            type=str,
            help='Ruta del archivo de backup a importar',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Eliminar datos existentes antes de importar',
        )
    
    def handle(self, *args, **options):
        backup_file = options['backup_file']
        clear_existing = options.get('clear', False)
        
        self.stdout.write(f"Importando backup desde: {backup_file}")
        
        # Leer archivo
        try:
            with open(backup_file, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Archivo no encontrado: {backup_file}"))
            return
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f"Error al parsear JSON: {e}"))
            return
        
        # Validar versión
        version = backup_data.get('version', '1.0')
        if float(version) < 2.0:
            self.stdout.write(self.style.WARNING(f"Versión de backup antigua: {version}"))
        
        matrices_data = backup_data.get('matrices', [])
        operations_data = backup_data.get('operations', [])
        
        self.stdout.write(f"Matrices en backup: {len(matrices_data)}")
        self.stdout.write(f"Operaciones en backup: {len(operations_data)}")
        
        # Importar con transacción
        try:
            with transaction.atomic():
                if clear_existing:
                    from calculator.models import Matrix, Operation
                    self.stdout.write(self.style.WARNING("Eliminando datos existentes..."))
                    Operation.objects.all().delete()
                    Matrix.objects.all().delete()
                
                # Deserializar matrices
                self.stdout.write("Importando matrices...")
                matrices_json = json.dumps(matrices_data)
                for obj in serializers.deserialize('json', matrices_json):
                    obj.save()
                
                # Deserializar operaciones
                self.stdout.write("Importando operaciones...")
                operations_json = json.dumps(operations_data)
                for obj in serializers.deserialize('json', operations_json):
                    obj.save()
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ Importación completada: {len(matrices_data)} matrices, {len(operations_data)} operaciones"
                    )
                )
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error durante importación: {e}"))
            raise
