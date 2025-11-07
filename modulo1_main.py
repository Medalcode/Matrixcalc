"""Compatibility shim: re-export MatrixCalcApp from `gui_main`.

This module is kept to avoid breaking external imports that reference the
historical name `modulo1_main`. It simply re-exports the canonical
application class from `gui_main`.
"""

from gui_main import MatrixCalcApp


if __name__ == "__main__":
    app = MatrixCalcApp()
    app.mainloop()

