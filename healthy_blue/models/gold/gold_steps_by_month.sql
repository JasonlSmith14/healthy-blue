SELECT
    strftime('%Y-%m', recorded_date) AS month_of_the_year,
    CAST(SUM("count") AS INT) AS total_steps,
    AVG("count") AS average_steps,
    CAST(MAX("count") AS INT) as maximum_steps,
    AVG(speed) AS average_speed,
    MAX(speed) AS maximum_speed,
    SUM(distance) AS total_distance,
    AVG(distance) AS average_distance,
    MAX(distance) AS maximum_distance,
    SUM(calorie) AS total_calories_burned,
    AVG(calorie) AS average_calories_burned,
    MAX(calorie) AS maximum_calories_burned,
    AVG(average_temperature) AS average_temperature
FROM
    {{ref('silver_steps_and_weather')}}
GROUP BY
    month_of_the_year
ORDER BY
    month_of_the_year