# Databricks notebook source
# MAGIC %md
# MAGIC # 01 Bronze Ingestion
# MAGIC
# MAGIC This notebook reads safe sample athlete training CSV data and writes it to a Bronze Delta table.
# MAGIC
# MAGIC Bronze layer goal:
# MAGIC - Preserve source data
# MAGIC - Add ingestion metadata
# MAGIC - Store data in Delta format for downstream Silver and Gold transformations

# COMMAND ----------

from pyspark.sql.functions import current_timestamp, lit

# COMMAND ----------

# Project/database name
database_name = "athlete_training_lakehouse"

# Source file path
# In Databricks, upload sample_activity_summary.csv to this path first:
# /FileStore/athlete_training_lakehouse/sample_activity_summary.csv

source_path = "/FileStore/athlete_training_lakehouse/sample_activity_summary.csv"

# Bronze table name
bronze_table_name = f"{database_name}.bronze_activity_summary"

# COMMAND ----------

# Create database if it does not exist
spark.sql(f"CREATE DATABASE IF NOT EXISTS {database_name}")

# COMMAND ----------

# Read sample CSV file into Spark DataFrame
activity_df = (
    spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(source_path)
)

# COMMAND ----------

# Add ingestion metadata
bronze_activity_df = (
    activity_df
        .withColumn("ingested_at", current_timestamp())
        .withColumn("source_system", lit("safe_sample_csv"))
        .withColumn("bronze_layer", lit("bronze_activity_summary"))
)

# COMMAND ----------

# Write to Bronze Delta table
(
    bronze_activity_df
        .write
        .format("delta")
        .mode("overwrite")
        .saveAsTable(bronze_table_name)
)

# COMMAND ----------

# Preview Bronze table
display(spark.table(bronze_table_name))

# COMMAND ----------

# Basic validation
row_count = spark.table(bronze_table_name).count()

print(f"Bronze table created successfully: {bronze_table_name}")
print(f"Rows loaded: {row_count}")