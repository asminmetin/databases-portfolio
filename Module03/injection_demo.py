"""Demonstrate SQL injection and its one correct fix: bound parameters."""

import sqlite3
from pathlib import Path

DB = Path(__file__).with_name("warehouse.db")

if not DB.exists():
    raise SystemExit(f"{DB} not found — run the Module 3 setup first")

conn = sqlite3.connect(DB)


def vulnerable(name: str):
    """DON'T DO THIS. String-building the query is the bug."""
    sql = f"SELECT customer_id, name FROM customer WHERE name = '{name}'"
    return conn.execute(sql).fetchall()


def safe(name: str):
    """DO THIS. The value is bound separately from the SQL."""
    sql = "SELECT customer_id, name FROM customer WHERE name = ?"
    return conn.execute(sql, (name,)).fetchall()


if __name__ == "__main__":
    print("normal   :", vulnerable("Customer 1"))

    # Reproduce the apostrophe crash.
    try:
        print("apostrophe:", vulnerable("O'Brien"))
    except sqlite3.Error as e:
        print("apostrophe: crashed with", e)

    # Show that the same input works when bound safely.
    print("fixed     :", safe("O'Brien"))

    # Demonstrate SQL injection.
    payload = "' OR '1'='1"
    try:
        print("injected :", vulnerable(payload)[:3], "...")
    except sqlite3.Error as e:
        print("injected : crashed with", e)

    # Show that the payload is treated as ordinary text.
    print("safe     :", safe(payload))

conn.close()