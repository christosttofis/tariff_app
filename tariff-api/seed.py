"""
First-time setup only: load a legacy localStorage cfg JSON export (from the
pre-database version of admin.html) into an EMPTY database.

Usage:
    cd tariff-api
    python seed.py path/to/cfg.json [--force]

This replaces all suppliers, profiles and tariffs and marks every imported
tariff as approved (see importer.py). It refuses to run if the database
already contains suppliers or tariffs; --force overrides that, and will
destroy the existing data. Take a backup first (ADMIN_MANUAL.md 15.5).
"""

import json
import sys
from pathlib import Path

# Ensure the tariff-api package is on sys.path when run from any cwd
sys.path.insert(0, str(Path(__file__).parent))

import models
from database import SessionLocal, engine
from importer import import_cfg


def main():
    args = [a for a in sys.argv[1:] if a != "--force"]
    force = "--force" in sys.argv[1:]
    if len(args) != 1:
        print(__doc__)
        sys.exit(1)

    path = Path(args[0])
    if not path.exists():
        print(f"Error: file not found: {path}")
        sys.exit(1)

    print(f"Reading {path} …")
    with open(path, encoding="utf-8") as f:
        cfg = json.load(f)

    print("Creating database tables if needed …")
    models.Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        existing = db.query(models.Tariff).count() + db.query(models.Supplier).count()
        if existing and not force:
            print("Refusing to import: the database already contains suppliers/tariffs, which "
                  "this import would delete and replace. Re-run with --force only if that is "
                  "really intended, after taking a backup.")
            sys.exit(1)
        print("Importing data …")
        result = import_cfg(cfg, db)
    finally:
        db.close()

    print("Done!")
    for k, v in result.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
