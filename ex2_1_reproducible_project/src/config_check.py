"""Fail-safe presence-only environment configuration check."""
import os

REQUIRED = ("APP_MODE", "SERVICE_TOKEN")
def missing_settings(environ=os.environ):
    return [name for name in REQUIRED if not environ.get(name, "").strip()]
def main():
    missing = missing_settings()
    if missing:
        print("Missing configuration setting(s): " + ", ".join(missing))
        return 1
    print("Configuration check passed (values hidden).")
    return 0
if __name__ == "__main__": raise SystemExit(main())
