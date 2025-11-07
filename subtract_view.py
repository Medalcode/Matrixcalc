"""subtract_view.py

Contiene la clase RestaScreen, responsable de la interfaz para restar dos matrices.
Utiliza MatrixEditor para la entrada y delega la lógica a `matrix_model`.
"""
import tkinter as tk
from tkinter import ttk

import matrix_model as mm
from matrix_editor import MatrixEditor
from result_viewer import MatrixResultViewer
from exceptions import MatrixModelError


class RestaScreen(ttk.Frame):
    """Pantalla para restar dos matrices usando MatrixEditor y matrix_model."""

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

        # Botón para aplicar dimensiones
        self.btn_apply_dim = ttk.Button(self, text="Aplicar dimensiones", command=self._apply_dimensions)
        self.btn_apply_dim.grid(row=2, column=0, columnspan=4, pady=5)

        # MatrixEditors
        ttk.Label(self, text="Matriz A:").grid(row=3, column=0, columnspan=2, sticky="w", padx=5)
        ttk.Label(self, text="Matriz B:").grid(row=3, column=2, columnspan=2, sticky="w", padx=5)

        self.editor_A = MatrixEditor(self, rows=default_rows, cols=default_cols)
        self.editor_A.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        self.editor_B = MatrixEditor(self, rows=default_rows, cols=default_cols)
        self.editor_B.grid(row=4, column=2, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Result viewer
        ttk.Label(self, text="Resultado:").grid(row=5, column=0, columnspan=4, sticky="w", padx=5)
        self.result_viewer = MatrixResultViewer(self)
        self.result_viewer.grid(row=6, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")

        # Error label
        self.error_label = ttk.Label(self, text="", foreground="red")
        self.error_label.grid(row=7, column=0, columnspan=4, pady=5)

        # Buttons
        self.btn_calcular = ttk.Button(self, text="Calcular Resta", command=self.calcular_resta)
        self.btn_calcular.grid(row=8, column=0, columnspan=2, pady=10)

        self.btn_reset = ttk.Button(self, text="Resetear Entradas", command=self.reset_entries)
        self.btn_reset.grid(row=8, column=2, columnspan=2, pady=10)

        # Layout stretch
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)
        self.grid_rowconfigure(6, weight=1)

    def _apply_dimensions(self):
        try:
            rows = int(self.entry_filas.get())
            cols = int(self.entry_columnas.get())
            if rows <= 0 or cols <= 0:
                raise ValueError()
        except Exception:
            self.error_label.config(text="Ingrese filas y columnas válidas (enteros positivos).")
            return

        self.error_label.config(text="")
        self.editor_A.set_dimensions(rows, cols)
        self.editor_B.set_dimensions(rows, cols)

    def calcular_resta(self):
        self.error_label.config(text="")

        try:
            rows = int(self.entry_filas.get())
            cols = int(self.entry_columnas.get())
            if rows <= 0 or cols <= 0:
                raise ValueError("Filas y columnas deben ser enteros positivos.")
        except ValueError as exc:
            self.error_label.config(text=str(exc) or "Dimensiones inválidas.")
            self.result_viewer.clear_viewer()
            return

        txtA = self.editor_A.get_matrix_text()
        txtB = self.editor_B.get_matrix_text()

        try:
            A = mm.parse_matrix(txtA, rows, cols)
            B = mm.parse_matrix(txtB, rows, cols)
            R = mm.safe_subtract(A, B)
        except MatrixModelError as exc:
            self.error_label.config(text=str(exc))
            self.result_viewer.clear_viewer()
            return
        except Exception as exc:
            # Unexpected errors should be logged; show generic message
            import logging

            logging.exception("Unexpected error in calcular_resta")
            self.error_label.config(text="Error inesperado. Revise logs.")
            self.result_viewer.clear_viewer()
            return

        try:
            self.result_viewer.show_matrix(R)
        except Exception as exc:
            self.error_label.config(text=f"Error mostrando resultado: {exc}")

    def reset_entries(self):
        self.entry_filas.delete(0, 'end')
        self.entry_columnas.delete(0, 'end')
        for editor in (self.editor_A, self.editor_B):
            for r in range(editor.rows):
                for c in range(editor.cols):
                    try:
                        editor.entries[r][c].delete(0, 'end')
                    except Exception:
                        pass

        self.result_viewer.clear_viewer()
        self.error_label.config(text="")


def crear_resta(parent):
    return RestaScreen(parent)
