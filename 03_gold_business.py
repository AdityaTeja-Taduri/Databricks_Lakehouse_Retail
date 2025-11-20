# Databricks notebook source
from pyspark.sql.functions import *
from pyspark.sql.window import Window

silver_df = spark.read.table("workspace.silver.retail_orders_silver")

print("Silver rows:", silver_df.count())
silver_df.printSchema()


# COMMAND ----------

daily_sales_df = (
    silver_df
    .groupBy("order_date")
    .agg(
        countDistinct("order_id").alias("total_orders"),
        sum("quantity").alias("total_quantity"),
        sum("net_amount").alias("total_revenue"),
        avg("net_amount").alias("avg_order_value")
    )
    .orderBy("order_date")
)

display(daily_sales_df.limit(20))

daily_sales_table = "workspace.gold.daily_sales"

(
    daily_sales_df.write
        .format("delta")
        .mode("overwrite")
        .saveAsTable(daily_sales_table)
)

print("Gold table created:", daily_sales_table)


# COMMAND ----------

category_sales_df = (
    silver_df
    .groupBy("category")
    .agg(
        sum("net_amount").alias("category_revenue"),
        countDistinct("order_id").alias("orders"),
        sum("quantity").alias("units_sold")
    )
)

w = Window.orderBy(desc("category_revenue"))

top_categories_df = (
    category_sales_df
    .withColumn("revenue_rank", row_number().over(w))
    .orderBy("revenue_rank")
)

display(top_categories_df)

top_categories_table = "workspace.gold.top_categories"

(
    top_categories_df.write
        .format("delta")
        .mode("overwrite")
        .saveAsTable(top_categories_table)
)

print("Gold table created:", top_categories_table)


# COMMAND ----------

clv_df = (
    silver_df
    .groupBy("customer_id")
    .agg(
        countDistinct("order_id").alias("order_count"),
        sum("net_amount").alias("total_spend"),
        avg("net_amount").alias("avg_order_amount"),
        min("order_date").alias("first_order_date"),
        max("order_date").alias("last_order_date")
    )
    .withColumn(
        "customer_lifetime_days",
        datediff(col("last_order_date"), col("first_order_date"))
    )
    .withColumn(
        "avg_days_between_orders",
        when(col("order_count") > 1,
             col("customer_lifetime_days") / (col("order_count") - 1)
        ).otherwise(None)
    )
    .orderBy(desc("total_spend"))
)

display(clv_df.limit(20))

customer_clv_table = "workspace.gold.customer_lifetime_value"

(
    clv_df.write
        .format("delta")
        .mode("overwrite")
        .saveAsTable(customer_clv_table)
)

print("Gold table created:", customer_clv_table)


# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM workspace.gold.daily_sales ORDER BY order_date LIMIT 20;
# MAGIC
# MAGIC SELECT * FROM workspace.gold.top_categories ORDER BY revenue_rank LIMIT 10;
# MAGIC
# MAGIC SELECT * FROM workspace.gold.customer_lifetime_value ORDER BY total_spend DESC LIMIT 10;
# MAGIC