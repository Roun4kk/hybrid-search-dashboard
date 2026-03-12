import sqlite3
from datetime import datetime
import os

DB_PATH = "data/metrics/search_logs.db"


def init_db():
    os.makedirs("data/metrics", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS search_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        query TEXT,
        top_k INTEGER,
        alpha REAL,
        result_count INTEGER,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()


def log_query(query, top_k, alpha, result_count):

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO search_logs
    (query, top_k, alpha, result_count, timestamp)
    VALUES (?, ?, ?, ?, ?)
    """, (
        query,
        top_k,
        alpha,
        result_count,
        datetime.utcnow().isoformat()
    ))

    conn.commit()
    conn.close()