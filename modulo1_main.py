"""Legacy module removed.

This repository removed the legacy `modulo1_main.py` implementation during a
refactor that renamed modules to descriptive `*_view.py` names and a single
`gui_main.py` entrypoint. Importing this module will raise ImportError to
make the breaking change explicit.

Use `gui_main.MatrixCalcApp` as the entrypoint.
"""

raise ImportError("modulo1_main has been removed. Use 'gui_main.MatrixCalcApp' instead.")

