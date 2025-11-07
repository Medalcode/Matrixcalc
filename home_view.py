"""home_view.py

Contiene la pantalla de bienvenida (home) y recursos UI asociados.
"""
from PIL import ImageTk, Image
import tkinter as tk
import os


def crear_home(ventana):
    frame_home = tk.Frame(ventana, width=550, height=550, bg="white") 
    label_home = tk.Label(frame_home, text="Calculadora\nMatricial\n\n", font=("Bold", 20), bg="white")
    label_home.pack(pady=20)

    # Insertar imagen
    image_path = os.path.join(os.path.dirname(__file__), "logo.jpg")
    if os.path.exists(image_path):
        image = Image.open(image_path)
        image = image.resize((200, 200))
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(frame_home, image=photo, bg="white")
        label.image = photo
        label.pack()
    else:
        # If the image is missing, show a harmless placeholder label instead
        # of raising an exception. This makes the UI robust when resources
        # are not bundled with the repo (e.g., running from source).
        label = tk.Label(frame_home, text="[logo not found]", bg="white")
        label.pack()

    return frame_home
