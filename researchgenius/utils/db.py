import sqlite3, json
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "research.db"

def get_conn():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feature TEXT NOT NULL,
            topic TEXT NOT NULL,
            result_json TEXT,
            score INTEGER DEFAULT 0,
            status TEXT DEFAULT 'active',
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now'))
        );
    """)
    conn.commit(); conn.close()

def save_result(feature, topic, result, score=0):
    init_db()
    conn = get_conn()
    cur = conn.execute("INSERT INTO sessions (feature,topic,result_json,score) VALUES (?,?,?,?)",
                       (feature, topic[:120], json.dumps(result), score))
    conn.commit(); rid = cur.lastrowid; conn.close(); return rid

def get_all_results():
    init_db()
    conn = get_conn()
    rows = conn.execute("SELECT * FROM sessions ORDER BY created_at DESC").fetchall()
    conn.close(); return [dict(r) for r in rows]

def update_status(rid, status):
    init_db()
    conn = get_conn()
    conn.execute("UPDATE sessions SET status=?,updated_at=datetime('now') WHERE id=?", (status, rid))
    conn.commit(); conn.close()

def delete_result(rid):
    init_db()
    conn = get_conn()
    conn.execute("DELETE FROM sessions WHERE id=?", (rid,))
    conn.commit(); conn.close()
