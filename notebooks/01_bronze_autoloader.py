# Databricks notebook source
from pyspark.sql.functions import *

raw_path = "/Volumes/workspace/bronze/raw_retail"

bronze_table_name = "workspace.bronze.retail_orders_bronze"
schema_location   = "/Volumes/workspace/bronze/raw_retail/_schemas"
checkpoint_path   = "/Volumes/workspace/bronze/raw_retail/_checkpoints"

# Auto Loader streaming read
bronze_stream_df = (
    spark.readStream
        .format("cloudFiles")
        .option("cloudFiles.format", "csv")
        .option("header", "true")
        .option("inferSchema", "true")
        .option("cloudFiles.schemaLocation", schema_location)
        .load(raw_path)
)

# Write to Bronze Delta table
(
    bronze_stream_df.writeStream
        .format("delta")
        .option("checkpointLocation", checkpoint_path)
        .trigger(availableNow=True)
        .toTable(bronze_table_name)
)

print("Bronze table created:", bronze_table_name)


# COMMAND ----------

display(spark.read.table("workspace.bronze.retail_orders_bronze").limit(10))
