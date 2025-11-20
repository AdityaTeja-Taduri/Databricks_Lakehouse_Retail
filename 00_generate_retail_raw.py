# Databricks notebook source
from pyspark.sql.functions import *
import pyspark.sql.functions as F

raw_path = "/Volumes/workspace/bronze/raw_retail"

N = 100000  # number of rows

# Generate realistic retail data
df = (
    spark.range(N)
    .withColumn("order_id", col("id") + 1)
    .withColumn("customer_id", (rand() * 5000 + 1).cast("int"))
    .withColumn("product_id", (rand() * 500 + 1).cast("int"))
    .withColumn(
        "category",
        element_at(
            array(
                lit("Electronics"),
                lit("Clothing"),
                lit("Sports"),
                lit("Home"),
                lit("Books"),
                lit("Beauty"),
            ),
            (rand() * 6 + 1).cast("int"),
        ),
    )
    .withColumn("quantity", (rand() * 4 + 1).cast("int"))
    .withColumn("unit_price", round(rand() * 180 + 20, 2))
    .withColumn("discount_pct", round(rand() * 0.3, 2))
    .withColumn("gross_amount", col("quantity") * col("unit_price"))
    .withColumn(
        "order_ts",
        timestamp_seconds(
            1704067200 + (rand() * 60 * 60 * 24 * 180).cast("int")
        ),
    )
    .drop("id")
)

# Write ~20 CSV files
(
    df.repartition(20)
      .write
      .mode("overwrite")
      .option("header", True)
      .csv(raw_path)
)

print("RAW retail data generated at:", raw_path)


# COMMAND ----------

display(dbutils.fs.ls(raw_path))