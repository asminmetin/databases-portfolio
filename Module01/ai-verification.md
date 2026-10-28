# Task 7 — LLM-assisted SQL profiling

## Prompt

> Here is my SQLite table: readings(ts TEXT, machine TEXT, temp_c REAL, vib_rms REAL, spindle_load REAL). Write a query that returns, for each machine, the average spindle load for readings taken overnight (after 18:00), ordered by average load descending.

## Model

<ChatGPT / Claude / ... — which one you used>

## Generated SQL

File: [task7-llm.sql](task7-llm.sql)

```sql
SELECT
    machine,
    AVG(spindle_load) AS avg_overnight_load
FROM readings
WHERE CAST(strftime('%H', ts) AS INTEGER) >= 18
GROUP BY machine
ORDER BY avg_overnight_load DESC;%  
```

## Run

File: [outputs/task7-run.txt](outputs/task7-run.txt)

```
machine  avg_overnight_load
-------  ------------------
cnc-03   60.4331666666667
cnc-01   60.3670486111111
cnc-02   60.3558680555556
```

## EXPLAIN QUERY PLAN

File: [outputs/task7-plan.txt](outputs/task7-plan.txt)

```
QUERY PLAN
|--SCAN readings
|--USE TEMP B-TREE FOR GROUP BY
`--USE TEMP B-TREE FOR ORDER BY
```

<one line: what SCAN readings means>

## Break attempts

Expected rows for 18:00–24:00: 6 h × 1,200 readings/h × 2 days × 3 machines = 43,200

| Filter | Rows | Expected | OK? | Why |
|---|---|---|---|---|
| LLM: `CAST(strftime('%H', ts) AS INTEGER) >= 18` | 43,200 | 43,200 | yes | This is correct since the 3rd is wrong. CAST.. AS INTEGER compares only integers. |
| `ts LIKE '%18%'` | 18,102 | 43,200 | no | it counts everything has 18 in it, not just the time. |
| `strftime('%H', ts) >= 18` | 172,800 | 43,200 | no | this command makes every number a string, when SQLite compares different types, every string is greater than integers. That's why every row is correct. |
| `ts > '2026-01-05 18:00:00'` | 129,597 | 43,200 | no | even though the comparasion is true, the command puts a specific date limitation, so it counts every time after Monday 18.00. |

## Ambiguity: 18:00–24:00 vs 18:00–06:00

<result of the 18–06 query: does the ranking change? did the model ask?>

machine  avg_load        
-------  ----------------
cnc-02   60.2053090277778
cnc-03   60.2024583333333
cnc-01   60.1848645833333


machine  avg_load        
-------  ----------------
cnc-03   60.4331666666667
cnc-01   60.3670486111111
cnc-02   60.3558680555556

## Second way

<result of the substr(ts, 12, 2) query: same as the LLM's?>

## Verification paragraph

The query returned the average spindle load for each machine, with cnc-03 having the highest average. I checked the row count and got the expected 43,200 readings. The model assumed that “overnight” means from 18:00 until midnight, but it could also mean until 06:00. The most surprising test was strftime('%H', ts) >= 18, because it returned all rows instead of only the evening readings. I fixed this by converting the hour to an integer using CAST.