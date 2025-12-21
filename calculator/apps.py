"""
Configuración de la app calculator.
"""
import os
from django.apps import AppConfig


class CalculatorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'calculator'
    verbose_name = 'Matrix Calculator'
    
    def ready(self):
        """
        Código que se ejecuta cuando la app está lista.
        Configura el scheduler para tareas programadas.
        """
        # Solo ejecutar scheduler si está habilitado y no en runserver reload
        if os.environ.get('RUN_SCHEDULER') == 'true' and not os.environ.get('RUN_MAIN'):
            self.start_scheduler()
    
    def start_scheduler(self):
        """Inicia el scheduler para tareas programadas."""
        from apscheduler.schedulers.background import BackgroundScheduler
        from apscheduler.triggers.cron import CronTrigger
        from django.core.management import call_command
        import logging
        
        logger = logging.getLogger(__name__)
        
        def cleanup_task():
            """Tarea de limpieza programada."""
            try:
                logger.info("Ejecutando limpieza automática...")
                call_command('cleanup_old_data')
                logger.info("Limpieza completada exitosamente")
            except Exception as e:
                logger.error(f"Error en limpieza automática: {e}")
        
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            cleanup_task,
            trigger=CronTrigger(hour=2, minute=0),  # 2:00 AM diario
            id='cleanup_old_data',
            name='Limpieza automática de datos antiguos',
            replace_existing=True
        )
        scheduler.start()
        logger.info("Scheduler iniciado: limpieza diaria a las 2:00 AM")
        
        # TODO v2.0: Agregar job para broadcast de stats via WebSocket
