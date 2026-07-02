"""
数据库初始化与工具函数（SQLite，原生 sqlite3 实现，零依赖）。
"""
import sqlite3
import os
from app.config import settings


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(settings.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    os.makedirs(os.path.dirname(settings.DATABASE_PATH), exist_ok=True)
    os.makedirs(settings.EXPORT_DIR, exist_ok=True)
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            template_type TEXT NOT NULL,
            content TEXT NOT NULL,
            variables TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS clauses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            content TEXT NOT NULL,
            applicable_condition TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS risk_rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rule_name TEXT NOT NULL,
            rule_type TEXT NOT NULL,
            severity TEXT NOT NULL DEFAULT 'medium',
            condition_expr TEXT NOT NULL,
            message_template TEXT NOT NULL,
            suggestion TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS generation_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_text TEXT NOT NULL,
            parsed_spec TEXT,
            selected_clauses TEXT,
            risk_report TEXT,
            file_path TEXT,
            file_name TEXT,
            status TEXT DEFAULT 'created',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    conn.close()
