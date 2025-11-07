"""Compatibility shim: re-export `crear_multiplica` from `multiply_view`.

This preserves the historical import path while delegating to `multiply_view.py`.
"""

from multiply_view import crear_multiplica
