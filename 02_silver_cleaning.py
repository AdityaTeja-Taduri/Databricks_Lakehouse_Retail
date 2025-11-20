# Databricks notebook source
from pyspark.sql.functions import *

bronze_df = spark.read.table("workspace.bronze.retail_orders_bronze")

print("Bronze row count:", bronze_df.count())
bronze_df.printSchema()

display(bronze_df.limit(10))


# COMMAND ----------

from pyspark.sql.types import *

bronze_df = spark.read.table("workspace.bronze.retail_orders_bronze")

# 1) Cast to proper types
typed_df = (
    bronze_df
    .withColumn("order_id",      col("order_id").cast("long"))
    .withColumn("customer_id",   col("customer_id").cast("long"))
    .withColumn("product_id",    col("product_id").cast("long"))
    .withColumn("quantity",      col("quantity").cast("int"))
    .withColumn("unit_price",    col("unit_price").cast("double"))
    .withColumn("discount_pct",  col("discount_pct").cast("double"))
    .withColumn("gross_amount",  col("gross_amount").cast("double"))
    .withColumn("order_ts",      col("order_ts").cast("timestamp"))
)

# 2) Filter out bad / incomplete rows
clean_df = (
    typed_df
    # drop rows missing key identifiers
    .na.drop(subset=["order_id", "customer_id", "product_id", "order_ts"])
    # quantity and price must be positive
    .filter(col("quantity") > 0)
    .filter(col("unit_price") > 0)
    # discount between 0 and 1 (0–100%)
    .filter((col("discount_pct") >= 0) & (col("discount_pct") <= 1))
)

# 3) Add useful derived columns
silver_df = (
    clean_df
    .withColumn("order_date", to_date("order_ts"))
    .withColumn("net_amount", col("gross_amount") * (1 - col("discount_pct")))
    .withColumn("ingest_ts", current_timestamp())
)

print("Silver row count:", silver_df.count())
silver_df.printSchema()
display(silver_df.limit(10))


# COMMAND ----------

silver_table = "workspace.silver.retail_orders_silver"

(
    silver_df.write
        .format("delta")
        .mode("overwrite")
        .saveAsTable(silver_table)
)

print("Silver table created:", silver_table)


# COMMAND ----------

sdf = spark.read.table("workspace.silver.retail_orders_silver")

print("Silver rows:", sdf.count())
display(sdf.groupBy("category").agg(count("*").alias("orders")).orderBy(desc("orders")).limit(10))
