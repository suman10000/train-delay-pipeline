
SELECT
    route_id,
    COUNT(*) AS observation_count,
    ROUND(AVG(arrival_delay_seconds), 2)
        AS average_predicted_delay_seconds
FROM fact_prediction_observation AS f
JOIN dim_trip AS t
    ON f.trip_id = t.trip_id
WHERE arrival_delay_seconds IS NOT NULL
GROUP BY route_id
ORDER BY average_predicted_delay_seconds DESC;
