# Module 03 — SQL Query Plans, Indexes and Security

# Learning Goals

This module gives you the opportunity to explore complex querying and query optimization and achieve competency in writing, profiling, and securing SQL.

By the end of this module, you can:

Build complex DQL queries: joins, aggregation with GROUP BY/HAVING, subqueries, and window functions.
Read EXPLAIN QUERY PLAN as primary evidence: say what the engine will do for a given query, tell a SCAN from a SEARCH, and a table lookup from a covering index.
Benchmark the effect of an index and explain when the planner ignores one.
Generate a query with an LLM, then verify it: correctness, performance, and edge cases.
Prevent SQL injection with bound parameters and demonstrate why string concatenation is exploitable.

## Overview

In this module, I worked on understanding how SQL queries are represented, executed and improved. I used relational algebra, SQLite query plans, index benchmarks and a SQL injection demonstration.

My main goal was to verify the behaviour of queries rather than relying only on what an AI model suggested.

## Quick Navigation

| Task | What I did | Main evidence |
|---|---|---|
| 1. SQL and query plans | Examined SQL behaviour and execution plans | [sql-notes.md](sql-notes.md) |
| 2. Index benchmark | Measured query execution times before and after adding indexes | [bench.py](bench.py), [warehouse.db](warehouse.db) |
| 3. SQL injection drill | Demonstrated unsafe SQL construction and fixed it with bound parameters | [injection_demo.py](injection_demo.py) |
| 4. Relational algebra | Translated a SQL query into relational algebra and checked that both describe the same operations | [sql-notes.md](sql-notes.md) |

The files above are intended to be kept in the `Module03` folder. Make sure `injection_demo.py` is present there before publishing the portfolio.

## Task 1 — SQL and Relational Algebra

I connected SQL statements with their relational algebra operations.

- Selection (`σ`) filters rows.
- Projection (`π`) selects columns.
- Join (`⋈`) combines related tables.
- Grouping and aggregation (`γ`) calculate values such as counts and sums.

I checked that the conditions, joins and output columns in the SQL query matched the corresponding algebra operations.

Evidence: [sql-notes.md](sql-notes.md)

## Task 2 — Query Plans and Index Benchmarking

I used `EXPLAIN QUERY PLAN` to see how SQLite executed queries and `bench.py` to measure execution time.

The benchmark used one warm-up and five timed runs per stage, reporting the median.

### Measured Results

| Query and stage | Median time |
|---|---:|
| Dashboard — baseline | 79.516 ms |
| Dashboard — after adding the date index | 79.041 ms |
| Dashboard — after adding the order-line index | 259.785 ms |
| Dashboard — after adding all three indexes | 255.581 ms |
| Single-day lookup — baseline | 2.011 ms |
| Single-day lookup — with the date index | 0.092 ms |

The date index greatly improved the single-day lookup, but barely changed the dashboard query. The dashboard became slower after the order-line index was added to the existing date index.

The query plan also showed that the product index was used for a direct lookup by `product_id`, although it was not used in the dashboard plan.

**Important limitation:** The benchmark results are cumulative because indexes were added successively. They do not isolate the individual effect of every index. Independent tests on fresh baseline copies would be needed to measure each index separately.

Evidence: [bench.py](bench.py) · [sql-notes.md](sql-notes.md)

## Task 3 — SQL Injection Drill

I demonstrated what happens when user input is inserted directly into an SQL query.

The vulnerable query uses an f-string. An apostrophe in a name such as `O'Brien` can break the SQL statement. The payload `' OR '1'='1` can also change the meaning of the query.

I then used a bound parameter (`?`) to separate the SQL statement from the supplied value. This allows the apostrophe to be handled as part of the name and prevents the payload from being interpreted as SQL code.

Evidence: [injection_demo.py](injection_demo.py)

## Task 4 — One Query, from Algebra to Plan

I represented a SQL query using relational algebra and explained how its operations correspond to the SQL clauses.

I also interpreted query plans using terms such as `SCAN`, `SEARCH` and temporary B-trees. This helped me understand the difference between the logical operations of a query and the execution strategy chosen by SQLite.

Evidence: [sql-notes.md](sql-notes.md)

## Main Takeaways

- A query can be logically correct but still have a slow execution plan.
- An index is not guaranteed to improve every query.
- `EXPLAIN QUERY PLAN` helps explain how SQLite accesses data.
- A measured result is more useful than assuming an index is beneficial.
- Bound parameters are safer than manually building SQL strings with user input.
- AI-generated SQL should be executed and verified before being accepted.

## Final Reflection

This module helped me connect SQL theory with practical testing. The most important lesson was that I need to check both correctness and performance. I also learned that a safe query should keep user input separate from SQL syntax.


[Reflection3](../Reflections/ref03.md)
