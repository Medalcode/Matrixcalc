# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.2.0] - 2026-08-04

### Added
- **Architecture**: Introduced `OperationService` in `calculator/services.py` to decouple business logic from HTTP controller views.
- **Testing**: Added end-to-end smoke and regression test suite (`test_smoke_regression.py`) covering complete matrix lifecycles and edge cases.
- **Frontend Testing**: Added unit tests for frontend utility modules (`shortcuts.spec.ts`, `matrixTemplates.spec.ts`), expanding Vitest suite to 45 passing tests.

### Changed
- **Data Safety**: Converted `Operation` foreign keys (`matrix_a`, `matrix_b`, `result`) from `CASCADE` to `SET_NULL` to prevent accidental history loss upon matrix deletion.
- **Error Handling**: Hardened `safe_dot` and `safe_rank` functions to catch `ValueError` and general runtime exceptions alongside `LinAlgError`.

### Fixed
- **Linting & Types**: Resolved all Flake8 compliance errors and fixed 100% of TypeScript errors in `vue-tsc` type-check build.

## [3.1.0] - 2026-08-01

### Added
- **CI/CD**: Added frontend testing suite (`vitest`) to GitHub Actions pipeline.
- **Testing**: E2E and frontend unit tests planned and configured in implementation phase.

### Changed
- **Docker**: Optimized `Dockerfile` multi-stage build by caching `package.json` and `package-lock.json` separately, significantly reducing build times.
- **Python**: Pinned CI matrix to Python 3.11 to align exactly with `pyproject.toml` and Docker base image.
- **Makefile**: Replaced deprecated `manage.py test` with `pytest` for backend test command.

### Security
- **Config**: Removed `backend-prod-config.yaml` to eliminate hardcoded secrets and wildcards (`ALLOWED_HOSTS: *`).
- **Dependencies**: Pinned all Python dependencies in `requirements.txt` to exact versions (`==`) to guarantee reproducible builds and prevent silent breakages from minor updates.
