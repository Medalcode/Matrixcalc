"""multiply_view.py

Contiene la clase MultiplicaScreen para la multiplicación matricial.
"""
import tkinter as tk
from tkinter import ttk
import matrix_model
from matrix_editor import MatrixEditor


class MultiplicaScreen(ttk.Frame):
    """Pantalla de multiplicación matricial que usa MatrixEditor y matrix_model."""

    def __init__(self, parent, show_frame_callback=None):
        super().__init__(parent, style="TFrame")
        self.parent = parent
        self.show_frame = show_frame_callback

        label = ttk.Label(self, text="Operación: Multiplicación", font=("Bold", 15))
        label.grid(row=0, column=0, columnspan=4, pady=20)

        # Dimensiones para A
        ttk.Label(self, text="Filas A:").grid(row=1, column=0, pady=5, sticky="w")
        self.entry_filas_A = ttk.Entry(self, width=5)
        self.entry_filas_A.grid(row=2, column=0, pady=5, padx=5)

        ttk.Label(self, text="Columnas A:").grid(row=1, column=1, pady=5, sticky="w")
        self.entry_columnas_A = ttk.Entry(self, width=5)
        self.entry_columnas_A.grid(row=2, column=1, pady=5, padx=5)

        # Dimensiones para B
        ttk.Label(self, text="Filas B:").grid(row=1, column=2, pady=5, sticky="w")
        self.entry_filas_B = ttk.Entry(self, width=5)
        self.entry_filas_B.grid(row=2, column=2, pady=5, padx=5)

        ttk.Label(self, text="Columnas B:").grid(row=1, column=3, pady=5, sticky="w")
        self.entry_columnas_B = ttk.Entry(self, width=5)
        self.entry_columnas_B.grid(row=2, column=3, pady=5, padx=5)

        # MatrixEditor para A y B
        ttk.Label(self, text="Matriz A:").grid(row=3, column=0, pady=5, sticky="w")
        self.editor_A = MatrixEditor(self, rows=3, cols=3)
        self.editor_A.grid(row=4, column=0, columnspan=2, pady=5, padx=5, sticky="nsew")

        ttk.Label(self, text="Matriz B:").grid(row=3, column=2, pady=5, sticky="w")
        self.editor_B = MatrixEditor(self, rows=3, cols=3)
        self.editor_B.grid(row=4, column=2, columnspan=2, pady=5, padx=5, sticky="nsew")

        # Error label centralizado
        self.error_label = ttk.Label(self, text="", foreground="red")
        self.error_label.grid(row=5, column=0, columnspan=4, pady=10, sticky="ew")

        # Bind para actualizar dimensiones cuando cambian
        self.entry_filas_A.bind("<FocusOut>", lambda e: self._on_dim_change_A())
        self.entry_columnas_A.bind("<FocusOut>", lambda e: self._on_dim_change_A())
        self.entry_filas_B.bind("<FocusOut>", lambda e: self._on_dim_change_B())
        self.entry_columnas_B.bind("<FocusOut>", lambda e: self._on_dim_change_B())

        # Botones
        self.boton_calcular = ttk.Button(self, text="Calcular Multiplicación", command=self.calcular_multiplicacion)
        self.boton_calcular.grid(row=6, column=0, columnspan=2, pady=15)

        self.boton_reset = ttk.Button(self, text="Resetear Entradas", command=self.reset_entries)
        self.boton_reset.grid(row=6, column=2, columnspan=2, pady=15)

    def _on_dim_change_A(self):
        try:
            r = int(self.entry_filas_A.get())
            c = int(self.entry_columnas_A.get())
        except Exception:
            return
        if r > 0 and c > 0:
            self.editor_A.set_dimensions(r, c)

    def _on_dim_change_B(self):
        try:
            r = int(self.entry_filas_B.get())
            c = int(self.entry_columnas_B.get())
        except Exception:
            return
        if r > 0 and c > 0:
            self.editor_B.set_dimensions(r, c)

    def reset_entries(self):
        # Limpiar dimensiones
        self.entry_filas_A.delete(0, tk.END)
        self.entry_columnas_A.delete(0, tk.END)
        self.entry_filas_B.delete(0, tk.END)
        self.entry_columnas_B.delete(0, tk.END)

        # Limpiar celdas de los editores
        for r in range(self.editor_A.rows):
            for c in range(self.editor_A.cols):
                self.editor_A.entries[r][c].delete(0, tk.END)
        for r in range(self.editor_B.rows):
            for c in range(self.editor_B.cols):
                self.editor_B.entries[r][c].delete(0, tk.END)

        self.error_label.config(text="")

    def calcular_multiplicacion(self):
        self.error_label.config(text="")
        try:
            # Leer dimensiones
            rA = int(self.entry_filas_A.get())
            cA = int(self.entry_columnas_A.get())
            rB = int(self.entry_filas_B.get())
            cB = int(self.entry_columnas_B.get())

            # Obtener CSV desde los editores
            text_a = self.editor_A.get_matrix_text()
            text_b = self.editor_B.get_matrix_text()

            # Delegar parseo al modelo
            A = matrix_model.parse_matrix(text_a, rA, cA)
            B = matrix_model.parse_matrix(text_b, rB, cB)

            # Delegar multiplicación al modelo
            R = matrix_model.safe_dot(A, B)

            # Mostrar resultado
            self._mostrar_resultado(R)

        except ValueError as e:
            self.error_label.config(text=str(e))

    def _mostrar_resultado(self, resultado):
        ventana_resultado = tk.Toplevel(self.parent)
        ventana_resultado.title("Resultado de la Multiplicación")

        frame_resultado = ttk.Frame(ventana_resultado)
        frame_resultado.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        label_resultado = ttk.Label(frame_resultado, text="Resultado de la Multiplicación", font=("Bold", 15))
        label_resultado.grid(row=0, column=0, columnspan=resultado.shape[1], pady=10)

        treeview = ttk.Treeview(frame_resultado)
        cols = [f"C{i+1}" for i in range(resultado.shape[1])]
        treeview["columns"] = cols
        treeview.heading("#0", text="Fila")
        for c in cols:
            treeview.heading(c, text=c)

        for i, fila in enumerate(resultado.tolist()):
            treeview.insert("", "end", text=f"Fila {i+1}", values=tuple(fila))

        treeview.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)


def crear_multiplica(parent):
    return MultiplicaScreen(parent)
