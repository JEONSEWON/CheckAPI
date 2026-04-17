import os
import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    print("ERROR: DATABASE_URL not set")
    exit(1)

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS maintenance_windows (
        id VARCHAR(36) PRIMARY KEY,
        user_id VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        name VARCHAR(255) NOT NULL,
        repeat_type VARCHAR(20) DEFAULT 'once',
        weekday INTEGER,
        day_of_month INTEGER,
        start_time VARCHAR(5) NOT NULL,
        end_time VARCHAR(5) NOT NULL,
        start_date TIMESTAMP,
        end_date TIMESTAMP,
        timezone VARCHAR(50) DEFAULT 'UTC',
        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT NOW(),
        updated_at TIMESTAMP DEFAULT NOW()
    );
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS maintenance_window_monitors (
        maintenance_window_id VARCHAR(36) NOT NULL REFERENCES maintenance_windows(id) ON DELETE CASCADE,
        monitor_id VARCHAR(36) NOT NULL REFERENCES monitors(id) ON DELETE CASCADE,
        PRIMARY KEY (maintenance_window_id, monitor_id)
    );
""")

conn.commit()
cur.close()
conn.close()
print("Migration done! maintenance_windows and maintenance_window_monitors tables created.")
