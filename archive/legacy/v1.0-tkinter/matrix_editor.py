import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from typing import Optional


class MatrixEditor(ttk.Frame):
    """Widget reutilizable para editar matrices en una cuadrícula con scroll.

    - Cambié las celdas a `tk.Entry` para permitir marcado visual en validación.
    - Añadí validación por celda en `<FocusOut>` (marca celdas no numéricas).
    - Incluye un botón "Import CSV" que abre un diálogo para pegar CSV y cargar la matriz.

    Métodos clave:
    - set_dimensions(rows, cols)
    - get_matrix_text() -> CSV fila-major
    - import_from_csv_text(text)
    """

    def __init__(self, parent, rows: int = 3, cols: int = 3, cell_width: int = 8, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.rows = int(rows)
        self.cols = int(cols)
        self.cell_width = cell_width

        # Toolbar: Import CSV
        toolbar = ttk.Frame(self)
        toolbar.grid(row=0, column=0, sticky="ew", padx=2, pady=(0, 4))
        btn_import = ttk.Button(toolbar, text="Import CSV", command=self._open_import_dialog)
        btn_import.pack(side=tk.LEFT)

        # Canvas con scrollbars
        self.canvas = tk.Canvas(self)
        self.v_scroll = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.h_scroll = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)

        self.v_scroll.grid(row=1, column=1, sticky="ns")
        self.h_scroll.grid(row=2, column=0, sticky="ew")
        self.canvas.grid(row=1, column=0, sticky="nsew")

        # Make the canvas expandable
        self.grid_rowconfigure(1, weight=1)
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

        # Crear nueva cuadrícula (usamos tk.Entry para permitir cambios visuales)
        for r in range(rows):
            row_entries = []
            for c in range(cols):
                e = tk.Entry(self.interior_frame, width=self.cell_width)
                e.grid(row=r, column=c, padx=2, pady=2)
                # Bind validación al perder foco
                e.bind("<FocusOut>", lambda ev, ent=e: self._validate_cell(ent))
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

    def _validate_cell(self, entry: tk.Entry) -> bool:
        """Validate the content of a single cell; mark background if invalid.

        Returns True when valid or empty, False otherwise.
        """
        val = entry.get().strip()
        if val == "":
            # empty is allowed; clear visual mark
            try:
                entry.configure(bg="white")
            except Exception:
                pass
            return True
        try:
            float(val)
            try:
                entry.configure(bg="white")
            except Exception:
                pass
            return True
        except Exception:
            # Mark invalid visually
            try:
                entry.configure(bg="#ffd6d6")
            except Exception:
                pass
            return False

    def _open_import_dialog(self, parent: Optional[tk.Widget] = None):
        """Open a simple dialog to paste CSV text and import it into the editor."""
        dlg = tk.Toplevel(self)
        dlg.title("Import CSV")
        dlg.geometry("400x300")
        lbl = ttk.Label(dlg, text="Pegue CSV (filas en nuevas líneas, columnas separadas por comas):")
        lbl.pack(anchor="w", padx=8, pady=4)
        text = scrolledtext.ScrolledText(dlg)
        text.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

        def _do_import():
            csv_text = text.get("1.0", tk.END).strip()
            try:
                self.import_from_csv_text(csv_text)
            except Exception as exc:
                # Simple feedback
                tk.messagebox.showerror("Import error", str(exc))
            finally:
                dlg.destroy()

        btn = ttk.Button(dlg, text="Importar", command=_do_import)
        btn.pack(pady=6)

    def import_from_csv_text(self, csv_text: str):
        """Import matrix from CSV text with newlines as rows.

        Example:
            "1,2,3\n4,5,6"
        """
        if not csv_text:
            raise ValueError("Texto de importación vacío")
        rows = [line.strip() for line in csv_text.splitlines() if line.strip()]
        data = [ [tok.strip() for tok in row.split(',')] for row in rows]
        r = len(data)
        c = len(data[0]) if r>0 else 0
        # Verify all rows have same columns
        for row in data:
            if len(row) != c:
                raise ValueError("Todas las filas deben tener el mismo número de columnas")

        # Resize grid and fill
        self.set_dimensions(r, c)
        for i in range(r):
            for j in range(c):
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].insert(0, data[i][j])
                self._validate_cell(self.entries[i][j])
