SELECT DISTINCT
    DATE(datetime(day_time / 1000, 'unixepoch')) AS recorded_date, 
    "count", 
    speed, 
    distance, 
    calorie
FROM
    {{ref('bronze_steps')}}

