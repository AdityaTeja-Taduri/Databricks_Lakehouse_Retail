# Databricks Lakehouse Retail ETL Pipeline  
_End-to-end Bronze → Silver → Gold pipeline with Auto Loader, Delta Lake, and Unity Catalog_

## 🚀 Overview

This project implements a complete **Lakehouse ETL pipeline** on Databricks Free Edition using:

- Unity Catalog (catalog: `workspace`)
- Managed Volumes (`/Volumes/workspace/bronze/raw_retail`)
- Auto Loader (`cloudFiles`)
- Delta Lake
- Bronze → Silver → Gold medallion architecture

The pipeline processes a **100,000-row synthetic retail dataset** generated inside Databricks to simulate a production landing zone of multi-file CSV data.

---

## 🧱 Architecture

**Flow:**

1. **RAW (Volume)**  
   - Synthetic retail dataset generated with PySpark  
   - Written as ~20 CSV files to  
     `/Volumes/workspace/bronze/raw_retail`

2. **BRONZE – Auto Loader**  
   - Auto Loader (`cloudFiles`) reads from the volume  
   - Infers schema, tracks files via checkpoint and schema locations  
   - Writes a Delta table:  
     `workspace.bronze.retail_orders_bronze`

3. **SILVER – Cleaning & Enrichment**  
   - Enforces data types  
   - Filters invalid rows (negative quantity/price, invalid discounts, null keys)  
   - Adds derived fields (`order_date`, `net_amount`, `ingest_ts`)  
   - Writes a cleaned Delta table:  
     `workspace.silver.retail_orders_silver`

4. **GOLD – Business Marts**  
   - Aggregates from Silver into multiple Gold tables:  
     - `workspace.gold.daily_sales`  
     - `workspace.gold.top_categories`  
     - `workspace.gold.customer_lifetime_value`

---

## 📂 Repo Structure

```text
databricks-lakehouse-retail/
│
├── notebooks/
│   ├── 00_generate_retail_raw.py        # Generate 100k synthetic retail orders
│   ├── 01_bronze_autoloader.py          # Auto Loader → Bronze Delta table
│   ├── 02_silver_cleaning.py            # Cleaning / validation → Silver Delta
│   └── 03_gold_business.py              # Gold business tables (daily sales, CLV, etc.)
│
├── sql/
│   ├── daily_sales_view.sql             # View over gold.daily_sales
│   ├── top_categories_view.sql          # View over gold.top_categories
│   └── customer_ltv_view.sql            # View over gold.customer_lifetime_value
│
├── screenshots/
│   ├── catalog_structure.png            # UC tree: workspace → bronze/silver/gold
│   ├── bronze_preview.png               # Preview of bronze table
│   ├── silver_preview.png               # Preview of silver table
│   ├── gold_preview.png                 # Preview of gold tables
│   ├── architecture_diagram.png         # Visual architecture
│
├── architecture/
│   └── lakehouse_diagram.png
│
└── README.md
