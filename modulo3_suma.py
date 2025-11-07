"""Compatibility shim: re-export `crear_suma` from `sum_view`.

This maintains the historical import path `modulo3_suma` while delegating
to the modern implementation in `sum_view.py`.
"""

from sum_view import crear_suma


