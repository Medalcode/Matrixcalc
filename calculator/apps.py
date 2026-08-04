"""
Configuración de la app calculator.
"""

from django.apps import AppConfig


class CalculatorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "calculator"
    verbose_name = "Matrix Calculator"

    def ready(self):
        """
        Código que se ejecuta cuando la app está lista.
        Nota: El scheduling fue migrado a Celery Beat.
        """
        pass
