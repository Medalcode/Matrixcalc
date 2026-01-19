import tkinter as tk
from tkinter import ttk
import numpy as np


class MatrixResultViewer(ttk.Frame):
    """Widget para mostrar `np.ndarray` en formato tabular usando ttk.Treeview.

    Uso:
        viewer = MatrixResultViewer(parent)
        viewer.show_matrix(np.array([[1,2],[3,4]]))
    """

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.tree = ttk.Treeview(self)
        self.vsb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.hsb = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        self.vsb.grid(row=0, column=1, sticky="ns")
        self.hsb.grid(row=1, column=0, sticky="ew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def clear_viewer(self):
        # Borrar elementos y columnas
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Reset columns
        self.tree["columns"] = ()
        try:
            # hide headings
            self.tree.heading("#0", text="")
        except Exception:
            pass

    def show_matrix(self, matrix: np.ndarray):
        """Muestra la matriz NumPy en el Treeview, formateando números a 4 decimales."""
        self.clear_viewer()

        if not isinstance(matrix, np.ndarray):
            matrix = np.asarray(matrix)

        if matrix.ndim != 2:
            raise ValueError("El resultado debe ser una matriz 2D.")

        rows, cols = matrix.shape

        # Configurar columnas
        col_ids = [f"C{i}" for i in range(cols)]
        self.tree["columns"] = col_ids
        # Use #0 as row label
        self.tree.heading("#0", text="Fila")
        for i, cid in enumerate(col_ids):
            self.tree.heading(cid, text=f"C{i+1}")
            self.tree.column(cid, anchor="center")

        # Insert rows
        for r in range(rows):
            row_vals = []
            for c in range(cols):
                val = matrix[r, c]
                # Formatear con 4 decimales si es float, mantener int si es entero
                if isinstance(val, (float, np.floating)):
                    s = f"{val:.4f}" if np.isfinite(val) else str(val)
                else:
                    s = str(val)
                row_vals.append(s)
            self.tree.insert("", "end", text=f"Fila {r+1}", values=tuple(row_vals))
