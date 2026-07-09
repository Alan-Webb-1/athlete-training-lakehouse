with activities as (

    select *
    from {{ ref('stg_activities') }}

),

weekly_training as (

    select
        athlete_id,
        athlete_name,
        date_trunc('week', activity_date) as week_start_date,

        count(activity_id) as total_activities,
        round(sum(distance_miles), 2) as total_miles,
        round(sum(duration_minutes), 2) as total_duration_minutes,
        round(sum(elevation_gain_feet), 2) as total_elevation_gain_feet,
        round(avg(distance_miles), 2) as avg_distance_miles,
        round(avg(duration_minutes), 2) as avg_duration_minutes,
        round(max(distance_miles), 2) as longest_run_miles

    from activities
    group by
        athlete_id,
        athlete_name,
        date_trunc('week', activity_date)

)

select *
from weekly_training