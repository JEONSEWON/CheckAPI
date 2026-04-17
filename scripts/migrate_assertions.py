import os
import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    print("ERROR: DATABASE_URL not set")
    exit(1)

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS monitor_assertions (
        id VARCHAR(36) PRIMARY KEY,
        monitor_id VARCHAR(36) NOT NULL REFERENCES monitors(id) ON DELETE CASCADE,
        assertion_type VARCHAR(20) NOT NULL DEFAULT 'jsonpath',
        path TEXT,
        operator VARCHAR(20) NOT NULL,
        value JSONB,
        logic VARCHAR(3) DEFAULT 'AND',
        "order" INTEGER DEFAULT 0,
        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT NOW()
    );
""")

cur.execute("CREATE INDEX IF NOT EXISTS idx_assertions_monitor_id ON monitor_assertions(monitor_id);")

conn.commit()
cur.close()
conn.close()
print("Migration done! monitor_assertions table created.")
