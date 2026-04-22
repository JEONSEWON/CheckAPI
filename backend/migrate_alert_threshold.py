"""
Migration: add alert_threshold and consecutive_failures to monitors table
Run once: python migrate_alert_threshold.py
"""

import os
import sys
from sqlalchemy import create_engine, text

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    print("❌ DATABASE_URL not set")
    sys.exit(1)

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    # Add alert_threshold (default 1 = alert on first failure, matches old behavior)
    try:
        conn.execute(text(
            "ALTER TABLE monitors ADD COLUMN alert_threshold INTEGER NOT NULL DEFAULT 1"
        ))
        print("✅ Added alert_threshold column")
    except Exception as e:
        if "already exists" in str(e).lower() or "duplicate" in str(e).lower():
            print("⚠️  alert_threshold already exists, skipping")
        else:
            raise

    # Add consecutive_failures (starts at 0 for all existing monitors)
    try:
        conn.execute(text(
            "ALTER TABLE monitors ADD COLUMN consecutive_failures INTEGER NOT NULL DEFAULT 0"
        ))
        print("✅ Added consecutive_failures column")
    except Exception as e:
        if "already exists" in str(e).lower() or "duplicate" in str(e).lower():
            print("⚠️  consecutive_failures already exists, skipping")
        else:
            raise

    conn.commit()

print("✅ Migration complete")
