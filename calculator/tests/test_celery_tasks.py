"""
Tests para calculator.celery_tasks.

Verifica que las tareas Celery manejan correctamente
los casos de éxito y error de los servicios subyacentes.
"""
from unittest import mock

import pytest


@pytest.mark.django_db
class TestExportBackupTask:
    """Test suite for export_backup_task"""

    def test_success_returns_result(self):
        from calculator.celery_tasks import export_backup_task

        with mock.patch(
            'calculator.celery_tasks.export_backup_service',
            return_value={'status': 'ok', 'path': '/tmp/backup.json'}
        ):
            result = export_backup_task(output_path='/tmp/backup.json')

        assert result == {'status': 'ok', 'path': '/tmp/backup.json'}

    def test_failure_raises_exception(self):
        from calculator.celery_tasks import export_backup_task
        from calculator.services import export_backup_service

        with mock.patch(
            'calculator.celery_tasks.export_backup_service',
            return_value={'status': 'error', 'message': 'disk full'}
        ):
            with pytest.raises(Exception, match='export_backup failed: disk full'):
                export_backup_task()


@pytest.mark.django_db
class TestCleanupOldDataTask:
    """Test suite for cleanup_old_data_task"""

    def test_success_returns_result(self):
        from calculator.celery_tasks import cleanup_old_data_task

        with mock.patch(
            'calculator.celery_tasks.cleanup_data_service',
            return_value={'status': 'ok'}
        ):
            result = cleanup_old_data_task(dry_run=True, days=30)

        assert result == {'status': 'ok'}

    def test_failure_raises_exception(self):
        from calculator.celery_tasks import cleanup_old_data_task

        with mock.patch(
            'calculator.celery_tasks.cleanup_data_service',
            return_value={'status': 'error', 'message': 'permission denied'}
        ):
            with pytest.raises(Exception, match='cleanup_old_data failed: permission denied'):
                cleanup_old_data_task()
