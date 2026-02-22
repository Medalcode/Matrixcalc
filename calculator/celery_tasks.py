from __future__ import annotations
from celery import shared_task

from .services import export_backup_service, cleanup_data_service


@shared_task(bind=True, name='calculator.export_backup')
def export_backup_task(self, output_path: str | None = None):
    """Tarea Celery que ejecuta el servicio de exportación."""
    result = export_backup_service(output_path=output_path)
    if result.get('status') != 'ok':
        raise Exception(f"export_backup failed: {result.get('message')}")
    return result


@shared_task(bind=True, name='calculator.cleanup_old_data')
def cleanup_old_data_task(self, dry_run: bool = False, days: int | None = None):
    """Tarea Celery que ejecuta el servicio de limpieza."""
    result = cleanup_data_service(dry_run=dry_run, days=days)
    if result.get('status') != 'ok':
        raise Exception(f"cleanup_old_data failed: {result.get('message')}")
    return result
