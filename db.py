"""
db.py
Modul akses database SQLite untuk menyimpan riwayat deteksi VeriPixel.
Menggunakan sqlite3 bawaan Python (tidak perlu ORM tambahan).
"""

import os
import sqlite3
from contextlib import contextmanager

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "veripixel.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS detections (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    original_filename  TEXT NOT NULL,
    gradcam_filename   TEXT NOT NULL,
    label              TEXT NOT NULL,
    confidence         REAL NOT NULL,
    created_at         TEXT NOT NULL
);
"""


def init_db():
    """Membuat tabel detections jika belum ada. Dipanggil sekali saat aplikasi start."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(SCHEMA)
        conn.commit()


@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # agar baris bisa diakses seperti dict (item["label"])
    try:
        yield conn
    finally:
        conn.close()


def insert_detection(original_filename, gradcam_filename, label, confidence, created_at):
    with get_conn() as conn:
        cur = conn.execute(
            """INSERT INTO detections
               (original_filename, gradcam_filename, label, confidence, created_at)
               VALUES (?, ?, ?, ?, ?)""",
            (original_filename, gradcam_filename, label, confidence, created_at),
        )
        conn.commit()
        return cur.lastrowid


def get_all_detections():
    with get_conn() as conn:
        return conn.execute("SELECT * FROM detections ORDER BY id DESC").fetchall()


def get_detection(detection_id):
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM detections WHERE id = ?", (detection_id,)
        ).fetchone()


def delete_detection(detection_id):
    with get_conn() as conn:
        conn.execute("DELETE FROM detections WHERE id = ?", (detection_id,))
        conn.commit()


def clear_all_detections():
    with get_conn() as conn:
        conn.execute("DELETE FROM detections")
        conn.commit()
