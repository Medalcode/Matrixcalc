import tkinter as tk
from tkinter import ttk
import matrix_model


class SumaScreen(ttk.Frame):
    """Pantalla de suma matricial.

    Esta clase es responsable únicamente de la interfaz y delega toda la
    lógica de parseo/validación y cálculo al módulo `matrix_model`.
    """

    def __init__(self, parent, show_frame_callback=None):
        super().__init__(parent, style="TFrame")
        self.parent = parent
        self.show_frame = show_frame_callback

        # Widgets: dimensiones y matrices en formato CSV (entrada simple)
        label_suma = ttk.Label(self, text="Operación: Suma", font=("Bold", 15))
        label_suma.grid(row=0, column=0, columnspan=4, pady=20)

        ttk.Label(self, text="n°Filas:").grid(row=1, column=0, pady=5, sticky="w")
        self.entry_filas = ttk.Entry(self, width=5)
        self.entry_filas.grid(row=2, column=0, pady=5, padx=5)

        ttk.Label(self, text="n°Columnas:").grid(row=1, column=1, pady=5, sticky="w")
        self.entry_columnas = ttk.Entry(self, width=5)
        self.entry_columnas.grid(row=2, column=1, pady=5, padx=5)

        ttk.Label(self, text="Matriz A (CSV):").grid(row=3, column=0, pady=5, sticky="w")
        self.entry_matriz_a = ttk.Entry(self, width=40)
        self.entry_matriz_a.grid(row=4, column=0, columnspan=2, pady=5, padx=5)

        ttk.Label(self, text="Matriz B (CSV):").grid(row=3, column=2, pady=5, sticky="w")
        self.entry_matriz_b = ttk.Entry(self, width=40)
        self.entry_matriz_b.grid(row=4, column=2, columnspan=2, pady=5, padx=5)

        # Error label único y centralizado
        self.error_label = ttk.Label(self, text="", foreground="red")
        self.error_label.grid(row=5, column=0, columnspan=4, pady=10, sticky="ew")

        # Botones
        self.boton_calcular = ttk.Button(self, text="Calcular Suma", command=self.calcular_suma)
        self.boton_calcular.grid(row=6, column=0, columnspan=2, pady=15)

        self.boton_reset = ttk.Button(self, text="Resetear Entradas", command=self.reset_entries)
        self.boton_reset.grid(row=6, column=2, columnspan=2, pady=15)

    def reset_entries(self):
        self.entry_filas.delete(0, tk.END)
        self.entry_columnas.delete(0, tk.END)
        self.entry_matriz_a.delete(0, tk.END)
        self.entry_matriz_b.delete(0, tk.END)
        self.error_label.config(text="")

    def calcular_suma(self):
        """Controlador que parsea entradas, delega en matrix_model y muestra resultado."""
        # Limpiar errores previos
        self.error_label.config(text="")

        try:
            # 1) Obtener dimensiones
            filas = int(self.entry_filas.get())
            columnas = int(self.entry_columnas.get())

            # 2) Parsear matrices vía el modelo
            text_a = self.entry_matriz_a.get()
            text_b = self.entry_matriz_b.get()

            A = matrix_model.parse_matrix(text_a, filas, columnas)
            B = matrix_model.parse_matrix(text_b, filas, columnas)

            # 3) Calcular suma con el modelo
            R = matrix_model.safe_add(A, B)

            # 4) Mostrar resultado en una ventana tipo Treeview
            self._mostrar_resultado(R)

        except ValueError as e:
            # Mensajes claros procedentes del modelo
            self.error_label.config(text=str(e))

    def _mostrar_resultado(self, resultado):
        ventana_resultado = tk.Toplevel(self.parent)
        ventana_resultado.title("Resultado de la Suma")

        frame_resultado = ttk.Frame(ventana_resultado)
        frame_resultado.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        label_resultado = ttk.Label(frame_resultado, text="Resultado de la Suma", font=("Bold", 15))
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


def crear_suma(parent):
    """Factory para mantener compatibilidad con la main (que espera una función)."""
    return SumaScreen(parent)

