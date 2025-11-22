# Databricks Lakehouse Retail ETL Pipeline

This project shows how to build a complete **Lakehouse ETL pipeline** on Databricks using the Bronze → Silver → Gold architecture.  
I used Unity Catalog, Auto Loader, Delta Lake, and Databricks Volumes to create a realistic, production-style data engineering workflow.

---

## 🛠️ Tech Stack

- **Databricks Lakehouse Platform**
- **Unity Catalog** (governance, schema management, permissions)
- **Delta Lake** (Bronze → Silver → Gold storage)
- **PySpark** (ETL transformations)
- **Auto Loader** (streaming ingestion)
- **Photon Engine** (optimized execution)
- **SQL** (views & business aggregations)
- **MLflow** (optional lineage and tracking)

---

## 🚀 What This Project Does

### 1. **Generates a retail dataset**
- Creates ~100,000 fake retail orders  
- Saves them as multiple CSV files in a Databricks Volume  
- Acts like a “raw data landing zone”

### 2. **Bronze Layer – Ingestion with Auto Loader**
- Reads the raw CSVs incrementally  
- Uses schema inference + checkpoints  
- Stores clean Delta files in the Bronze layer

### 3. **Silver Layer – Cleaning & Validation**
- Corrects datatypes  
- Removes invalid or missing records  
- Adds useful fields like `order_date`, `net_amount`, etc.

### 4. **Gold Layer – Business Tables**
Creates 3 analytics tables:
- **Daily Sales**  
- **Top Categories**  
- **Customer Lifetime Value**

---

## 📁 Repository Structure

```
databricks-lakehouse-retail/
│
├── notebooks/                       # Python versions of all notebooks
│   ├── 00_generate_retail_raw.py
│   ├── 01_bronze_autoloader.py
│   ├── 02_silver_cleaning.py
│   └── 03_gold_business.py
│
├── databricks/                      # Databricks-native notebook exports
│   ├── 00_generate_retail_raw.dbc
│   ├── 01_bronze_autoloader.dbc
│   ├── 02_silver_cleaning.dbc
│   └── 03_gold_business.dbc
│
├── sql/                             # SQL view layer 
│   ├── daily_sales_view.sql
│   ├── top_categories_view.sql
│   └── customer_ltv_view.sql
│
├── screenshots/                     # Visuals from the Databricks workspace
│   ├── catalog_structure.png
│   ├── bronze_preview.png
│   ├── silver_preview.png
│   ├── gold_preview.png
│   └── architecture_diagram.png
│
├── architecture/                    # Architecture diagram(s)
│   └── lakehouse_diagram.png
│
└── README.md                        # Main documentation file
```


---

## 🧰 Tools Used

- **Databricks (Free Edition)**
- **Unity Catalog**
- **Databricks Volumes**
- **Auto Loader (cloudFiles)**
- **Delta Lake**
- **PySpark**

---

## ▶️ How To Run This Project

1. Create the `bronze`, `silver`, and `gold` schemas in Unity Catalog.  
2. Create a Volume inside the `bronze` schema (named `raw_retail`).  
3. Run notebook **00** to generate data.  
4. Run notebook **01** to ingest data with Auto Loader.  
5. Run notebook **02** to clean the data.  
6. Run notebook **03** to produce business tables.


---

## 💼 Why This Project Matters

This project mirrors what Data Engineers do in real companies:
- Creating pipelines  
- Managing schemas  
- Cleaning real-world messy data  
- Building analytical tables  
- Organizing code in a clear project structure  

---

## 📸 Screenshots

Screenshots of the catalog, Bronze/Silver/Gold tables, and pipeline flow are included in the `screenshots/` folder.

---

## 🧱 Architecture

This project follows the Databricks Lakehouse medallion pattern:

- **Storage:** Databricks Volumes in Unity Catalog (`/Volumes/workspace/bronze/raw_retail`)
- **Bronze:** Auto Loader ingests raw CSV files into `workspace.bronze.retail_orders_bronze`
- **Silver:** Cleaning, type casting, validation, and enrichment into `workspace.silver.retail_orders_silver`
- **Gold:** Business-ready tables:
  - `workspace.gold.daily_sales`
  - `workspace.gold.top_categories`
  - `workspace.gold.customer_lifetime_value`

High-level flow:

```text
Raw CSV (Volume)
/Volumes/workspace/bronze/raw_retail
                │
                ▼
        Auto Loader (Bronze)
 workspace.bronze.retail_orders_bronze
                │
                ▼
     Cleaning & Enrichment (Silver)
 workspace.silver.retail_orders_silver
                │
                ▼
       Gold Business Marts (Gold)
   daily_sales · top_categories · customer_lifetime_value


---

