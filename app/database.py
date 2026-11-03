import sqlite3
from pathlib import Path
from sqlite3.dbapi2 import connect

from app.models import KIND_EXPENSE, KIND_INCOME

DB_PATH = Path("data/expenses.db")
SCHEMA = """
CREATE TABLE IF NOT EXISTS categories (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    kind TEXT NOT NULL CHECK (kind IN ('expense', 'income'))
);

CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount_cents INTEGER NOT NULL CHECK (amount_cents > 0),
    category_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    comment TEXT NOT NULL DEFAULT '',
    FOREIGN KEY (category_id) REFERENCES categories(id)
);
"""
DEFAULT_CATEGORIES: list[tuple[str, str]] = [
    ("Еда", KIND_EXPENSE),
    ("Транспорт", KIND_EXPENSE),
    ("Жильё", KIND_EXPENSE),
    ("Развлечения", KIND_EXPENSE),
    ("Здоровье", KIND_EXPENSE),
    ("Прочее", KIND_EXPENSE),
    ("Зарплата", KIND_INCOME),
    ("Подработка", KIND_INCOME),
    ("Прочее (доход)", KIND_INCOME),
]

def get_connection(db_path = DB_PATH) -> sqlite3.Connection:
    """Открывает соединение с бд."""
    if db_path != ":memory:":
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def seed_default_categories(conn: sqlite3.Connection) -> None:
    count = conn.execute("SELECT COUNT(*) FROM categories").fetchone()[0]
    if count == 0:
        conn.executemany("INSERT INTO categories (name, kind) VALUES (?, ?)", DEFAULT_CATEGORIES)
        conn.commit()

def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA)
    seed_default_categories(conn)
