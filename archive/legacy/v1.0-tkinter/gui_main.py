"""gui_main.py

Contiene la clase MatrixCalcApp que crea la ventana principal, el menú y
gestiona la navegación entre las distintas vistas (pantallas) de la app.
La aplicación crea cada pantalla mediante factories (crear_*) y las
mantiene en un contenedor para mostrarlas con show_frame(page_name).
"""
import tkinter as tk
from tkinter import ttk

# Imports for the screens (factories return Frame instances)
from home_view import crear_home
from sum_view import crear_suma
from subtract_view import crear_resta
from inverse_view import crear_inversa
from multiply_view import crear_multiplica
from transpose_view import crear_traspuesta
from determinant_view import crear_determinante


class MatrixCalcApp(tk.Tk):
    """Aplicación principal que maneja la navegación entre pantallas.

    Usa las funciones `crear_*` existentes para instanciar las pantallas dentro
    de un contenedor y expone `show_frame(page_name)` para la navegación.
    """

    def __init__(self):
        super().__init__()

        self.title("Matrixcal")
        self.geometry("700x550")
        self.resizable(False, False)

        # Menu y estilo
        self.style = ttk.Style()

        # Left panel: opciones
        self.frame_opciones = ttk.Frame(self, style="TFrame", width=150)
        self.frame_opciones.pack(side=tk.LEFT, fill=tk.Y)
        self.frame_opciones.pack_propagate(False)

        # Container where screens will be stacked
        self.container = ttk.Frame(self)
        self.container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Menú superior
        self._create_menu()

        # Map of page name -> factory function
        self.pages = {
            "Home": crear_home,
            "Suma": crear_suma,
            "Resta": crear_resta,
            "Inversa": crear_inversa,
            "Multiplica": crear_multiplica,
            "Traspuesta": crear_traspuesta,
            "Determinante": crear_determinante,
        }

        # Create frames and store in self.frames
        self.frames = {}
        for name, factory in self.pages.items():
            # factory returns a Frame instance; pass the container as parent
            frame = factory(self.container)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[name] = frame

        # Build navigation buttons
        self._create_navigation()

        # Show home by default
        self.show_frame("Home")

    def _create_menu(self):
        barra_menu = tk.Menu(self)
        self.config(menu=barra_menu)

        menu_ayuda = tk.Menu(barra_menu, tearoff=0)
        menu_info = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)
        barra_menu.add_cascade(label="Acerca de", menu=menu_info)

        # Tema submenu
        menu_tema = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="Tema", menu=menu_tema)
        for tema in self.style.theme_names():
            menu_tema.add_command(label=tema, command=lambda t=tema: self.cambiar_tema(t))

        menu_info.add_command(label="About", command=self.mostrar_ventana_about)
        menu_ayuda.add_command(label="Instrucciones", command=self.mostrar_ventana_ayuda)

    def _create_navigation(self):
        btn_specs = [
            ("HOME", "Home"),
            ("SUMA", "Suma"),
            ("RESTA", "Resta"),
            ("INVERSA", "Inversa"),
            ("MULTIPLICA", "Multiplica"),
            ("TRASPUESTA", "Traspuesta"),
            ("DETERMINANTE", "Determinante"),
        ]

        for text, page in btn_specs:
            btn = ttk.Button(self.frame_opciones, text=text, command=lambda p=page: self.show_frame(p))
            btn.pack(pady=10, fill=tk.X, padx=5)

    def cambiar_tema(self, tema: str):
        self.style.theme_use(tema)

    def show_frame(self, page_name: str):
        """Muestra la pantalla indicada por name (raise)."""
        frame = self.frames.get(page_name)
        if frame is None:
            raise KeyError(f"Página desconocida: {page_name}")
        frame.tkraise()

    def mostrar_ventana_about(self):
        ventana_about = tk.Toplevel(self)
        ventana_about.title("About")
        ventana_about.geometry("500x500")
        frame_about = ttk.Frame(ventana_about)
        frame_about.pack(expand=True)
        label_about = ttk.Label(frame_about, text=(
            "Nombre de la Aplicación: Matrixcal\n\nVersión: 1.0\n\nDesarrolladores:\n\n- Lancelot Castro Bobadilla\n\n- Hernan Espinoza Castillo\n\n- Jonathan Medalla Aliste\n\nColaboradores:\n\n- Carolina Gomez Bravo\n\n- Alejandro Cuevas Rivero\n\n- Ernesto Vivanco Tapia\n\n\nFecha de Lanzamiento: 31/01/2024\n\n© 2024 Matrixcal. Todos los derechos reservados."))
        label_about.pack(pady=20)

    def mostrar_ventana_ayuda(self):
        ventana_ayuda = tk.Toplevel(self)
        ventana_ayuda.title("Ayuda")
        ventana_ayuda.attributes("-topmost", True)
        frame_ayuda = ttk.Frame(ventana_ayuda)
        frame_ayuda.pack(padx=20, pady=20)
        label_ayuda = ttk.Label(frame_ayuda, text=(
            "Instrucciones de Uso - Matrixcal:\n\n"
            "1. Selección de Operación: Utiliza los botones de la barra de opciones para seleccionar la operación matricial deseada (SUMA, RESTA, INVERSA, MULTIPLICA, TRASPUESTA).\n\n"
            "2. Ingreso de Valores: Ingresa los valores de las matrices en las secciones correspondientes (MatrixEditor).\n\n"
            "3. Reglas para los Valores: Ingresa solo valores numéricos.\n\n"
            "4. Realización de la Operación: Después de ingresar los valores, haz clic en el botón correspondiente para realizar la operación seleccionada.\n\n"
            "5. Resultado de la Operación: El resultado se mostrará en el panel de resultados de la pantalla."))
        label_ayuda.pack(pady=10)


if __name__ == "__main__":
    app = MatrixCalcApp()
    app.mainloop()
