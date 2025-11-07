import tkinter as tk
from tkinter import ttk


class MatrixEditor(ttk.Frame):
    """Widget reutilizable para editar matrices en una cuadrícula con scroll.

    Provee set_dimensions(rows, cols) para redibujar la cuadrícula y
    get_matrix_text() que devuelve una cadena CSV con los valores de las celdas.
    """

    def __init__(self, parent, rows: int = 3, cols: int = 3, cell_width: int = 8, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.rows = int(rows)
        self.cols = int(cols)
        self.cell_width = cell_width

        # Canvas con scrollbars
        self.canvas = tk.Canvas(self)
        self.v_scroll = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.h_scroll = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)

        self.v_scroll.grid(row=0, column=1, sticky="ns")
        self.h_scroll.grid(row=1, column=0, sticky="ew")
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Make the canvas expandable
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Interior frame dentro del canvas
        self.interior_frame = ttk.Frame(self.canvas)
        self.interior_id = self.canvas.create_window((0, 0), window=self.interior_frame, anchor="nw")

        # Bind para actualizar el scroll region
        self.interior_frame.bind("<Configure>", self._on_interior_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        # Entradas (lista anidada)
        self.entries = []

        # Crear la cuadrícula inicial
        self._create_grid(self.rows, self.cols)

    def _on_interior_configure(self, event=None):
        # Actualiza scrollregion cuando cambia el tamaño del interior
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event=None):
        # Asegura que la ventana interior tenga al menos el ancho del canvas
        canvas_width = event.width if event else self.canvas.winfo_width()
        self.canvas.itemconfig(self.interior_id, width=canvas_width)

    def _create_grid(self, rows: int, cols: int):
        # Destruir widgets previos
        for child in self.interior_frame.winfo_children():
            child.destroy()
        self.entries = []

        # Crear nueva cuadrícula
        for r in range(rows):
            row_entries = []
            for c in range(cols):
                e = ttk.Entry(self.interior_frame, width=self.cell_width)
                e.grid(row=r, column=c, padx=2, pady=2)
                row_entries.append(e)
            self.entries.append(row_entries)

        # Guardar dimensiones
        self.rows = rows
        self.cols = cols

        # Forzar actualización del scrollregion
        self.interior_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def set_dimensions(self, rows: int, cols: int):
        """Redibuja la cuadrícula a las nuevas dimensiones."""
        try:
            rows_i = int(rows)
            cols_i = int(cols)
        except (ValueError, TypeError):
            return

        if rows_i <= 0 or cols_i <= 0:
            return

        if rows_i == self.rows and cols_i == self.cols:
            return

        self._create_grid(rows_i, cols_i)

    def get_matrix_text(self) -> str:
        """Devuelve los valores de la cuadrícula como una cadena CSV (fila-major)."""
        tokens = []
        for r in range(self.rows):
            for c in range(self.cols):
                val = self.entries[r][c].get().strip()
                # Permitir celdas vacías como '' — el modelo decidirá si eso es aceptable
                tokens.append(val)
        return ",".join(tokens)
