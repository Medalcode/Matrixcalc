"""
Servicios de aplicación para MatrixCalc.

Este módulo contiene lógica de alto nivel que orquestra componentes
del sistema, como backups, limpiezas y orquestación de tareas largas.
"""

import logging
import os
from datetime import UTC, datetime
from typing import Any

from django.conf import settings
from django.core.management import call_command

logger = logging.getLogger(__name__)


def export_backup_service(output_path: str | None = None) -> dict[str, Any]:
    """
    Exporta un respaldo completo de la base de datos a un archivo JSON.
    """
    if output_path is None:
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(settings.BASE_DIR, "backups", f"backup_{timestamp}.json")

    try:
        call_command("export_backup", output=output_path)
        return {"status": "ok", "path": output_path}
    except Exception as e:
        logger.exception("Error in export_backup_service")
        return {"status": "error", "message": str(e)}


def cleanup_data_service(days: int | None = None, dry_run: bool = False) -> dict[str, Any]:
    """
    Limpia operaciones y matrices antiguas según la política de retención.
    """
    try:
        options = {"dry_run": dry_run}
        if days is not None:
            options["days"] = days

        call_command("cleanup_old_data", **options)
        return {"status": "ok"}
    except Exception as e:
        logger.exception("Error in cleanup_data_service")
        return {"status": "error", "message": str(e)}


def maintenance_super_skill(action: str, **kwargs) -> dict[str, Any]:
    """
    Dispatcher de Super-Skill para mantenimiento de plataforma.

    Args:
        action: 'backup' o 'cleanup'
        **kwargs: Parámetros específicos de cada acción.
    """
    if action == "backup":
        return export_backup_service(output_path=kwargs.get("output_path"))
    elif action == "cleanup":
        return cleanup_data_service(days=kwargs.get("days"), dry_run=kwargs.get("dry_run", False))
    else:
        return {"status": "error", "message": f"Acción desconocida: {action}"}
