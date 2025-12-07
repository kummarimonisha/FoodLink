import sqlite3
from pathlib import Path

db_path = Path(__file__).resolve().parents[1] / 'foodlink.db'
print('DB path:', db_path)
if not db_path.exists():
    print('Database file not found:', db_path)
    raise SystemExit(1)

conn = sqlite3.connect(str(db_path))
cur = conn.cursor()
try:
    cur.execute("ALTER TABLE donations ADD COLUMN allocated_to_id INTEGER")
    conn.commit()
    print('Column allocated_to_id added successfully')
except Exception as e:
    print('Error:', e)
finally:
    conn.close()
