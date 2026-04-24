"""
Railway startup: auto-stamp baseline if Alembic has never run, then upgrade.
"""
import subprocess
import sys

from app.database import engine
from sqlalchemy import inspect


def main() -> None:
    insp = inspect(engine)
    if not insp.has_table("alembic_version"):
        print("No alembic_version table found — stamping 0001 as baseline")
        result = subprocess.run(["alembic", "stamp", "0001"])
        if result.returncode != 0:
            sys.exit(result.returncode)

    print("Running: alembic upgrade head")
    result = subprocess.run(["alembic", "upgrade", "head"])
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
