from typing import Any, Dict

def cleanup_old_data_skill(dry_run: bool = False, days: int | None = None) -> Dict[str, Any]:
    """Ejecuta la limpieza de datos antiguos.

    Retorna un dict con status y meta información.
    """
    try:
        # Importar la lógica del comando de management
        from calculator.management.commands.cleanup_old_data import Command as CleanupCommand

        cmd = CleanupCommand()
        # Pasar opciones al handle() para que respete dry-run y days
        options = {}
        if dry_run:
            options['dry_run'] = True
        if days is not None:
            options['days'] = days
        cmd.handle(**options)
        return {'status': 'ok'}
    except Exception as exc:
        return {'status': 'error', 'error': str(exc)}
