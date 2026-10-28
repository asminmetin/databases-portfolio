# Module 03 — SQL Query Plans, Relational Algebra, and Security

## 1. References

- [Relational Algebra — University of Göttingen PDF](https://www.dbis.informatik.uni-goettingen.de/Teaching/DB-WS1112/db-rel-algebra.pdf) — helped me connect selection, projection, and join to SQL.
- [SQL Order of Execution — DataCamp](https://www.datacamp.com/tutorial/sql-order-of-execution) — explains why SQL's logical execution order differs from its written order.
- [EXPLAIN QUERY PLAN — SQLite documentation](https://www.sqlite.org/eqp.html) — explains `SCAN`, `SEARCH`, and covering indexes.
- [EXPLAIN QUERY PLAN — Varsity Tutors](https://www.varsitytutors.com/practice/subjects/sql/lessons/explain-query-plan) — another simple explanation of reading query plans.
- [SQL Analysis and Tuning — LinkedIn](https://www.linkedin.com/pulse/advanced-sql-analysis-tuning-faster-applications-jmz0c/) — prompted me to look at query plans and indexes when investigating slow queries.
- [SQL Injection Prevention — OWASP](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html) — recommends parameterized queries instead of putting user input directly into SQL.
- [Use The Index, Luke](https://use-the-index-luke.com/) — explains how indexes help searches and why some conditions cannot use them efficiently.
- [Module 2 — Data Contracts and Legacy Schemas](https://github.com/iotempire/iotempire-teaching/blob/main/full-classes/hsbi-databases-10d/modules/02-data-contracts-and-legacy-schemas.md) — links this work to the `legacy.db` schema from Module 2.

## 2. What I Googled and Learned

- **Relational algebra:** `σ` filters rows (`WHERE`), `π` chooses columns (`SELECT`), and `⋈` combines related tables (`JOIN`). [Source 1](https://www.dbis.informatik.uni-goettingen.de/Teaching/DB-WS1112/db-rel-algebra.pdf)
- **Logical SQL order:** `FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY`; aliases made in `SELECT` should not be relied on in `WHERE` in portable SQL. [Source 2](https://www.datacamp.com/tutorial/sql-order-of-execution)
- **Query plans:** `SCAN` reads all rows/entries; `SEARCH` visits a subset; `COVERING` means the index already has all columns the query needs. [Source 3](https://www.sqlite.org/eqp.html)
- **Indexes:** a leading-wildcard pattern such as `LIKE '%ei%'` cannot normally seek directly to matching values using a regular B-tree index. [Source 7](https://use-the-index-luke.com/)
- **SQL injection:** bind parameters keep user input as data instead of allowing it to become SQL syntax. [Source 6](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)

## 3. Remarkable Things

- The SQL query is written starting with `SELECT`, but its logical processing starts with `FROM`.
- An index search is not always covering: SQLite may still have to fetch the other columns from the table.
- After I added an index on `maint_job(technician)`, SQLite changed that equality query from `SCAN` to `SEARCH`, but the leading-wildcard `LIKE` query still used a scan.
- My test also showed that SQLite 3.46.1 accepts a simple `SELECT` alias in `WHERE` as an extension. That is not portable SQL, so it is safer to use the original column name in `WHERE`.
- The plan explains what SQLite chose to do; a runtime alone does not explain why a query is slow. SQLite notes that the display format of `EXPLAIN QUERY PLAN` can change between versions. [Source 3](https://www.sqlite.org/eqp.html)

## 4. LLM Answers I Verified

### Prompt 1 — Explain relational algebra simply

**Answer summary:** Relational algebra describes database operations; SQL is how we write queries. Selection (`σ`) filters rows, projection (`π`) chooses columns, and join (`⋈`) combines related tables.

**Verification:** I matched `SELECT job_id, technician FROM maint_job WHERE technician = 'Beier';` to `π_job_id, technician (σ_technician='Beier' (maint_job))`. The filter and selected columns match. [Source 1](https://www.dbis.informatik.uni-goettingen.de/Teaching/DB-WS1112/db-rel-algebra.pdf)

### Prompt 2 — Translate SQL into relational algebra

**Answer summary:** Apply selection to keep jobs where `technician = 'Beier'`, then projection to keep `job_id` and `technician`.

**Verification:** I checked that the condition matches `WHERE` and the two output columns match `SELECT`. I did not run relational algebra itself because SQLite executes SQL, not algebra notation. [Source 1](https://www.dbis.informatik.uni-goettingen.de/Teaching/DB-WS1112/db-rel-algebra.pdf)

### Prompt 3 — Why does SQL evaluate `FROM` before `SELECT`?

**Answer summary:** SQL first needs to identify the tables and rows before it can form the output columns. Aggregate conditions belong in `HAVING`, after grouping, rather than in `WHERE`.

**Verification:** This query fails in SQLite because `WHERE` cannot filter on an aggregate:

```sql
SELECT technician, COUNT(*) AS job_count
FROM maint_job
WHERE COUNT(*) > 1
GROUP BY technician;
```

The corrected query uses `HAVING COUNT(*) > 1` after `GROUP BY`. [Source 2](https://www.datacamp.com/tutorial/sql-order-of-execution)

### Prompt 4 — Explain a query plan

**Answer summary:** `SCAN maint_job` means SQLite reads all rows. `SEARCH maint_job USING INDEX ix_job_tech (technician=?)` means it uses the index to find matching technician rows.

**Verification:** I ran `EXPLAIN QUERY PLAN` before and after creating `ix_job_tech` on a copy of `legacy.db`; the actual results are recorded below. [Source 3](https://www.sqlite.org/eqp.html)

### Prompt 5 — When is an index covering?

**Answer summary:** An index is covering when it contains all the columns a query needs, so SQLite does not need to fetch matching rows from the table separately.

**Verification:** In a scratch database, `SELECT a FROM t WHERE a = 1` reported `SEARCH t USING COVERING INDEX i (a=?)`; selecting `a, b` reported `SEARCH t USING INDEX i (a=?)`. [Source 3](https://www.sqlite.org/eqp.html)

### Prompt 6 — Why does `LIKE '%ei%'` not use the index efficiently?

**Answer summary:** The initial `%` means the matching text may start anywhere, so a normal B-tree index cannot seek directly to the start of the match.

**Verification:** The plan for `technician LIKE '%ei%'` remained `SCAN maint_job` after I added an index on `technician`. [Source 3](https://www.sqlite.org/eqp.html) [Source 7](https://use-the-index-luke.com/)

### Security check — SQL injection

**Answer summary:** A payload such as `' OR '1'='1' --` can change the meaning of a query if input is pasted directly into SQL text. Parameterized queries keep the input as a value.

**Verification:** I compared the advice with OWASP's guidance on prepared statements and parameterized queries. [Source 6](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)

## Task A: 
# 1-

| Query | My prediction | Why?|
| :---     | :----:   | ---:  |
| technician = 'Beier'	| SCAN | No index exists on technician yet.|
|machine_name = 'cnc-02'| SCAN | No index exists on machine_name.|

|technician LIKE '%ei%'	| SCAN | The pattern starts with %, so an ordinary index cannot seek directly to matching values.|


- Query 1
Find jobs assigned to Beier:

"SCAN maint_job" 

SQLite checks the rows in maint_job because there is no index on technician.

- Query 2
Find machine cnc-02

"SCAN machine"

SQLite checks the rows in machine because there is no index on machine_name.

- Query 3
Find technicians whose names contain “ei”

"SCAN maint_job"

SQLite checks the table because %ei% can match text with any characters before “ei”.

# 2- After the index

Actual results after adding the index

| Query | Actual Plan | Changed?|
| :---     | :----:   | ---:  |
| technician = 'Beier'	|  SEARCH maint_job USING INDEX ix_job_tech (technician=?)| Yes
|machine_name = 'cnc-02'| SCAN machine | No 
|technician LIKE '%ei%'	| SCAN maint_job |No |

Why did only the first query change?
Query 1: SQLite now uses ix_job_tech to locate matching technician names. This is a SEARCH instead of a table scan.

Query 2: We created an index on maint_job.technician, not on machine.machine_name. The machine query cannot benefit from an index on a different table and column.

Query 3: The index contains technician names in their normal stored form. Because %ei% can match anywhere within a name, an ordinary B-tree index cannot directly seek to the beginning of the matching values. SQLite still scans.

# 3-

Before adding the index, all three queries used SCAN. After creating ix_job_tech on maint_job(technician), the equality query changed to SEARCH because SQLite could look up Beier using the index. The machine query stayed a scan because it uses a different table and column. The leading-wildcard LIKE '%ei%' also stayed a scan because the match can occur anywhere in the name. Wrapping the technician column in UPPER() also produced a scan with the ordinary index.

## Task B:
- Query I chose:

SELECT *
FROM maint_job
WHERE technician = 'Beier';

- My own relational algebra attempt:

σ<sub>technician='Beier'</sub>maint_job


I used selection σ because I want only the rows where the technician is Beier.

- LLM answer:


π<sub>job_id, machine_name, technician, done_on, parts_used</sub> (σ<sub>technician='Beier'</sub>(maint_job))

My expression and the LLM's answer were equivalent. I initially used only selection, but the LLM also showed projection over all columns. I learned that projection is optional in the algebra expression when we keep every column, and no join is needed when only one table is used.

## Task C:
1. Both pods got the same expected plans. The technician query changed from SCAN to SEARCH after adding the index. The other two queries stayed SCAN.

2. An index does not help every query. LIKE '%ei%' still scans because the wildcard can match anywhere in the text.

3. We learned that SCAN is not always bad, especially for small tables. Our question for #sql-questions is how to search substrings efficiently. 


## Setup Note Questions

1- **Where do 240,000 rows come from?** No table has them. `WITH RECURSIVE n(x)` is a counter
   built inside the query: it starts at 1 and adds 1 until the 240000. The customer block
   generates 60,000 numbers but keeps only 2,000 (`x <= 2000`), which is wasteful but harmless.

2- **INSERT … SELECT with zero rows?** It inserts nothing and gives no error. With `x <= 0`
   the table stayed empty. That is why we check `COUNT(*)` after the setup.

3- **What guarantees the customer exists?** Nothing. `(x % 2000) + 1` happens to land in
   1–2000, so there are 0 orphan orders today, but no rule enforces it. Module 4 adds a
   FOREIGN KEY for that.

4- **Why build the date modifier with `||`?** `date()` expects text like `'+5 days'`, so the
   number is glued into that string. At x = 540, `540 % 540 = 0`, so the date wraps back to
   2025-01-01 (x = 539 gives 2026-06-24).

5- **What does `printf('%05d', x)` buy?** Text is compared character by character: without
   padding, `SKU-10` sorts before `SKU-2`. With padding (`SKU-00002`, `SKU-00010`) text order
   equals number order.


# Task 1

## Exact prompt:

"SQLite schema: customer(customer_id, name, city), product(product_id, sku, price), orders(order_id, customer_id, ordered_on, status), order_line(order_id, product_id, qty). Write a query that returns, for each city, the number of distinct customers and the total revenue (sum of qty*price) of orders placed in 2025, ordered by revenue descending."

## LLM's query:

EXPLAIN QUERY PLAN
SELECT
    customer.city,
    COUNT(DISTINCT customer.customer_id) AS distinct_customers,
    SUM(order_line.qty * product.price) AS total_revenue
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
ORDER BY total_revenue DESC;

## My Predictions:

- order_line: SCAN, because there is no index specifically helping the initial search.
- orders, customer, product: SEARCH by their primary keys when matching rows.
- Temporary B-trees may be needed for grouping, counting distinct customers, and sorting by revenue.

## Output:

QUERY PLAN
|--SCAN order_line
|--SEARCH orders USING INTEGER PRIMARY KEY (rowid=?)
|--SEARCH customer USING INTEGER PRIMARY KEY (rowid=?)
|--SEARCH product USING INTEGER PRIMARY KEY (rowid=?)
|--USE TEMP B-TREE FOR GROUP BY
|--USE TEMP B-TREE FOR count(DISTINCT)
`--USE TEMP B-TREE FOR ORDER BY

## Correction:

The query correctly counts distinct customers who placed orders in 2025 and calculates revenue using qty * price. The date range includes all of 2025 when dates are stored in a compatible format.

One limitation is that the JOINs are inner joins, so customers with no orders in 2025 are excluded. If the task intends to count every customer in each city, including customers with no orders, the query would need LEFT JOINs instead.


# Task 2

## Task 2: Index Benchmark — Prove It or Disprove It

### 1. Method

I used `Module03/bench.py` to benchmark the dashboard query and single-day lookup on a copy of `warehouse.db`. The script performed one warm-up and five timed runs per stage and reported the median. All measurements were taken in the same Python process and connection.

### 2. Benchmark Results

| Query / benchmark stage | Median (ms) |
|---|---:|
| Dashboard — baseline | 79.516 |
| Dashboard — after `ix_orders_ordered_on` | 79.041 |
| Dashboard — after `ix_orderline_order` | 259.785 |
| Dashboard — after `ix_orderline_product` | 255.581 |
| Single-day lookup — baseline | 2.011 |
| Single-day lookup — with date index | 0.092 |

*Note: The dashboard indexes were added cumulatively, so the later timings do not show the isolated effect of each index.*

### 3. Query Plan Evidence

**Successful index use — single-day lookup after adding `ix_orders_ordered_on`:**

```text
SEARCH orders USING INDEX ix_orders_ordered_on (ordered_on=?)
SEARCH customer USING INTEGER PRIMARY KEY (rowid=?)
```

The median decreased from 2.011 ms to 0.092 ms, making the lookup approximately 21.9 times faster.

**Negative result — dashboard after adding `ix_orders_ordered_on`:**

```text
SCAN order_line
SEARCH orders USING INTEGER PRIMARY KEY (rowid=?)
SEARCH customer USING INTEGER PRIMARY KEY (rowid=?)
SEARCH product USING INTEGER PRIMARY KEY (rowid=?)
USE TEMP B-TREE FOR GROUP BY
USE TEMP B-TREE FOR count(DISTINCT)
USE TEMP B-TREE FOR ORDER BY
```

The plan remained unchanged, and the median improved by less than 1%. The dashboard scans `order_line` and must still perform grouping, distinct counting, and sorting. Therefore, the date index does not significantly help this query at this stage.

**Another negative result — dashboard after adding `ix_orderline_order`:**

The plan changed to use `ix_orderline_order`, but the median increased to 259.785 ms. The index encouraged a different join strategy that was slower for this aggregation workload.

The product index was used by the direct `product_id` lookup, but it did not appear in the dashboard plan.

### 4. Conclusion

The benchmark showed that indexes must be tested against the specific query workload. The date index greatly improved the single-day lookup but barely affected the dashboard. The order-line index was used by the dashboard but made it slower. An index being used does not automatically mean a query will perform better.

The dashboard timings above are cumulative results; each index should also be tested independently to isolate its effect, as required by the task.

## Task 3:
### Output:

normal query       : [(1, 'Customer 1')]
apostrophe (unsafe): crashed with near "Brien": syntax error
apostrophe (safe)  : []
payload used       : "' OR '1'='1"
injection (unsafe) : [(1, 'Customer 1'), (2, 'Customer 2'), (3, 'Customer 3')] ...
injection (safe)   : []

### Why is manual escaping or filtering not a real fix?

Escaping or filtering apostrophes by hand is unreliable because SQL syntax depends on context. String values, numeric expressions and identifiers follow different rules, and encodings or database-specific behavior can create additional edge cases. A manual filter can miss cases or reject legitimate input.

Bound parameters are safer because the SQL statement and the supplied value are handled separately. The database driver binds the value as data instead of letting it become part of the SQL syntax, taking responsibility for correct handling. Placeholders bind values, not table or column names; identifiers must be fixed in the query or selected from a trusted allowlist.

## Task 4:

### 1. SQL query

```sql
SELECT
    customer.city,
    COUNT(DISTINCT customer.customer_id) AS distinct_customers,
    SUM(order_line.qty * product.price) AS total_revenue
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
ORDER BY total_revenue DESC;
```

### 2. Relational algebra

First, join the four tables step by step:

```text
J1 = customer ⋈(customer.customer_id = orders.customer_id) orders

J2 = J1 ⋈(orders.order_id = order_line.order_id) order_line

J3 = J2 ⋈(order_line.product_id = product.product_id) product
```

Next, select orders from 2025:

```text
R = σ(ordered_on ≥ '2025-01-01'
      AND ordered_on < '2026-01-01')(J3)
```

Then, group the results by city and calculate the distinct customer count and total revenue:

```text
G = γ(
    customer.city;
    COUNT(DISTINCT customer.customer_id) → distinct_customers,
    SUM(order_line.qty × product.price) → total_revenue
)(R)
```

Finally, select the required columns and sort by revenue in descending order:

```text
P = π(city, distinct_customers, total_revenue)(G)

Result = sort(total_revenue DESC)(P)
```

### 3. Does the SQL Match the Algebra?

Yes. Each operation corresponds to part of the SQL query:

- **σ (selection):** Filters orders to dates in 2025.
- **⋈ (join):** Combines customers, orders, order lines, and products using their matching IDs.
- **γ (grouping and aggregation):** Groups rows by city and calculates the distinct customer count and total revenue.
- **π (projection):** Selects the three output columns.
- **sort:** Orders the results by revenue, highest first.

The relational algebra describes the logical operations, while SQL expresses them in executable form. The database query planner may choose a different execution order without changing the intended result.
