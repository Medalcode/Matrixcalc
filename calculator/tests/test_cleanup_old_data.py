"""
Tests para calculator.management.commands.cleanup_old_data.

Cubre: dry-run, eliminación real, auto-backup, conservación de datos,
errores de eliminación y de backup.
"""

from datetime import timedelta
from unittest import mock

import pytest
from django.core.management import call_command
from django.utils import timezone

from calculator.models import Matrix, Operation


@pytest.mark.django_db
class TestCleanupOldDataCommand:
    """Test suite for cleanup_old_data management command."""

    # ------------------------------------------------------------------
    # helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _old_matrix(name="OldM", days=60, **kw):
        now = timezone.now()
        m = Matrix.objects.create(name=name, rows=1, cols=1, data=[[0]], **kw)
        Matrix.objects.filter(pk=m.pk).update(created_at=now - timedelta(days=days))
        return Matrix.objects.get(pk=m.pk)

    @staticmethod
    def _recent_matrix(name="RecentM", **kw):
        return Matrix.objects.create(name=name, rows=1, cols=1, data=[[1]], **kw)

    @staticmethod
    def _old_operation(matrix, days=60):
        now = timezone.now()
        op = Operation.objects.create(
            operation_type="TRANSPOSE",
            matrix_a=matrix,
            result=matrix,
            execution_time_ms=10,
        )
        Operation.objects.filter(pk=op.pk).update(created_at=now - timedelta(days=days))
        return Operation.objects.get(pk=op.pk)

    # ------------------------------------------------------------------
    # dry-run
    # ------------------------------------------------------------------

    def test_dry_run_does_not_delete(self):
        m = self._old_matrix()
        self._old_operation(m)
        before = Matrix.objects.count()

        call_command("cleanup_old_data", days=30, dry_run=True)

        assert Matrix.objects.count() == before

    def test_dry_run_prints_counts(self, capsys):
        m = self._old_matrix()
        self._old_operation(m)

        call_command("cleanup_old_data", days=30, dry_run=True)

        captured = capsys.readouterr()
        assert "Operaciones a eliminar: 1" in captured.out
        assert "Simulación completada" in captured.out

    def test_dry_run_without_old_data(self, capsys):
        call_command("cleanup_old_data", days=30, dry_run=True)
        captured = capsys.readouterr()
        assert "Operaciones a eliminar: 0" in captured.out

    # ------------------------------------------------------------------
    # actual deletion
    # ------------------------------------------------------------------

    def test_deletes_old_operations(self):
        m = self._old_matrix()
        op = self._old_operation(m)
        assert Operation.objects.filter(pk=op.pk).exists()

        call_command("cleanup_old_data", days=30, dry_run=False)

        assert not Operation.objects.filter(pk=op.pk).exists()

    def test_deletes_orphaned_matrix(self):
        m = self._old_matrix()
        assert Matrix.objects.filter(pk=m.pk).exists()

        call_command("cleanup_old_data", days=30, dry_run=False)

        assert not Matrix.objects.filter(pk=m.pk).exists()

    def test_preserves_recent_data(self):
        m = self._recent_matrix()
        op = Operation.objects.create(
            operation_type="TRANSPOSE",
            matrix_a=m,
            result=m,
            execution_time_ms=10,
        )
        call_command("cleanup_old_data", days=30, dry_run=False)

        assert Matrix.objects.filter(pk=m.pk).exists()
        assert Operation.objects.filter(pk=op.pk).exists()

    def test_preserves_referenced_old_matrix(self):
        """Matrix referenced by a recent operation is preserved."""
        m = self._old_matrix()
        self._old_operation(m, days=5)  # recent operation (within retention)
        call_command("cleanup_old_data", days=30, dry_run=False)

        assert Matrix.objects.filter(pk=m.pk).exists()

    def test_deletes_multiple_old_operations(self):
        m1 = self._old_matrix("A")
        m2 = self._old_matrix("B")
        _ = self._old_operation(m1)
        _ = self._old_operation(m2)
        call_command("cleanup_old_data", days=30, dry_run=False)

        assert Operation.objects.count() == 0

    def test_uses_default_retention_days(self):
        """When --days is omitted, uses MATRIX_CONFIG['RETENTION_DAYS'] (30)."""
        m = self._old_matrix(days=40)
        self._old_operation(m, days=40)
        call_command("cleanup_old_data", dry_run=False)

        assert not Matrix.objects.filter(pk=m.pk).exists()

    # ------------------------------------------------------------------
    # auto-backup
    # ------------------------------------------------------------------

    def test_auto_backup_called_before_delete(self):
        m = self._old_matrix()
        self._old_operation(m)

        with mock.patch("django.core.management.call_command") as mock_call:
            call_command("cleanup_old_data", days=30, dry_run=False)

        mock_call.assert_any_call("export_backup")

    def test_continues_on_backup_failure(self):
        m = self._old_matrix()
        self._old_operation(m)

        with mock.patch(
            "django.core.management.call_command",
            side_effect=[RuntimeError("backup failed"), None],
        ):
            call_command("cleanup_old_data", days=30, dry_run=False)

        assert not Operation.objects.exists()

    def test_no_auto_backup_on_dry_run(self):
        m = self._old_matrix()
        self._old_operation(m)

        with mock.patch("django.core.management.call_command") as mock_call:
            call_command("cleanup_old_data", days=30, dry_run=True)

        mock_call.assert_not_called()

    # ------------------------------------------------------------------
    # error handling
    # ------------------------------------------------------------------

    def test_raises_on_deletion_error(self):
        m = self._old_matrix()
        self._old_operation(m)

        with (
            mock.patch(
                "calculator.management.commands.cleanup_old_data.transaction.atomic",
                side_effect=RuntimeError("db crash"),
            ),
            pytest.raises(RuntimeError, match="db crash"),
        ):
            call_command("cleanup_old_data", days=30, dry_run=False)

    def test_deletion_error_logged(self, caplog):
        m = self._old_matrix()
        self._old_operation(m)

        with (
            mock.patch(
                "calculator.management.commands.cleanup_old_data.transaction.atomic",
                side_effect=RuntimeError("db crash"),
            ),
            pytest.raises(RuntimeError),
        ):
            call_command("cleanup_old_data", days=30, dry_run=False)

        assert any("db crash" in msg for msg in caplog.messages)
