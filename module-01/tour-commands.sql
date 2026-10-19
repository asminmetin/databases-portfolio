-- print every command into the output too
.echo on

-- SQL: create a table and add rows
CREATE TABLE reading(machine TEXT, vib REAL);
INSERT INTO reading VALUES ('cnc-01', 1.2), ('cnc-02', 2.4), ('cnc-01', 0.9);

-- what tables exist, and how was this one made?
.tables
.schema reading

-- readable columns with a header
.mode column
.headers on
SELECT machine, max(vib) AS peak FROM reading GROUP BY machine;

-- same query, now timed
.timer on
SELECT machine, max(vib) AS peak FROM reading GROUP BY machine;
