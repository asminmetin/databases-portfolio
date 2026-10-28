.echo on
DROP INDEX IF EXISTS ix_job_tech;

-- BEFORE the index
EXPLAIN QUERY PLAN SELECT * FROM maint_job WHERE technician = 'Beier';
EXPLAIN QUERY PLAN SELECT * FROM machine WHERE machine_name = 'cnc-02';
EXPLAIN QUERY PLAN SELECT * FROM maint_job WHERE technician LIKE '%ei%';

CREATE INDEX ix_job_tech ON maint_job(technician);

-- AFTER the index
EXPLAIN QUERY PLAN SELECT * FROM maint_job WHERE technician = 'Beier';
EXPLAIN QUERY PLAN SELECT * FROM machine WHERE machine_name = 'cnc-02';
EXPLAIN QUERY PLAN SELECT * FROM maint_job WHERE technician LIKE '%ei%';

-- BREAK IT: my own WHERE clauses that defeat the index
EXPLAIN QUERY PLAN SELECT * FROM maint_job WHERE technician = 'Beier';