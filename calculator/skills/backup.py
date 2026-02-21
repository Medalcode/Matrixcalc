from typing import Any, Dict
import os
from django.conf import settings

def export_backup_skill(output_path: str | None = None, *, include_media: bool = False) -> Dict[str, Any]:
    """Exporta un respaldo de la aplicación.

    Parámetros:
    - output_path: ruta destino (si None, usa ./backups con nombre timestamp)
    - include_media: si incluye ficheros grandes (no implementado aquí)

    Retorna: dict con status/result/meta
    """
    import json
    from datetime import datetime
    from calculator.management.commands.export_backup import Command as ExportCommand

    if output_path is None:
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        output_path = os.path.join(settings.BASE_DIR, 'backups', f'backup_{timestamp}.json')

    # Reutilizar la lógica del management command si está disponible
    try:
        cmd = ExportCommand()
        # El comando implementa handle() que escribe en backups/ por defecto;
        # para compatibilidad simple, invocamos handle() sin args y luego devolvemos la ruta.
        cmd.handle(output=output_path)
        return {'status': 'ok', 'result': {'path': output_path}}
    except Exception as exc:
        return {'status': 'error', 'error': str(exc)}
