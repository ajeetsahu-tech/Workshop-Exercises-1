# Exercise 2.1 — Reproducible Python project

This dependency-light audit tool uses Python's standard library. From this folder, create and activate an isolated environment:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python src\config_check.py
python src\dependency_audit.py
python -m unittest discover -s tests -v
```

On macOS/Linux replace activation with `source .venv/bin/activate`. `requirements.txt` is intentionally empty because no external package is required. No credentials are needed; `.env.example` contains harmless dummy settings. Copy it to `.env` for local experimentation; `.env` is ignored by Git. The startup checker only reports missing setting names and never prints values.

## Structure

`src/` scripts; `tests/` standard-library tests; `data/` sample inventory; `logs/` runtime logs; `docs/` setup and audit evidence.

## Reproduce

Install Python 3.10 or newer, create the venv above, and run the two commands. The scripts have no third-party dependencies, so the same environment can be recreated from `requirements.txt` without a package download.
