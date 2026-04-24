"""
Migration helper script.

Usage:
  # Apply pending migrations:
  python migrate.py upgrade

  # Mark existing DB as up-to-date (first-time Alembic adoption on live DB):
  python migrate.py stamp

  # Show current revision:
  python migrate.py current

  # Auto-generate migration after model changes:
  python migrate.py generate "describe your change"
"""

import sys
import subprocess


def run(cmd: list[str]) -> None:
    result = subprocess.run(["alembic"] + cmd, cwd=".")
    sys.exit(result.returncode)


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    action = sys.argv[1]

    if action == "upgrade":
        run(["upgrade", "head"])
    elif action == "stamp":
        run(["stamp", "head"])
    elif action == "current":
        run(["current"])
    elif action == "generate":
        if len(sys.argv) < 3:
            print("Usage: python migrate.py generate <message>")
            sys.exit(1)
        run(["revision", "--autogenerate", "-m", sys.argv[2]])
    elif action == "downgrade":
        target = sys.argv[2] if len(sys.argv) > 2 else "-1"
        run(["downgrade", target])
    else:
        print(f"Unknown action: {action}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
