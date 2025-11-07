# matrixcalc
matrix calculator

## Breaking changes (renames)

This repository refactored the original procedural modules (`moduloX_*.py`) to
Pythonic, descriptive view modules and a single GUI entrypoint. The following
changes were applied:

- `gui_main.py` is the new canonical entrypoint (replaces `modulo1_main.py`).
- View modules were renamed to `*_view.py` (for example `sum_view.py`, `multiply_view.py`, etc.).

All legacy `moduloX_*.py` compatibility shims were removed in this refactor. If
you relied on the old import paths, update imports to the new module names.

## Migration / Breaking changes (detailed)

If your code or scripts imported the legacy `moduloN_*` modules, update them to
use the new modules. Below is a mapping of the old module names to the new
locations plus short examples to help migrate.

Mapping

- `modulo1_main.py` -> `gui_main.MatrixCalcApp`
- `modulo2_home.py` -> `home_view.crear_home`
- `modulo3_suma.py` -> `sum_view.crear_suma`
- `modulo4_resta.py` -> `subtract_view.crear_resta`
- `modulo5_inversa.py` -> `inverse_view.crear_inversa`
- `modulo6_multiplica.py` -> `multiply_view.crear_multiplica`
- `modulo7_traspuesta.py` -> `transpose_view.crear_traspuesta`
- `modulo8_determina.py` -> `determinant_view.crear_determinante`

Quick examples

1) Old import (legacy):

```python
# antiguo
from modulo3_suma import main as suma_main

# ...use suma_main() ...
```

2) New import (recommended):

```python
# nuevo
from sum_view import crear_suma

# call the new view factory or integrate with MatrixCalcApp
crear_suma()
```

Entrypoint example

Previously some users started the GUI via `modulo1_main.py`. Use the new
entrypoint instead:

```python
from gui_main import MatrixCalcApp

app = MatrixCalcApp()
app.mainloop()
```

Notes and recommendations

- The numeric and GUI logic were moved to `matrix_model.py` (numeric core) and
	`*_view.py` modules (GUI screens). Removing the legacy files reduces
	maintenance burden and avoids duplication.
- If you maintain external projects that import the old names, consider either
	updating those projects or creating a small compatibility package/branch that
	provides shims.
- Unit tests cover the numeric model and were run after the refactor; they
	passed (see `test_model.py`).

## Numeric policy

All numerical parsing and operations are centralized in `matrix_model.py`.
Key decisions:

- Input parsing uses `np.float64` for consistency across operations.
- `safe_inv` rejects matrices whose condition number exceeds `1e12` to avoid
	returning numerically unstable inverses. This threshold is documented in
	`matrix_model.py` and tested in the unit tests (`test_model.py`).

If you need to change the numeric policy (for example a different threshold or
dtype), update `matrix_model.py` and extend tests accordingly.
