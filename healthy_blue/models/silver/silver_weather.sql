SELECT
    strftime('%Y-%m-%d', time) as recorded_date,
    location,
    tavg as average_temperature,
    tmin as minimum_temperature,
    tmax as maximum_temperature,
    prcp as precipitation,
    snow,
    wdir as wind_direction,
    wspd as wind_speed,
    wpgt as wind_gust_speed,
    pres as pressure,
    tsun as sunshine_duration
FROM 
    {{ref('bronze_weather')}}