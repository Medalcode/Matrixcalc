"""Compatibility shim: re-export `crear_home` from `home_view`.

Este archivo existe con el nombre legacy `modulo2_home.py` para no romper
imports externos; redirige a la implementación moderna en `home_view.py`.
"""

from home_view import crear_home

