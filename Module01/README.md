# Module 01 — Introduction to Databases and SQL

> Learning Goals

By the end of this module, you can:

Explain how this class works — the CBL/PBL philosophy, the portfolio-based project work assessment, and the "moving bar" of a first-time course.
Set up your personal GitHub portfolio from the course template, with a clean first commit and a .gitignore that keeps databases and secrets out of Git.
Set up the entire toolchain reproducibly with uv — one fixed Python plus SQLite, DuckDB, Datasette, and more — on Windows, macOS, or Linux, and verify it.
Explain — with a measurement, not a slide — the difference between an embedded database and a client/server database, and why most local apps should not run a server.
Load real rows into SQLite and query them from Python using bound parameters.
Take a first LLM-generated query, run it, and begin the habit that defines this course: verify before you trust.
+ This is my first database course, so I want to see for myself why embedded databases like SQLite and DuckDB are fine for most local projects and don’t need a server.

one sentence: which dot-command you found most useful, and why.
+ I liked .dump command most because it is always good to have a back up in case something goes wrong.

## Overview

In this module, I learned the basics of working with databases, writing SQL queries, and checking whether query results are correct.

I worked with SQLite databases and machine telemetry data. I also used an AI-generated query as a starting point and tested it instead of automatically trusting the answer.

The main lesson I took from this module was that a query can run successfully but still make incorrect assumptions. Checking the output and testing different conditions are important parts of working with data.

## Quick Navigation

| Task | What I worked on | Evidence |
|---|---|---|
| 1. Portfolio and tools | Set up my database portfolio and development environment | [Root README](../README.md) · [pyproject.toml](../pyproject.toml) |
| 2. Explore a database | Worked with a sample SQLite database | [tour.db](tour.db) |
| 3. Query machine telemetry | Worked with readings from different machines | [telemetry.db](telemetry.db) |
| 4. SQL queries | Used SQL to summarise readings and investigate machine data | [Task 7 SQL](task7-llm.sql) |
| 5. LLM-assisted SQL profiling | Tested an AI-generated query, checked its execution plan, and compared different filters | [Query output](outputs/task7-run.txt) · [Query plan](outputs/task7-plan.txt) |

## Task 1 — Portfolio and Development Environment

I set up my database portfolio and worked with the tools needed for the course.

The goal was to have a reproducible environment for working with Python, SQLite, and SQL files. I also learned how to organise the work so that queries, database files and results could be included in my portfolio.

Evidence: [Project configuration](../pyproject.toml)

## Task 2 — Exploring SQLite Databases

I explored SQLite databases and learned how tables store related information in rows and columns.

SQLite is an embedded database, which means it can run directly inside an application without requiring a separate database server. This makes it useful for local applications and smaller data-processing tasks.

Evidence: [tour.db](tour.db)

## Task 3 — Working with Machine Telemetry

I worked with a telemetry database containing readings from machines. The readings included timestamps, machine names, temperature, vibration and spindle load.

SQL queries can be used to answer practical questions about the data, such as:

- How many readings are recorded for each machine?
- What is the highest recorded vibration for each machine?
- How many readings exceed a chosen vibration threshold?

These exercises helped me understand how SQL can turn raw readings into information that is easier to analyse.

Evidence: [telemetry.db](telemetry.db)

## Task 4 — LLM-Assisted SQL Profiling

I asked an AI model to write a query that calculates the average spindle load for each machine during the evening, ordered from highest to lowest average load.

The generated query was:

```sql
SELECT
    machine,
    AVG(spindle_load) AS avg_overnight_load
FROM readings
WHERE CAST(strftime('%H', ts) AS INTEGER) >= 18
GROUP BY machine
ORDER BY avg_overnight_load DESC;
```

The query extracts the hour from the timestamp, keeps readings from 18:00 onward, groups the readings by machine, and calculates the average spindle load.

I ran the query and checked its execution plan using `EXPLAIN QUERY PLAN`.

The plan included:

```text
SCAN readings
USE TEMP B-TREE FOR GROUP BY
USE TEMP B-TREE FOR ORDER BY
```

`SCAN readings` means SQLite reads the table entries to evaluate the filter. The temporary B-trees are used to group and sort the results.

Evidence: [Generated SQL](task7-llm.sql) · [Run output](outputs/task7-run.txt) · [Query plan](outputs/task7-plan.txt)

## Task 5 — Testing the Query and Its Assumptions

I checked whether the query returned the expected number of rows for the period from 18:00 until midnight.

The expected number was:

6 hours × 1,200 readings per hour × 2 days × 3 machines = 43,200 readings.

The query returned 43,200 rows, matching the expected count.

I also tested other filters to see whether they produced the correct result. For example, searching with `LIKE '%18%'` did not correctly identify readings after 18:00 because it searched for the characters `18` anywhere in the timestamp.

Another test showed that comparing the hour returned by `strftime` directly with the number `18` produced the wrong result. Casting the hour to an integer fixed the comparison.

Finally, I tested a longer time range, from 18:00 until 06:00. The ranking of the machines changed, showing that the meaning of "overnight" affects the result. The original query assumed that overnight ended at midnight instead of asking for clarification.

### Task 6 — size and cloud cost

- `telemetry.db`: 10,526,720 bytes, 172,800 rows → ~61 bytes/row
- 86,400 rows/day → ~5.3 MB/day → ~1.9 GB/year

Cloud cost: At about 1.9 GB per year, this dataset fits on any shop-floor PC; in the cloud, Wittkamp would pay a recurring monthly bill for a database server, backups and someone to maintain them, all for one dashboard and one weekly report, while the embedded SQLite file adds no infrastructure cost at all.

http://127.0.0.1:8001/telemetry/readings?machine__exact=cnc-02&_sort_desc=vib_rms 


## Main Takeaways

- SQLite allows applications to store and query data without a separate database server.
- SQL can summarise raw data using filtering, grouping and aggregate functions.
- AI-generated SQL should be tested against the real data.
- `EXPLAIN QUERY PLAN` helps explain how SQLite accesses and processes data.
- Expected row counts and alternative filters are useful ways to verify query correctness.
- Clear requirements matter because words such as "overnight" can have more than one interpretation.

## Final Reflection

This module gave me a practical introduction to working with databases and SQL. I learned that understanding the data and checking the results are just as important as writing the query itself.

The most valuable experience was testing an AI-generated query, finding problems with alternative filters, and correcting the conditions instead of accepting the original answer without verification.






- Main takeaway:
The most important lesson from this module was to verify SQL instead of trusting it just because it runs. I checked row counts and query plans, and tested edge cases to see whether the results matched the question. 


## Reflection 1
[Reflection 1](/Reflections/ref01.md)



