#!/usr/bin/env python3
"""Benchmark the Module 03 dashboard query and index experiments.

Usage:
    python Module03/bench.py path/to/dashboard.db

Uses only Python's standard library. Runs a warm-up, then five timed runs per
stage and reports the median. It drops/recreates only the three benchmark
indexes named in the assignment. Run it on a copy of your course database if
those index names are already used for other work.
"""
from __future__ import annotations

import argparse
import os
import statistics
import sqlite3
import sys
import time
from typing import Sequence

DASHBOARD_QUERY = """
SELECT customer.city,
       COUNT(DISTINCT customer.customer_id) AS customers,
       SUM(order_line.qty * product.price) AS revenue
FROM customer
JOIN orders
  ON orders.customer_id = customer.customer_id
JOIN order_line
  ON order_line.order_id = orders.order_id
JOIN product
  ON product.product_id = order_line.product_id
WHERE orders.ordered_on >= '2025-01-01'
  AND orders.ordered_on < '2026-01-01'
GROUP BY customer.city
ORDER BY revenue DESC
"""

SINGLE_DAY_QUERY = """
SELECT orders.order_id, orders.ordered_on, customer.name
FROM orders
JOIN customer
  ON customer.customer_id = orders.customer_id
WHERE orders.ordered_on = '2026-02-14'
"""

INDEXES = (
    ("ix_orders_ordered_on", "CREATE INDEX ix_orders_ordered_on ON orders(ordered_on)"),
    ("ix_orderline_order", "CREATE INDEX ix_orderline_order ON order_line(order_id)"),
    ("ix_orderline_product", "CREATE INDEX ix_orderline_product ON order_line(product_id)"),
)

REQUIRED_COLUMNS = {
    "customer": {"customer_id", "name", "city"},
    "product": {"product_id", "sku", "price"},
    "orders": {"order_id", "customer_id", "ordered_on", "status"},
    "order_line": {"order_id", "product_id", "qty"},
}


def plan(conn: sqlite3.Connection, query: str, params: Sequence[object] = ()) -> list[str]:
    rows = conn.execute("EXPLAIN QUERY PLAN " + query, params).fetchall()
    return [str(row[3]) for row in rows]


def print_plan(conn: sqlite3.Connection, title: str, query: str,
               params: Sequence[object] = ()) -> None:
    print(f"\nPLAN — {title}")
    for detail in plan(conn, query, params):
        print(f"  {detail}")


def median_ms(conn: sqlite3.Connection, query: str, runs: int = 5) -> tuple[list[float], float]:
    # Warm the file cache first; do not include the warm-up in the samples.
    conn.execute(query).fetchall()
    samples: list[float] = []
    for _ in range(runs):
        start = time.perf_counter()
        conn.execute(query).fetchall()
        samples.append((time.perf_counter() - start) * 1000.0)
    return samples, statistics.median(samples)


def print_timing(conn: sqlite3.Connection, title: str, query: str) -> None:
    samples, median = median_ms(conn, query)
    formatted = ", ".join(f"{value:.3f}" for value in samples)
    print(f"TIME — {title}: runs (ms) = [{formatted}], median = {median:.3f} ms")


def validate_schema(conn: sqlite3.Connection) -> None:
    tables = {
        row[0]
        for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    }
    missing_tables = set(REQUIRED_COLUMNS) - tables
    if missing_tables:
        raise ValueError(
            "This is not the dashboard database. Missing tables: "
            + ", ".join(sorted(missing_tables))
            + ". The Module02/legacy.db file only contains machine, part, and maint_job. "
              "Pass the database that contains customer, product, orders, and order_line."
        )
    for table, required in REQUIRED_COLUMNS.items():
        actual = {row[1] for row in conn.execute(f"PRAGMA table_info({table})")}
        missing = required - actual
        if missing:
            raise ValueError(f"Table {table} is missing columns: {', '.join(sorted(missing))}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("database", help="path to the course dashboard SQLite database")
    args = parser.parse_args()
    database_path = os.path.abspath(args.database)
    if not os.path.isfile(database_path):
        print(f"Database file not found: {database_path}", file=sys.stderr)
        return 2

    print(f"Database: {database_path}")
    print(f"SQLite version: {sqlite3.sqlite_version}")
    print("Method: same Python process/connection; one warm-up + five timed runs; median reported.")
    print("Note: timings are comparable within this run; do not compare them directly to sqlite3 CLI .timer results.")

    try:
        conn = sqlite3.connect(database_path)
        with conn:
            validate_schema(conn)
            # Reset just the benchmark indexes, as requested by the task.
            for name, _ in INDEXES:
                conn.execute(f"DROP INDEX IF EXISTS {name}")

            # Baseline dashboard and single-day lookup.
            print("\n=== BASELINE: no benchmark indexes ===")
            print_plan(conn, "dashboard", DASHBOARD_QUERY)
            print_timing(conn, "dashboard", DASHBOARD_QUERY)
            print_plan(conn, "single-day lookup", SINGLE_DAY_QUERY)
            print_timing(conn, "single-day lookup", SINGLE_DAY_QUERY)

            # Add the indexes one at a time, preserving previous stages.
            for index_name, create_sql in INDEXES:
                conn.execute(create_sql)
                conn.commit()
                print(f"\n=== AFTER ADDING {index_name} ===")
                print_plan(conn, "dashboard", DASHBOARD_QUERY)
                print_timing(conn, "dashboard", DASHBOARD_QUERY)
                if index_name == "ix_orders_ordered_on":
                    print_plan(conn, "single-day lookup", SINGLE_DAY_QUERY)
                    print_timing(conn, "single-day lookup", SINGLE_DAY_QUERY)

            # Negative result: dashboard joins to product through product's PK,
            # so ix_orderline_product may not be selected for this query.
            print_plan(conn, "dashboard after all three indexes", DASHBOARD_QUERY)

            # Positive control: filter directly on order_line.product_id.
            product_id_row = conn.execute(
                "SELECT product_id FROM order_line WHERE product_id IS NOT NULL LIMIT 1"
            ).fetchone()
            if product_id_row is not None:
                product_query = "SELECT order_id, product_id, qty FROM order_line WHERE product_id = ?"
                print_plan(conn, "direct product_id lookup (index should be useful)",
                           product_query, (product_id_row[0],))

            # Negative result: function on ordered_on usually prevents a normal
            # index on ordered_on from serving as a direct equality lookup.
            function_query = "SELECT order_id FROM orders WHERE date(ordered_on) = '2026-02-14'"
            print_plan(conn, "date() wraps ordered_on (normal index usually not used)", function_query)
    except (sqlite3.Error, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    finally:
        try:
            conn.close()
        except UnboundLocalError:
            pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
