import os
import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    print("ERROR: DATABASE_URL not set")
    exit(1)

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

cur.execute("ALTER TABLE monitors ADD COLUMN IF NOT EXISTS monitor_type VARCHAR(20) DEFAULT 'http';")
cur.execute("ALTER TABLE monitors ADD COLUMN IF NOT EXISTS heartbeat_token VARCHAR(64) UNIQUE;")
cur.execute("ALTER TABLE monitors ADD COLUMN IF NOT EXISTS heartbeat_interval INTEGER;")
cur.execute("ALTER TABLE monitors ADD COLUMN IF NOT EXISTS heartbeat_grace INTEGER DEFAULT 5;")
cur.execute("ALTER TABLE monitors ADD COLUMN IF NOT EXISTS last_ping_at TIMESTAMP;")
cur.execute("CREATE INDEX IF NOT EXISTS idx_monitors_heartbeat_token ON monitors(heartbeat_token);")

conn.commit()
cur.close()
conn.close()
print("Migration done! Heartbeat fields added.")
