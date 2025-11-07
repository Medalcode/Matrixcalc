import tkinter as tk
from tkinter import ttk
import numpy as np
import matrix_model
from matrix_editor import MatrixEditor


class DeterminanteScreen(ttk.Frame):
    """Pantalla para calcular el determinante usando matrix_model.safe_det."""

    def __init__(self, parent, show_frame_callback=None):
        super().__init__(parent, style="TFrame")
        self.parent = parent
        self.show_frame = show_frame_callback

        label = ttk.Label(self, text="Operación: Determinante", font=("Bold", 15))
        label.grid(row=0, column=0, columnspan=3, pady=20)

        ttk.Label(self, text="Filas:").grid(row=1, column=0, pady=5, sticky="w")
        self.entry_filas = ttk.Entry(self, width=5)
        self.entry_filas.grid(row=2, column=0, pady=5, padx=5)

        ttk.Label(self, text="Columnas:").grid(row=1, column=1, pady=5, sticky="w")
        self.entry_columnas = ttk.Entry(self, width=5)
        self.entry_columnas.grid(row=2, column=1, pady=5, padx=5)

        ttk.Label(self, text="Matriz A:").grid(row=3, column=0, pady=5, sticky="w")
        self.editor_A = MatrixEditor(self, rows=3, cols=3)
        self.editor_A.grid(row=4, column=0, columnspan=3, pady=5, padx=5, sticky="nsew")

        self.error_label = ttk.Label(self, text="", foreground="red")
        self.error_label.grid(row=5, column=0, columnspan=3, pady=10, sticky="ew")

        # Bind para actualizar dimensiones
        self.entry_filas.bind("<FocusOut>", lambda e: self._on_dim_change())
        self.entry_columnas.bind("<FocusOut>", lambda e: self._on_dim_change())

        self.boton_calcular = ttk.Button(self, text="Calcular Determinante", command=self.calcular_determinante)
        self.boton_calcular.grid(row=6, column=0, pady=10)

        self.boton_reset = ttk.Button(self, text="Resetear Entradas", command=self.reset_entries)
        self.boton_reset.grid(row=6, column=1, pady=10)

    def _on_dim_change(self):
        try:
            r = int(self.entry_filas.get())
            c = int(self.entry_columnas.get())
        except Exception:
            return
        if r > 0 and c > 0:
            self.editor_A.set_dimensions(r, c)

    def reset_entries(self):
        self.entry_filas.delete(0, tk.END)
        self.entry_columnas.delete(0, tk.END)
        for r in range(self.editor_A.rows):
            for c in range(self.editor_A.cols):
                self.editor_A.entries[r][c].delete(0, tk.END)
        self.error_label.config(text="")

    def calcular_determinante(self):
        self.error_label.config(text="")
        try:
            filas = int(self.entry_filas.get())
            columnas = int(self.entry_columnas.get())

            text_a = self.editor_A.get_matrix_text()
            A = matrix_model.parse_matrix(text_a, filas, columnas)

            det = matrix_model.safe_det(A)

            # Mostrar resultado en nueva ventana
            ventana_resultado = tk.Toplevel(self.parent)
            ventana_resultado.title("Determinante")
            frame = ttk.Frame(ventana_resultado)
            frame.pack(padx=10, pady=10)
            ttk.Label(frame, text=f"Determinante: {det}", font=("Bold", 12)).pack()
            invertible = not np.isclose(det, 0.0)
            ttk.Label(frame, text=("Invertible" if invertible else "No invertible"), foreground=("green" if invertible else "red")).pack()

        except ValueError as e:
            self.error_label.config(text=str(e))


def crear_determinante(parent):
    return DeterminanteScreen(parent)
