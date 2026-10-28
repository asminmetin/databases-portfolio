# Reflection 02 — Database Schema Audit

## Take-away

I learned that a database can contain relationships that are not properly defined or enforced. My advice to my past self would be to check the data with SQL queries instead of assuming the schema is correct.

## What was good?

The integrity-checking queries worked well because they showed actual problems, such as duplicate part numbers and maintenance jobs referencing machines that do not exist. This made it easier to understand why primary keys and foreign keys are important.

## What was difficult?

Understanding the cardinalities was difficult because the legacy database had almost no constraints. The `parts_used` column was especially confusing because several part numbers were stored in a single cell instead of separate rows.

## Exploration and show stoppers

I found it interesting that a simple join could miss a maintenance job when its parts were stored as a comma-separated list. How to handle inconsistent legacy data before migrating it into a corrected schema was confusing.

## Interaction with peers and instructors

I was unable to attend the class because I was sick, so I could not work directly with my classmates or ask questions during the session. I worked through the exercises independently.

## How did you verify AI suggestions?

I used AI to help understand the schema and write SQL queries. I checked the suggestions against the actual database results.

## Help and extra work

Again, I used AI's help as a learning aid to understand the queries and document the schema problems. I have not yet presented my findings or discussed them with classmates because I missed the session due to sickness.