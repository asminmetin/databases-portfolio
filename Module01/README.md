# Module 1

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

## Reflection 1
[Reflection 1](/Reflections/ref01.md)


### Task 6 — size and cloud cost

- `telemetry.db`: 10,526,720 bytes, 172,800 rows → ~61 bytes/row
- 86,400 rows/day → ~5.3 MB/day → ~1.9 GB/year

Cloud cost: At about 1.9 GB per year, this dataset fits on any shop-floor PC; in the cloud, Wittkamp would pay a recurring monthly bill for a database server, backups and someone to maintain them, all for one dashboard and one weekly report, while the embedded SQLite file adds no infrastructure cost at all.



