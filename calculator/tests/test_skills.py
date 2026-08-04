import json
import os
from datetime import timedelta
from unittest import mock

import pytest
from django.utils import timezone

from calculator.models import Matrix, Operation
from calculator.services import cleanup_data_service, export_backup_service, maintenance_super_skill


@pytest.mark.django_db
def test_export_backup_skill_creates_file(tmp_path):
    # Crear datos mínimos
    m1 = Matrix.objects.create(name="A", rows=2, cols=2, data=[[1, 2], [3, 4]])
    m2 = Matrix.objects.create(name="B", rows=2, cols=2, data=[[5, 6], [7, 8]])
    _ = Operation.objects.create(
        operation_type="SUM", matrix_a=m1, matrix_b=m2, result=m1, execution_time_ms=10
    )

    out = tmp_path / "test_backup.json"
    result = export_backup_service(output_path=str(out))
    assert result.get("status") == "ok"
    assert out.exists()

    data = json.loads(out.read_text(encoding="utf-8"))
    assert "matrices" in data and "operations" in data
    assert data["total_matrices"] >= 2


@pytest.mark.django_db
def test_cleanup_old_data_skill_dry_run():
    now = timezone.now()
    old = now - timedelta(days=60)
    m = Matrix.objects.create(name="Old", rows=1, cols=1, data=[[0]])
    # Forzar created_at antiguo
    Matrix.objects.filter(pk=m.pk).update(created_at=old)

    # Run dry-run; no deletion should happen
    result = cleanup_data_service(dry_run=True, days=30)
    assert result.get("status") == "ok"
    assert Matrix.objects.filter(pk=m.pk).exists()


# =============================================================================
# export_backup_service — path por defecto y error
# =============================================================================


@pytest.mark.django_db
def test_export_backup_default_path():
    """Export with default output_path should succeed and return a path."""
    _ = Matrix.objects.create(name="X", rows=1, cols=1, data=[[42]])
    result = export_backup_service()
    assert result.get("status") == "ok"
    assert result.get("path") is not None
    assert "backup_" in result["path"]
    assert result["path"].endswith(".json")
    # Limpiar archivo creado
    if os.path.exists(result["path"]):
        os.unlink(result["path"])


@pytest.mark.django_db
def test_export_backup_error():
    """When ExportCommand fails, returns error status."""
    from calculator.management.commands.export_backup import Command

    with mock.patch.object(Command, "handle", side_effect=RuntimeError("write denied")):
        result = export_backup_service(output_path="/tmp/fail.json")

    assert result.get("status") == "error"
    assert "write denied" in result.get("message", "")


# =============================================================================
# cleanup_data_service — error
# =============================================================================


@pytest.mark.django_db
def test_cleanup_data_error():
    """When CleanupCommand fails, returns error status."""
    from calculator.management.commands.cleanup_old_data import Command

    with mock.patch.object(Command, "handle", side_effect=RuntimeError("db locked")):
        result = cleanup_data_service(dry_run=True)

    assert result.get("status") == "error"
    assert "db locked" in result.get("message", "")


# =============================================================================
# maintenance_super_skill
# =============================================================================


@pytest.mark.django_db
def test_maintenance_super_skill_backup(tmp_path):
    """Dispatcher with action='backup' delegates to export_backup_service."""
    _ = Matrix.objects.create(name="M", rows=1, cols=1, data=[[1]])
    out = tmp_path / "skill_backup.json"
    result = maintenance_super_skill("backup", output_path=str(out))
    assert result.get("status") == "ok"
    assert out.exists()


@pytest.mark.django_db
def test_maintenance_super_skill_cleanup():
    """Dispatcher with action='cleanup' delegates to cleanup_data_service."""
    result = maintenance_super_skill("cleanup", days=30, dry_run=True)
    assert result.get("status") == "ok"


def test_maintenance_super_skill_unknown_action():
    """Dispatcher with unknown action returns error."""
    result = maintenance_super_skill("reboot")
    assert result.get("status") == "error"
    assert "Acci\u00f3n desconocida" in result.get("message", "")
