# Reflection 03 — SQL Queries and Query Performance

## Take-away

I learned that writing a query is not enough; it is also important to understand how the database executes it. My advice to my past self would be to test queries and check the results instead of assuming they work correctly.

## What was good?

The index benchmark was useful because it showed me that an index does not always make a query faster. I also learned how to use `EXPLAIN QUERY PLAN` to understand what SQLite does when executing a query.

## What was difficult?

Understanding why some indexes were not helpful was difficult. It was also challenging to translate a SQL query into relational algebra and understand how the different operations are connected and I feel like I am still struggling with that.

## Exploration and show stoppers

I found the SQL injection exercise interesting because it showed how an apostrophe can break a query and how bound parameters prevent this problem. Testing different filters and comparing the results also helped me understand why checking query results is important.

## Interaction with peers and instructors

I attended the class and spoke with my professor about some concerns regarding my portfolio and the upcoming checkpoint. This helped me better understand what I should focus on before the checkpoint.

## How did you verify AI suggestions?

I used AI to help write and understand SQL queries and relational algebra expressions. I checked the queries against the database, compared the row counts, and used `EXPLAIN QUERY PLAN` to verify how SQLite executed them. The index benchmark also helped me see that suggestions need to be tested rather than accepted automatically.

## Help and extra work

I used AI as a learning aid to understand the tasks and organize my portfolio. I also practised the SQL injection example and compared query performance with different indexes. Preparing for the checkpoint with Gulnisa helped me review the topics and identify areas that I still need to practise.