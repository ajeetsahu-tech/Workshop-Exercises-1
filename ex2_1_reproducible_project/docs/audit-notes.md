# Dependency and configuration audit

| Package | Version | Purpose |
|---|---|---|
| Python standard library | 3.10+ | JSON, CSV, environment access and package metadata; no external runtime dependency |

Run `python src/dependency_audit.py` inside the activated environment to create an exact version inventory from installed distributions. Keep it environment-specific; the repository intentionally has no pinned external packages. Startup checks setting names only and suppresses their values. `.env` and virtual environments are ignored.

**Evidence:** The test module covers valid configuration, a missing token, and blank configuration. Run `python -m unittest discover -s tests -v` in the project directory. The exercise folder itself is reproducible using `py -m venv .venv`; a virtual environment is local machine state and is deliberately not committed.
