"""Registro de skills de la app calculator.
Las skills implementadas aquí siguen la convención: <nombre>_skill(params...)
"""

from .backup import export_backup_skill
from .cleanup import cleanup_old_data_skill

__all__ = [
    'export_backup_skill',
    'cleanup_old_data_skill',
]
