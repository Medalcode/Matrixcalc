import os
import logging
import pytest
from unittest.mock import patch
from django.apps import apps


@pytest.mark.django_db
class TestCalculatorConfig:
    @staticmethod
    def _config():
        return apps.get_app_config('calculator')

    def test_ready_skips_scheduler_by_default(self):
        config = self._config()
        with patch.object(config, 'start_scheduler') as mock_start:
            config.ready()
            mock_start.assert_not_called()

    def test_ready_starts_scheduler_when_enabled(self):
        os.environ['RUN_SCHEDULER'] = 'true'
        try:
            config = self._config()
            with patch.object(config, 'start_scheduler') as mock_start:
                config.ready()
                mock_start.assert_called_once()
        finally:
            os.environ.pop('RUN_SCHEDULER', None)

    def test_ready_skips_with_run_main(self):
        os.environ['RUN_SCHEDULER'] = 'true'
        os.environ['RUN_MAIN'] = 'true'
        try:
            config = self._config()
            with patch.object(config, 'start_scheduler') as mock_start:
                config.ready()
                mock_start.assert_not_called()
        finally:
            os.environ.pop('RUN_SCHEDULER', None)
            os.environ.pop('RUN_MAIN', None)

    def test_start_scheduler_creates_and_starts_scheduler(self):
        with patch('apscheduler.schedulers.background.BackgroundScheduler') as mock_scheduler_cls, \
             patch('apscheduler.triggers.cron.CronTrigger'):
            config = self._config()
            config.start_scheduler()

            mock_scheduler = mock_scheduler_cls.return_value
            mock_scheduler.add_job.assert_called_once()
            _, kwargs = mock_scheduler.add_job.call_args
            assert kwargs['id'] == 'cleanup_old_data'
            mock_scheduler.start.assert_called_once()

    def test_cleanup_task_calls_command(self):
        with patch('apscheduler.schedulers.background.BackgroundScheduler') as mock_scheduler_cls, \
             patch('apscheduler.triggers.cron.CronTrigger'), \
             patch('django.core.management.call_command') as mock_call_command:
            config = self._config()
            config.start_scheduler()

            mock_scheduler = mock_scheduler_cls.return_value
            func = mock_scheduler.add_job.call_args[0][0]
            func()
            mock_call_command.assert_called_once_with('cleanup_old_data')

    def test_cleanup_task_error_logged(self, caplog):
        caplog.set_level(logging.ERROR)
        with patch('apscheduler.schedulers.background.BackgroundScheduler') as mock_scheduler_cls, \
             patch('apscheduler.triggers.cron.CronTrigger'), \
             patch('django.core.management.call_command', side_effect=Exception("boom")):
            config = self._config()
            config.start_scheduler()

            mock_scheduler = mock_scheduler_cls.return_value
            func = mock_scheduler.add_job.call_args[0][0]
            func()
            assert "boom" in caplog.text
