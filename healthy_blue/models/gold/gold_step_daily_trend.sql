SELECT
    strftime('%Y-%m', recorded_date) AS month_of_the_year,
    SUM("count") AS total_steps,
    AVG(speed) AS average_speed,
    SUM(distance) AS total_distance,
    AVG(calorie) AS total_calories_burned,
    AVG(calorie) AS average_calories_burned
FROM
    silver_step_daily_trend
GROUP BY
    month_of_the_year
ORDER BY
    month_of_the_year