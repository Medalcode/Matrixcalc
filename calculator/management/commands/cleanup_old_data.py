"""
Management command para limpiar datos antiguos.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from django.db import transaction
from django.db.models import Q
from datetime import timedelta
from calculator.models import Matrix, Operation
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Limpia operaciones y matrices antiguas según RETENTION_DAYS'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            help='Días de retención (sobrescribe configuración)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simula la limpieza sin eliminar datos',
        )
    
    def handle(self, *args, **options):
        days = options.get('days') or settings.MATRIX_CONFIG['RETENTION_DAYS']
        dry_run = options.get('dry_run', False)
        
        cutoff_date = timezone.now() - timedelta(days=days)
        
        self.stdout.write(
            self.style.WARNING(f"Limpiando datos anteriores a {cutoff_date.strftime('%Y-%m-%d %H:%M:%S')}")
        )
        
        if dry_run:
            self.stdout.write(self.style.NOTICE("Modo DRY RUN - No se eliminarán datos"))
        
        # Auto-backup antes de eliminar (solo si no es dry-run)
        if not dry_run:
            try:
                from django.core.management import call_command
                self.stdout.write("Creando backup automático...")
                call_command('export_backup')
                self.stdout.write(self.style.SUCCESS("✓ Backup creado"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error al crear backup: {e}"))
                self.stdout.write(self.style.WARNING("Continuando sin backup..."))
        
        # Contar operaciones a eliminar
        operations_to_delete = Operation.objects.filter(created_at__lt=cutoff_date)
        op_count = operations_to_delete.count()
        
        # Contar matrices huérfanas a eliminar
        matrices_to_delete = Matrix.objects.filter(
            Q(operations_as_a__isnull=True) &
            Q(operations_as_b__isnull=True) &
            Q(operations_as_result__isnull=True) &
            Q(created_at__lt=cutoff_date)
        )
        matrix_count = matrices_to_delete.count()
        
        self.stdout.write(f"Operaciones a eliminar: {op_count}")
        self.stdout.write(f"Matrices huérfanas a eliminar: {matrix_count}")
        
        if dry_run:
            self.stdout.write(self.style.SUCCESS("Simulación completada"))
            return
        
        # Eliminar con transacción
        try:
            with transaction.atomic():
                # Eliminar operaciones (cascade eliminará relaciones)
                deleted_ops = operations_to_delete.delete()
                
                # Eliminar matrices huérfanas
                deleted_matrices = matrices_to_delete.delete()
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ Eliminadas {deleted_ops[0]} operaciones y {deleted_matrices[0]} matrices"
                    )
                )
                
                logger.info(f"Limpieza completada: {deleted_ops[0]} ops, {deleted_matrices[0]} matrices")
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error durante limpieza: {e}"))
            logger.error(f"Error en limpieza: {e}")
            raise
