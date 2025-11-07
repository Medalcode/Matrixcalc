"""Compatibility shim: re-export `crear_inversa` from `inverse_view`.

This preserves the legacy import path while delegating to the modern
implementation in `inverse_view.py`.
"""

from inverse_view import crear_inversa
