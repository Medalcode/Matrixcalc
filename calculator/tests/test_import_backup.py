import json

import pytest
from django.core.management import call_command

from calculator.models import Matrix, Operation

BACKUP_MATRIX = [
    {
        "model": "calculator.matrix",
        "pk": 1,
        "fields": {
            "name": "Imported",
            "rows": 2,
            "cols": 2,
            "data": [[1, 2], [3, 4]],
            "created_at": "2024-01-01T00:00:00+00:00",
            "updated_at": "2024-01-01T00:00:00+00:00",
        },
    }
]

BACKUP_OPERATION = [
    {
        "model": "calculator.operation",
        "pk": 1,
        "fields": {
            "operation_type": "SUM",
            "matrix_a": 1,
            "matrix_b": 1,
            "result": 1,
            "extra_data": None,
            "created_at": "2024-01-01T00:00:00+00:00",
            "execution_time_ms": 10,
        },
    }
]


def _backup_file(tmp_path, data, name="backup.json"):
    path = tmp_path / name
    path.write_text(json.dumps(data), encoding="utf-8")
    return str(path)


@pytest.mark.django_db
class TestImportBackupCommand:
    def test_import_success(self, tmp_path):
        """Import a valid backup with one matrix and one operation"""
        data = {"version": "2.0", "matrices": BACKUP_MATRIX, "operations": BACKUP_OPERATION}
        path = _backup_file(tmp_path, data)
        call_command("import_backup", path)
        assert Matrix.objects.count() == 1
        assert Operation.objects.count() == 1
        m = Matrix.objects.get()
        assert m.name == "Imported"
        assert m.data == [[1, 2], [3, 4]]

    def test_import_empty(self, tmp_path):
        """Import a backup with no matrices or operations"""
        data = {"version": "2.0", "matrices": [], "operations": []}
        path = _backup_file(tmp_path, data)
        call_command("import_backup", path)
        assert Matrix.objects.count() == 0
        assert Operation.objects.count() == 0

    def test_import_file_not_found(self, tmp_path):
        """Import from a non-existent file"""
        path = str(tmp_path / "nope.json")
        call_command("import_backup", path)

    def test_import_invalid_json(self, tmp_path):
        """Import from a file with invalid JSON content"""
        path = str(tmp_path / "bad.json")
        with open(path, "w") as f:
            f.write("not json")
        call_command("import_backup", path)

    def test_import_old_version_warning(self, tmp_path):
        """Import a backup with old version (< 2.0) triggers warning"""
        data = {"version": "1.0", "matrices": [], "operations": []}
        path = _backup_file(tmp_path, data)
        call_command("import_backup", path)

    def test_import_with_clear(self, tmp_path):
        """--clear deletes existing data before importing"""
        Matrix.objects.create(name="Existing", rows=1, cols=1, data=[[0]])
        data = {"version": "2.0", "matrices": BACKUP_MATRIX, "operations": []}
        path = _backup_file(tmp_path, data)
        call_command("import_backup", path, clear=True)
        assert Matrix.objects.count() == 1
        assert Matrix.objects.get().name == "Imported"

    def test_import_error_in_transaction(self, tmp_path):
        """Invalid model in backup data triggers exception"""
        data = {
            "version": "2.0",
            "matrices": [{"model": "calculator.foo", "pk": 1, "fields": {}}],
            "operations": [],
        }
        path = _backup_file(tmp_path, data)
        with pytest.raises(Exception):
            call_command("import_backup", path)
