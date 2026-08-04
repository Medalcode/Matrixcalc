import pytest
from django.apps import apps


@pytest.mark.django_db
class TestCalculatorConfig:
    @staticmethod
    def _config():
        return apps.get_app_config("calculator")

    def test_app_config_metadata(self):
        config = self._config()
        assert config.name == "calculator"
        assert config.verbose_name == "Matrix Calculator"
        assert config.default_auto_field == "django.db.models.BigAutoField"

    def test_ready_executes_without_errors(self):
        config = self._config()
        # Ensure ready() executes cleanly
        config.ready()
