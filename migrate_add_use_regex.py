import os
import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    print("ERROR: DATABASE_URL not set")
    exit(1)

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

cur.execute("""
    ALTER TABLE monitors
    ADD COLUMN IF NOT EXISTS use_regex BOOLEAN DEFAULT FALSE;
""")

conn.commit()
cur.close()
conn.close()
print("Migration done! use_regex column added.")
