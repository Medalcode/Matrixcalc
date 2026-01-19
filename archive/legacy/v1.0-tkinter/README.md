# MatrixCalc v1.0 - Tkinter Desktop App (Legacy)

This directory contains the original Tkinter desktop application code from MatrixCalc v1.0.

**Status:** Deprecated (replaced by Django + Vue.js web app in v2.0)  
**Archived:** January 19, 2026  
**Reason:** Migration to web application completed

---

## 📁 Files

### Core Application

- `gui_main.py` - Main Tkinter application entry point
- `matrix_editor.py` - Matrix editor GUI component
- `matrix_model.py` - Matrix calculation logic (superseded by `calculator/utils/matrix_model.py`)
- `exceptions.py` - Custom exceptions (superseded by `calculator/utils/exceptions.py`)

### View Components (`views/`)

- `home_view.py` - Home screen view
- `sum_view.py` - Matrix addition view
- `subtract_view.py` - Matrix subtraction view
- `multiply_view.py` - Matrix multiplication view
- `inverse_view.py` - Matrix inverse view
- `determinant_view.py` - Determinant calculation view
- `transpose_view.py` - Matrix transpose view
- `result_viewer.py` - Results display component

### Testing

- `test_model.py` - Unit tests for v1.0 matrix model

### Dependencies

- `requirements.txt` - Python dependencies for desktop app

---

## 🚀 To Run (Historical Reference Only)

```bash
# Install Tkinter dependencies
pip install -r requirements.txt

# Run desktop app
python gui_main.py
```

**Note:** This code is preserved for historical reference only.

---

## 🔄 Migration to v2.0

The desktop application was migrated to a modern web application:

**v1.0 (Tkinter)** → **v2.0 (Django + Vue.js)**

### What Changed:

- **GUI:** Tkinter → Vue.js 3 + TypeScript
- **Backend:** Standalone Python → Django REST API
- **Database:** In-memory → PostgreSQL
- **Deployment:** Desktop executable → Cloud Run / Docker

### Migration Guide:

See [`docs/migration/v1-to-v2.md`](../../docs/migration/v1-to-v2.md) for complete migration documentation.

---

## 📚 Documentation

For current MatrixCalc documentation, see:

- [Main README](../../README.md)
- [Documentation Index](../../docs/README.md)
- [Deployment Guide](../../docs/deployment/README.md)

---

**Last updated:** January 19, 2026  
**Archived by:** Documentation consolidation project
