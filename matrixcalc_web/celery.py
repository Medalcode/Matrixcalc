from __future__ import annotations
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'matrixcalc_web.settings')

app = Celery('matrixcalc_web')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
