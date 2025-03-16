SELECT
    DATE(datetime(day_time / 1000, 'unixepoch')) AS recorded_date, 
    location,
    AVG("count") as "count", 
    AVG(speed) as speed, 
    AVG(distance) as distance, 
    AVG(calorie) as calorie
FROM
    {{ref('bronze_steps')}}
GROUP BY
    recorded_date

