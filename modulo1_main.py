"""Backward-compatibility shim for the renamed GUI entrypoint.

This module preserves the old module name `modulo1_main` for any external
scripts that still import it. It re-exports MatrixCalcApp from `gui_main`.
"""

from gui_main import MatrixCalcApp


if __name__ == "__main__":
    app = MatrixCalcApp()
    app.mainloop()

