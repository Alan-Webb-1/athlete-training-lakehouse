select
    activity_id,
    athlete_id,
    athlete_name,
    activity_date,
    duration_minutes,
    distance_miles,
    elevation_gain_feet,
    trackpoint_count
from {{ source('silver', 'activities') }}