from __future__ import annotations
from celery import shared_task

from .skills import export_backup_skill, cleanup_old_data_skill


@shared_task(bind=True, name='calculator.export_backup')
def export_backup_task(self, output_path: str | None = None, include_media: bool = False):
    """Tarea Celery que ejecuta la skill de exportar backup."""
    result = export_backup_skill(output_path=output_path, include_media=include_media)
    if result.get('status') != 'ok':
        raise Exception(f"export_backup failed: {result.get('error')}")
    return result


@shared_task(bind=True, name='calculator.cleanup_old_data')
def cleanup_old_data_task(self, dry_run: bool = False):
    result = cleanup_old_data_skill(dry_run=dry_run)
    if result.get('status') != 'ok':
        raise Exception(f"cleanup_old_data failed: {result.get('error')}")
    return result
