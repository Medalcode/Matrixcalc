import json
import os
from datetime import timedelta

import pytest
from django.utils import timezone

from calculator.skills.backup import export_backup_skill
from calculator.skills.cleanup import cleanup_old_data_skill
from calculator.models import Matrix, Operation
from django.conf import settings


@pytest.mark.django_db
def test_export_backup_skill_creates_file(tmp_path):
    # Crear datos mínimos
    m1 = Matrix.objects.create(name='A', rows=2, cols=2, data=[[1, 2], [3, 4]])
    m2 = Matrix.objects.create(name='B', rows=2, cols=2, data=[[5, 6], [7, 8]])
    op = Operation.objects.create(operation_type='SUM', matrix_a=m1, matrix_b=m2, result=m1, execution_time_ms=10)

    out = tmp_path / 'test_backup.json'
    result = export_backup_skill(output_path=str(out))
    assert result.get('status') == 'ok'
    assert out.exists()

    data = json.loads(out.read_text(encoding='utf-8'))
    assert 'matrices' in data and 'operations' in data
    assert data['total_matrices'] >= 2


@pytest.mark.django_db
def test_cleanup_old_data_skill_dry_run():
    now = timezone.now()
    old = now - timedelta(days=60)
    m = Matrix.objects.create(name='Old', rows=1, cols=1, data=[[0]])
    # Forzar created_at antiguo
    Matrix.objects.filter(pk=m.pk).update(created_at=old)

    # Run dry-run; no deletion should happen
    result = cleanup_old_data_skill(dry_run=True, days=30)
    assert result.get('status') == 'ok'
    assert Matrix.objects.filter(pk=m.pk).exists()
