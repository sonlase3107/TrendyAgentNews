import sqlite3
from contextlib import contextmanager
from typing import Generator

from app.core.config import get_settings


def init_db() -> None:
    """Create application tables if they do not already exist."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS topics (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT,
                is_active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL,
                url TEXT NOT NULL,
                domain TEXT
            )
            """
        )
        conn.commit()


@contextmanager
def get_connection() -> Generator[sqlite3.Connection, None, None]:
    """Yield a configured SQLite connection and close it on exit."""
    settings = get_settings()
    conn = sqlite3.connect(settings.db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
