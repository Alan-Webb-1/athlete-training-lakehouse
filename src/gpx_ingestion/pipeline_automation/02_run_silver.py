from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.getOrCreate()

df = spark.table("workspace.athlete_training_lakehouse.activities_bronze")

silver_df = (
    df
    .filter(col("distance_miles") > 0)
    .filter(col("duration_minutes") > 0)
    .filter(col("trackpoint_count") > 0)
    .filter(col("duplicate_activity_flag") == False)
    .dropDuplicates(["activity_id"])
)

silver_df.write.mode("overwrite").format("delta").saveAsTable(
    "workspace.athlete_training_lakehouse.activities_silver"
)

print("Silver transformation complete")
print(f"Rows written: {silver_df.count()}")