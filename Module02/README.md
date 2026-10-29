# Module 02 — Database Schema Audit and Data Contracts

In this module, I worked with a legacy maintenance database for a machine shop. My goal was to understand how the existing tables were connected, identify data-quality problems, and design a better structure to prevent these problems in the future.

The main lesson was that a database can contain data that looks usable but is not reliable because important rules are missing.

## Quick Navigation

| Task | What I did | Main evidence |
|---|---|---|
| 1. Inspect the database | Examined the legacy tables and their contents | [legacy.db](legacy.db), [legacy_schema.sql](legacy_schema.sql) |
| 2. Audit the schema | Identified entities, intended keys and relationships | [er-audit.md](er-audit.md) |
| 3. Check data integrity | Used SQL queries to find inconsistent and duplicate data | [integrity-defects.md](integrity-defects.md) |
| 4. Design a better schema | Created application-level validation and database constraints | [contract.py](contract.py), [contract-ddl.sql](contract-ddl.sql) |
| 5. Document the solution | Explained the rules and limitations of the new design | [contract-notes.md](contract-notes.md) |

## Task 1 — Inspect the Legacy Database

I examined the `machine`, `part` and `maint_job` tables in `legacy.db`.

The tables contained information about machines, spare parts and maintenance jobs. However, the schema had almost no declared primary keys or foreign keys, so many relationships depended on text values matching.

**What I learned:** Having related information in different tables does not automatically mean that the database correctly enforces their relationships.

Evidence: [legacy.db](legacy.db) · [legacy_schema.sql](legacy_schema.sql)

## Task 2 — ER Audit and Cardinalities

I reconstructed the intended entities and relationships and checked them against the sample data.

The main relationships were:

- One machine can have multiple maintenance jobs.
- One technician can perform multiple jobs.
- One maintenance job can use multiple parts, and one part can be used in multiple jobs.

The last relationship is many-to-many and should be represented using a separate junction table.

Evidence: [er-audit.md](er-audit.md)

## Task 3 — Data Integrity Problems

I used SQL queries to identify problems in the existing data.

| Problem | Finding |
|---|---|
| Missing machine reference | Maintenance job 3 refers to `cnc-05`, which is not in the machine table. |
| Duplicate part number | `P-1003` occurs twice. |
| Incorrect data type | Part prices are stored as text. |
| Invalid date value | The machine `RANDOM-NAME` has `unknown` as its installation date. |
| Poor relationship structure | `parts_used` stores multiple part numbers in one cell. |

These problems can lead to missing join results, duplicate records and incorrect calculations.

Evidence: [integrity-defects.md](integrity-defects.md)

## Task 4 — Improved Schema and Data Contracts

I used Pydantic to validate application data and SQLAlchemy to define the database structure.

The improved design includes primary keys, foreign keys, required fields, a unique constraint for machine serial numbers, and a `job_part` junction table.

This makes the structure more reliable and represents the relationships more clearly.

Evidence: [contract.py](contract.py) · [contract-ddl.sql](contract-ddl.sql) · [contract-notes.md](contract-notes.md)

**Important limitation:** The generated schema describes the improved design; it does not automatically clean or migrate the original `legacy.db`. Existing invalid data must be handled before migration. SQLite foreign-key enforcement must also be enabled on each connection.

## Main Takeaways

- Primary keys identify records uniquely.
- Foreign keys help prevent references to records that do not exist.
- A junction table is the proper way to represent a many-to-many relationship.
- Data types and constraints matter because they affect the reliability of queries and calculations.
- Application validation and database constraints serve different purposes and can work together.

## Final Reflection

This module helped me understand why it is important to check both the data and the schema. SQL queries helped me discover the actual problems, while the improved design showed how those problems could be prevented in a better database structure.

## Reflection 2
[Reflection 2](/Reflections/ref02.md)


