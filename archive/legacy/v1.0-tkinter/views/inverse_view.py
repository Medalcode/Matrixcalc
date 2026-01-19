"""inverse_view.py

Contiene la clase InversaScreen para calcular la inversa de una matriz.
"""
import tkinter as tk
from tkinter import ttk
import matrix_model
from matrix_editor import MatrixEditor
from result_viewer import MatrixResultViewer
from exceptions import MatrixModelError


class InversaScreen(ttk.Frame):
    """Pantalla para calcular la inversa de una matriz usando matrix_model.safe_inv."""

    def __init__(self, parent, show_frame_callback=None):
        super().__init__(parent, style="TFrame")
        self.parent = parent
        self.show_frame = show_frame_callback

        label = ttk.Label(self, text="Operación: Inversa", font=("Bold", 15))
        label.grid(row=0, column=0, columnspan=3, pady=20)

        # Dimensiones
        ttk.Label(self, text="Filas:").grid(row=1, column=0, pady=5, sticky="w")
        self.entry_filas = ttk.Entry(self, width=5)
        self.entry_filas.grid(row=2, column=0, pady=5, padx=5)

        ttk.Label(self, text="Columnas:").grid(row=1, column=1, pady=5, sticky="w")
        self.entry_columnas = ttk.Entry(self, width=5)
        self.entry_columnas.grid(row=2, column=1, pady=5, padx=5)

        # MatrixEditor (una sola matriz)
        ttk.Label(self, text="Matriz A:").grid(row=3, column=0, pady=5, sticky="w")
        self.editor_A = MatrixEditor(self, rows=3, cols=3)
        self.editor_A.grid(row=4, column=0, columnspan=3, pady=5, padx=5, sticky="nsew")

        # Error label centralizado
        self.error_label = ttk.Label(self, text="", foreground="red")
        self.error_label.grid(row=5, column=0, columnspan=3, pady=10, sticky="ew")

        # Bind para actualizar dimensiones
        self.entry_filas.bind("<FocusOut>", lambda e: self._on_dim_change())
        self.entry_columnas.bind("<FocusOut>", lambda e: self._on_dim_change())

        # Botones
        self.boton_calcular = ttk.Button(self, text="Calcular Inversa", command=self.calcular_inversa)
        self.boton_calcular.grid(row=6, column=0, columnspan=1, pady=15)

        self.boton_reset = ttk.Button(self, text="Resetear Entradas", command=self.reset_entries)
        self.boton_reset.grid(row=6, column=1, columnspan=2, pady=15)

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
        # limpiar editor
        for r in range(self.editor_A.rows):
            for c in range(self.editor_A.cols):
                self.editor_A.entries[r][c].delete(0, tk.END)
        self.error_label.config(text="")

    def calcular_inversa(self):
        self.error_label.config(text="")
        try:
            filas = int(self.entry_filas.get())
            columnas = int(self.entry_columnas.get())

            text_a = self.editor_A.get_matrix_text()
            A = matrix_model.parse_matrix(text_a, filas, columnas)

            # Delegar la validación y el cálculo al modelo
            R = matrix_model.safe_inv(A)

            self._mostrar_resultado(R)

        except MatrixModelError as e:
            self.error_label.config(text=str(e))
        except Exception:
            import logging

            logging.exception("Unexpected error in calcular_inversa")
            self.error_label.config(text="Error inesperado. Revise logs.")

    def _mostrar_resultado(self, resultado):
        ventana_resultado = tk.Toplevel(self.parent)
        ventana_resultado.title("Resultado de la Inversa")

        frame_resultado = ttk.Frame(ventana_resultado)
        frame_resultado.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        viewer = MatrixResultViewer(frame_resultado)
        viewer.pack(fill=tk.BOTH, expand=True)
        viewer.show_matrix(resultado)


def crear_inversa(parent):
    return InversaScreen(parent)
