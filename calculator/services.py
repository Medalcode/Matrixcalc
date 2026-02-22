"""
Servicios de aplicación para MatrixCalc.

Este módulo contiene lógica de alto nivel que orquestra componentes
del sistema, como backups, limpiezas y orquestación de tareas largas.
"""
import os
from datetime import datetime
from typing import Any, Dict, Optional
from django.conf import settings
from calculator.management.commands.export_backup import Command as ExportCommand
from calculator.management.commands.cleanup_old_data import Command as CleanupCommand


def export_backup_service(output_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Exporta un respaldo completo de la base de datos a un archivo JSON.
    """
    if output_path is None:
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        output_path = os.path.join(settings.BASE_DIR, 'backups', f'backup_{timestamp}.json')

    try:
        cmd = ExportCommand()
        cmd.handle(output=output_path)
        return {'status': 'ok', 'path': output_path}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def cleanup_data_service(days: Optional[int] = None, dry_run: bool = False) -> Dict[str, Any]:
    """
    Limpia operaciones y matrices antiguas según la política de retención.
    """
    try:
        cmd = CleanupCommand()
        options = {'dry_run': dry_run}
        if days is not None:
            options['days'] = days
        
        cmd.handle(**options)
        return {'status': 'ok'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
def maintenance_super_skill(action: str, **kwargs) -> Dict[str, Any]:
    """
    Dispatcher de Super-Skill para mantenimiento de plataforma.
    
    Args:
        action: 'backup' o 'cleanup'
        **kwargs: Parámetros específicos de cada acción.
    """
    if action == 'backup':
        return export_backup_service(output_path=kwargs.get('output_path'))
    elif action == 'cleanup':
        return cleanup_data_service(days=kwargs.get('days'), dry_run=kwargs.get('dry_run', False))
    else:
        return {'status': 'error', 'message': f'Acción desconocida: {action}'}
