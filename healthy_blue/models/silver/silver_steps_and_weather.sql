SELECT
    silver_steps.recorded_date,
    silver_steps.location,
    "count",
    speed,
    distance,
    calorie,
    average_temperature,
    minimum_temperature,
    maximum_temperature,
    precipitation,
    snow,
    wind_direction,
    wind_speed,
    wind_gust_speed,
    pressure,
    sunshine_duration
FROM 
    {{ref('silver_steps')}} as silver_steps
LEFT JOIN 
    {{ref('silver_weather')}} as silver_weather
ON 
    silver_steps.recorded_date = silver_weather.recorded_date
AND
    silver_steps.location = silver_weather.location