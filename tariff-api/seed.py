"""
Seed the database from an exported localStorage cfg JSON file.

Usage:
    cd tariff-api
    python seed.py path/to/cfg.json

How to get the JSON:
    1. Open admin.html in a browser that has your config in localStorage.
    2. Click "Publish" once (to make sure it's saved).
    3. Open the browser console and run:
           copy(localStorage.getItem('elec-config-v5'))
    4. Paste into a file, e.g. cfg.json, and run this script.
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
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"Error: file not found: {path}")
        sys.exit(1)

    print(f"Reading {path} …")
    with open(path, encoding="utf-8") as f:
        cfg = json.load(f)

    print("Creating database tables if needed …")
    models.Base.metadata.create_all(bind=engine)

    print("Importing data …")
    db = SessionLocal()
    try:
        result = import_cfg(cfg, db)
    finally:
        db.close()

    print("Done!")
    for k, v in result.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
