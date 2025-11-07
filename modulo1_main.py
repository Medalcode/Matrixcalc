import tkinter as tk
from tkinter import ttk

# Tus imports
from modulo2_home import crear_home
from modulo3_suma import crear_suma
from modulo4_resta import crear_resta
from modulo5_inversa import crear_inversa
from modulo6_multiplica import crear_multiplica
from modulo7_traspuesta import crear_traspuesta
from modulo8_determina import crear_determinante
from result_viewer import MatrixResultViewer

def cambiar_tema(tema):
    style = ttk.Style()
    style.theme_use(tema)

def abrir_frame(crear_frame):
    global frame_actual
    if frame_actual:
        frame_actual.pack_forget()

    frame_actual = crear_frame(ventana)
    frame_actual.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

def mostrar_resultado(resultado):
    """Función de compatibilidad que muestra una matriz usando MatrixResultViewer.

    Recomendación: las pantallas deben usar su propio viewer (MatrixResultViewer)
    para presentar resultados; esta función es un stub que utiliza el mismo
    componente para presentaciones rápidas desde el main si fuera necesario.
    """
    ventana_resultado = tk.Toplevel(ventana)
    ventana_resultado.title("Resultado de la Operación")

    frame_resultado = ttk.Frame(ventana_resultado, style="TFrame", width=550, height=550)
    frame_resultado.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    viewer = MatrixResultViewer(frame_resultado)
    viewer.pack(fill=tk.BOTH, expand=True)
    try:
        viewer.show_matrix(resultado)
    except Exception as e:
        # Si no es una matriz 2D, mostrar fallback simple
        lbl = ttk.Label(frame_resultado, text=str(resultado))
        lbl.pack()

def mostrar_ventana_ayuda():
    global ventana_ayuda
    if ventana_ayuda is None:
        ventana_ayuda = tk.Toplevel(ventana)
        ventana_ayuda.title("Ayuda")
        ventana_ayuda.protocol("WM_DELETE_WINDOW", ocultar_ventana_ayuda)
        ventana_ayuda.attributes("-topmost", True)
        ventana_ayuda.geometry("+{}+{}".format(ventana.winfo_rootx() + ventana.winfo_width() // 2 - ventana_ayuda.winfo_width() // 2,
                                               ventana.winfo_rooty() + ventana.winfo_height() // 2 - ventana_ayuda.winfo_height() // 2))
        frame_ayuda = ttk.Frame(ventana_ayuda)
        frame_ayuda.pack(padx=20, pady=20)
        label_ayuda = ttk.Label(frame_ayuda, text="Instrucciones de Uso - Matrixcal:\n\n"
        "1. Selección de Operación: - Utiliza los botones de la barra de opciones para seleccionar la \noperación matricial deseada (SUMA, RESTA, INVERSA, MULTIPLICA, TRASPUESTA).\n\n"
        "2. Ingreso de Valores: - Ingresa los valores de las matrices en las secciones correspondientes. \nLos valores deben estar separados por comas.Ejemplo: Para una matriz 2x2, ingresa los valores como 1, 2, 3, 4.\n\n"
        "3. Reglas para los Valores: - Ingresa solo valores numéricos.\n- Utiliza comas para separar los valores.\n-Asegúrate de respetar las reglas aritméticas al ingresar los datos.\n\n"
        "4. Realización de la Operación:- Después de ingresar los valores, haz clic en el botón \ncorrespondiente para realizar la operación seleccionada.\n\n"
        "5. Resultado de la Operación: - El resultado se mostrará en una nueva ventana.\n-Examina cuidadosamente el resultado y verifica que cumple con las expectativas.\n\n")
        label_ayuda.pack(pady=10)
    ventana_ayuda.deiconify()
    ventana_ayuda.lift()

def ocultar_ventana_ayuda():
    global ventana_ayuda
    if ventana_ayuda is not None:
        ventana_ayuda.withdraw()
        ventana_ayuda = None

def abrir_home():
    global frame_actual
    if frame_actual:
        frame_actual.pack_forget()

    frame_actual = crear_home(ventana)
    frame_actual.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

def boton_guardar():
    pass

def guardar_resultado(resultado):
    pass

frame_actual = None

ventana = tk.Tk()
ventana.geometry("700x550")
ventana.title("Matrixcal")
ventana.resizable(0, 0)
ventana_ayuda = None

frame_ayuda = ttk.Frame(ventana)
frame_ayuda.pack(padx=20, pady=20)

frame_opciones = ttk.Frame(ventana, style="TFrame", width=550, height=550)
frame_opciones.pack(side=tk.LEFT)
frame_opciones.pack_propagate(False)
frame_opciones.config(width="150", height="550")

barra_menu = tk.Menu(ventana)
ventana.config(menu=barra_menu)

menu_archivo = tk.Menu(barra_menu, tearoff=0)
menu_ayuda = tk.Menu(barra_menu, tearoff=0)
menu_info = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)
barra_menu.add_cascade(label="Acerca de", menu=menu_info)

# Agregar menú de temas
menu_tema = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Tema", menu=menu_tema)
temas = ttk.Style().theme_names()
for tema in temas:
    menu_tema.add_command(label=tema, command=lambda t=tema: cambiar_tema(t))

# Add "About" button to the menu bar
def mostrar_ventana_about():
    ventana_about = tk.Toplevel(ventana)
    ventana_about.title("About")
    ventana_about.geometry("500x500")
    
    frame_about = ttk.Frame(ventana_about)
    frame_about.pack(expand=True)
    
    label_about = ttk.Label(frame_about, text="Nombre de la Aplicación: Matrixcal\n\nVersión: 1.0\n\nDesarrolladores:\n\n- Lancelot Castro Bobadilla\n\n- Hernan Espinoza Castillo\n\n- Jonathan Medalla Aliste\n\nColaboradores:\n\n- Carolina Gomez Bravo\n\n- Alejandro Cuevas Rivero\n\n- Ernesto Vivanco Tapia\n\n\nFecha de Lanzamiento: 31/01/2024\n\n© 2024 Matrixcal. Todos los derechos reservados.")
    label_about.pack(pady=50)

menu_info.add_command(label="About", command=mostrar_ventana_about)
menu_ayuda.add_command(label="Instrucciones", command=mostrar_ventana_ayuda)

boton_home = ttk.Button(frame_opciones, text="HOME",  command=abrir_home)
boton_home.pack(pady=20)

boton_suma = ttk.Button(frame_opciones, text="SUMA", command=lambda: abrir_frame(crear_suma))
boton_suma.pack(pady=20)

boton_resta = ttk.Button(frame_opciones, text="RESTA",  command=lambda: abrir_frame(crear_resta))
boton_resta.pack(pady=20)

boton_inversa = ttk.Button(frame_opciones, text="INVERSA",  command=lambda: abrir_frame(crear_inversa))
boton_inversa.pack(pady=20)

boton_multiplica = ttk.Button(frame_opciones, text="MULTIPLICA",  command=lambda: abrir_frame(crear_multiplica))
boton_multiplica.pack(pady=20)

boton_traspuesta = ttk.Button(frame_opciones, text="TRASPUESTA",  command=lambda: abrir_frame(crear_traspuesta))
boton_traspuesta.pack(pady=20)

boton_determinante = ttk.Button(frame_opciones, text="DETERMINANTE", command=lambda: abrir_frame(crear_determinante))
boton_determinante.pack(pady=20)

abrir_home()  # Run frame_home by default

ventana.mainloop()
