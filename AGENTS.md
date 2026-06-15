# MatrixCalc — Agent Guide

## Commands
```bash
make test                       # run all 158 backend tests
make migrate                    # Django migrations
make up                         # docker-compose up --build (Postgres + backend + frontend + Redis + Celery)
make shell                      # docker-compose exec backend sh
make dev                        # local dev (SQLite, no Docker)

# Manual test run:
python -m pytest -q             # from repo root (uses pytest.ini)

# Frontend tests:
cd frontend && npx vitest run   # 5 Vitest tests
```

## Critical Quirks

- **This is a LARGE codebase** — 182 files, Django + Celery + Redis + Vue 3 + TypeScript + Tailwind. The entry points are:
  - `manage.py` (Django)
  - `matrixcalc_web/settings.py` (Django settings — 273 lines)
  - `calculator/views.py` (REST API — 429 lines)
  - `frontend/src/main.ts` (Vue 3 SPA)
- **Single Dockerfile**: The project uses a single multi-stage `Dockerfile` in the root directory for production, which handles both backend and frontend.
- **Celery+Redis required** for async tasks (backup export, data cleanup). The `worker` service in docker-compose runs `celery -A matrixcalc_web worker -l info --concurrency=2`.
- **pytest.ini** configures: `DJANGO_SETTINGS_MODULE`, `--no-migrations`, `--reuse-db`, `--cov=calculator` with HTML/XML/terminal coverage reports. **158 tests** with 99% coverage.
- **Google Cloud Build** (`cloudbuild.yaml`) is the production deployment pipeline — not GitHub Actions. CI (`.github/workflows/ci.yml`) uses flake8 + pytest but does NOT deploy.
- **Dual database mode**: PostgreSQL in Docker, SQLite for local dev / Cloud Run fallback. The settings.py auto-detects via `DATABASE_URL`.
- **Matrix engine** is in `calculator/utils/matrix_model.py` (367 lines) — pure NumPy, all operations return `(result | None, error | None)` tuples. Safe wrappers (`safe_add`, `safe_dot`, `safe_inv`, etc.) catch NumPy errors.
- **Rate limiting** enabled via `django-ratelimit` — 100 requests/hour per user on matrix operations.
- **Frontend i18n**: Spanish (`es`) and English (`en`) via `vue-i18n`. All new UI text must be added to both locale files.
- **Backup system**: Django management commands `export_backup` and `import_backup` + scheduled Celery task. Backups stored in `backups/` directory.
