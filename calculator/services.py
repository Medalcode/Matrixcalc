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


class OperationService:
    """
    Servicio de capa de aplicación para ejecutar y persistir operaciones matriciales.
    Desacopla la lógica de negocio y timing de las vistas HTTP / controladores.
    """

    @staticmethod
    def execute_matrix_operation(
        operation_type: str, matrix_a: Any, matrix_b: Any = None, extra_data: Any = None
    ) -> Any:
        """
        Ejecuta la operación matemática solicitada, mide tiempo de ejecución,
        crea la matriz resultado y guarda el registro de Operation.
        """
        import time
        import numpy as np
        from calculator.models import Matrix, Operation
        from calculator.utils import (
            safe_add,
            safe_cholesky,
            safe_det,
            safe_dot,
            safe_eigenvalues,
            safe_inv,
            safe_qr,
            safe_rank,
            safe_subtract,
            safe_svd,
            safe_transpose,
        )

        A = np.array(matrix_a.data, dtype=np.float64)
        B = np.array(matrix_b.data, dtype=np.float64) if matrix_b else None

        ops_map = {
            "SUM": lambda: (safe_add(A, B), f"Suma: {matrix_a.name} + {matrix_b.name}"),
            "SUBTRACT": lambda: (safe_subtract(A, B), f"Resta: {matrix_a.name} - {matrix_b.name}"),
            "MULTIPLY": lambda: (safe_dot(A, B), f"Producto: {matrix_a.name} × {matrix_b.name}"),
            "INVERSE": lambda: (safe_inv(A), f"Inversa: {matrix_a.name}⁻¹"),
            "DETERMINANT": lambda: (np.array([[float(safe_det(A))]]), f"Det({matrix_a.name})"),
            "TRANSPOSE": lambda: (safe_transpose(A), f"Transpuesta: {matrix_a.name}ᵀ"),
            "RANK": lambda: (np.array([[float(safe_rank(A))]]), f"Rank({matrix_a.name})"),
            "EIGEN": lambda: (None, None),
            "SVD": lambda: (None, None),
            "QR": lambda: (None, None),
            "CHOLESKY": lambda: (safe_cholesky(A), f"Cholesky-L({matrix_a.name})"),
        }

        start_time = time.time()

        if operation_type in ["EIGEN", "SVD", "QR"]:
            if operation_type == "EIGEN":
                data = safe_eigenvalues(A)
                res_arr = np.array([[v["real"]] for v in data["eigenvalues"]])
                name = f"Eigenvals({matrix_a.name})"
            elif operation_type == "SVD":
                data = safe_svd(A)
                res_arr = np.array([[v] for v in data["S"]])
                name = f"SVD-S({matrix_a.name})"
            elif operation_type == "QR":
                data = safe_qr(A)
                res_arr = np.array(data["Q"])
                name = f"QR-Q({matrix_a.name})"
            extra_data = data
        else:
            res_arr, name = ops_map[operation_type]()
            if isinstance(res_arr, list):
                res_arr = np.array(res_arr)

        execution_time_ms = int((time.time() - start_time) * 1000)

        result_matrix = Matrix.objects.create(
            name=name, rows=res_arr.shape[0], cols=res_arr.shape[1], data=res_arr.tolist()
        )

        operation = Operation.objects.create(
            operation_type=operation_type,
            matrix_a=matrix_a,
            matrix_b=matrix_b,
            result=result_matrix,
            execution_time_ms=execution_time_ms,
            extra_data=extra_data,
        )

        return operation
