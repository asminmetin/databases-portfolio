## What the contract does

The contract describes the corrected maintenance database. Pydantic checks data in the Python application before it is saved. SQLAlchemy describes rules for the database tables.

## Constraints enforced by Pydantic (application level)

- `Machine.machine_id` must be at least 1 (`Field(ge=1)`).
- `Machine.serial_no` must have at least 3 characters and start with `SN-`.
- `Machine.installed` and `MaintenanceJob.done_on` must be valid dates.
- `MaintenanceJob.part_nos` is a list, so the application no longer represents all parts as one comma-separated string.

These checks can give the application quick, understandable validation errors. The Pydantic model alone does not check that a `machine_id` or part number exists in the database, and it does not prevent duplicate part numbers in `part_nos`.

## Constraints enforced by the database schema (SQLAlchemy)

- Primary keys identify each machine, part, job, and job-part row.
- `machine.serial_no` is `UNIQUE`, so two machines cannot have the same serial number.
- `NOT NULL` makes required columns mandatory.
- Foreign keys connect `maint_job.machine_id` to `machine.machine_id`, and `job_part` to its job and part.
- The composite primary key `(job_id, part_no)` in `job_part` stops the same part being listed twice for the same job.
- `part.unit_price` uses `NUMERIC(9, 2)` rather than text.

## Why use both?

Pydantic validates data at the application boundary and can show friendly errors. Database constraints protect stored data even if another script or application writes to the database without using these Pydantic models.

## Important limitations

- The database schema does not itself enforce the `SN-` prefix or `machine_id >= 1`; those checks are only in Pydantic in this version.
- SQLite foreign-key enforcement must be enabled on each database connection with `PRAGMA foreign_keys = ON` for SQLite to enforce declared foreign keys.
- The `part_nos` list belongs to the application model. In the database, each job-part association is stored as a separate row in `job_part`.
- Running `contract.py` creates tables in a temporary in-memory SQLite database to print the DDL. It does not migrate or overwrite `legacy.db`.

## Emitted DDL

The generated SQL is saved in `contract-ddl.sql`. To regenerate it from the project root, run:

```bash
uv run python Module02/contract.py
```