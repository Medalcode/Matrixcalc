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

## Numeric policy

All numerical parsing and operations are centralized in `matrix_model.py`.
Key decisions:

- Input parsing uses `np.float64` for consistency across operations.
- `safe_inv` rejects matrices whose condition number exceeds `1e12` to avoid
	returning numerically unstable inverses. This threshold is documented in
	`matrix_model.py` and tested in the unit tests (`test_model.py`).

If you need to change the numeric policy (for example a different threshold or
dtype), update `matrix_model.py` and extend tests accordingly.
