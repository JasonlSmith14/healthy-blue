SELECT DISTINCT
    CAST(TO_TIMESTAMP(day_time / 1000) AS DATE) AS recorded_date, 
    "count", 
    speed, 
    distance, 
    calorie
FROM
    {{ref('bronze_step_daily_trend')}}
