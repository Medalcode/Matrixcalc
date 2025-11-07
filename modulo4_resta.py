import tkinter as tk
from tkinter import ttk

import matrix_model as mm
from matrix_editor import MatrixEditor
from result_viewer import MatrixResultViewer


class RestaScreen(ttk.Frame):
    """Pantalla para restar dos matrices usando MatrixEditor y matrix_model.

    Provee entradas para filas/columnas, dos MatrixEditor (A y B), y un
    MatrixResultViewer para mostrar el resultado.
    """

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Dimensiones por defecto
        default_rows = 2
        default_cols = 2

        # Encabezado
        label_resta = ttk.Label(self, text="Operación: Resta", font=("Bold", 15))
        label_resta.grid(row=0, column=0, columnspan=4, pady=10)

        # Dimensiones
        ttk.Label(self, text="n°Filas:").grid(row=1, column=0, sticky="w", padx=5)
        self.entry_filas = ttk.Entry(self, width=5)
        self.entry_filas.grid(row=1, column=1, sticky="w", padx=5)
        self.entry_filas.insert(0, str(default_rows))

        ttk.Label(self, text="n°Columnas:").grid(row=1, column=2, sticky="w", padx=5)
        self.entry_columnas = ttk.Entry(self, width=5)
        self.entry_columnas.grid(row=1, column=3, sticky="w", padx=5)
        self.entry_columnas.insert(0, str(default_cols))
"""Compatibility shim: re-export `crear_resta` from `subtract_view`.

This file preserves the legacy import path while delegating to
`subtract_view.py` for the implementation.
"""

from subtract_view import crear_resta


