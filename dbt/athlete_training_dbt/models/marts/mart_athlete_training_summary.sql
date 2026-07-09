with weekly_training as (

    select *
    from {{ ref('int_weekly_training') }}

),

athlete_summary as (

    select
        athlete_id,
        athlete_name,

        count(distinct week_start_date) as active_training_weeks,
        sum(total_activities) as total_activities,
        round(sum(total_miles), 2) as total_miles,
        round(sum(total_duration_minutes), 2) as total_duration_minutes,
        round(sum(total_elevation_gain_feet), 2) as total_elevation_gain_feet,
        round(avg(total_miles), 2) as avg_weekly_miles,
        round(avg(total_activities), 2) as avg_weekly_activities,
        round(max(longest_run_miles), 2) as longest_run_miles

    from weekly_training
    group by
        athlete_id,
        athlete_name

)

select *
from athlete_summary