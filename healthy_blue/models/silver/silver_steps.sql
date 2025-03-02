-- Would prefer agg instead of distinct, could be losing data: SUM(count), where clause, to get certain soure type: Need to understand what it is. Might be supporting data, take AVG in that case. Make informed dec if you can't find out
SELECT DISTINCT
    DATE(datetime(day_time / 1000, 'unixepoch')) AS recorded_date, 
    "count", 
    speed, 
    distance, 
    calorie
FROM
    {{ref('bronze_steps')}}

