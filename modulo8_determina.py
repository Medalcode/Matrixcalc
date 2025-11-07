import tkinter as tk
from tkinter import ttk
import numpy as np
"""Compatibility shim: re-export `crear_determinante` from `determinant_view`.

This preserves the legacy import path while delegating to the modern
implementation in `determinant_view.py`.
"""

from determinant_view import crear_determinante
    def __init__(self, parent, show_frame_callback=None):
