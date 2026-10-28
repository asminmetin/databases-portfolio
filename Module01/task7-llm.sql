SELECT
    machine,
    AVG(spindle_load) AS avg_overnight_load
FROM readings
WHERE CAST(strftime('%H', ts) AS INTEGER) >= 18
GROUP BY machine
ORDER BY avg_overnight_load DESC;