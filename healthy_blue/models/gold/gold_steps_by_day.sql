SELECT
    recorded_date,
    "count" AS total_steps,
    speed,
    distance AS total_distance,
    calorie AS total_calories_burned,
    average_temperature, 
    minimum_temperature,
    maximum_temperature,
    precipitation, 
    wind_speed
FROM
    {{ref('silver_steps_and_weather')}}