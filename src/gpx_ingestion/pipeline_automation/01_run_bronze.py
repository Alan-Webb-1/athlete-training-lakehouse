from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

source_path = "s3://athlete-training-lakehouse-alan-webb-2026/bronze/sample_activity_summary.csv"

df = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(source_path)
)

df.write.mode("overwrite").format("delta").saveAsTable(
    "athlete_training_lakehouse.bronze.activities_bronze"
)

print("Bronze load complete")
print(f"Rows loaded: {df.count()}")