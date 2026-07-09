from pyspark.sql import SparkSession
from pyspark.sql.functions import count, sum, avg, round

spark = SparkSession.builder.getOrCreate()

df = spark.table("workspace.athlete_training_lakehouse.activities_silver")

gold_df = (
    df.groupBy("athlete_id")
    .agg(
        count("*").alias("total_activities"),
        round(sum("distance_miles"), 2).alias("total_miles"),
        round(avg("distance_miles"), 2).alias("avg_distance_miles"),
        round(avg("duration_minutes"), 2).alias("avg_duration_minutes"),
        round(sum("elevation_gain_feet"), 2).alias("total_elevation_gain_feet")
    )
)

gold_df.write.mode("overwrite").format("delta").saveAsTable(
    "workspace.athlete_training_lakehouse.athlete_training_summary_phase6"
)

print("Gold aggregation complete")
print(f"Rows written: {gold_df.count()}")