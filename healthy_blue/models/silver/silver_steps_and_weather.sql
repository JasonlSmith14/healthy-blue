SELECT
    recorded_date,
    location,
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
    presure,
    sunshine_duration
FROM 
    {{ref('silver_steps')}} as silver_steps
LEFT JOIN 
    {{ref('silver_weather')}} as silver_weather
ON 
    silver_steps.recorded_date = silver_weather.recorded_date