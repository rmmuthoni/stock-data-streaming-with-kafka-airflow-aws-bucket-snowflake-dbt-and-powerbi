# Stock Market Data Streaming

An end-to-end data engineering project that streams stock market data from the Finnhub API, stages it in MinIO, loads it into Snowflake, transforms it with dbt, and visualizes curated datasets in Power BI. Apache Airflow orchestrates the pipeline.

## Project overview

This project demonstrates a complete path from source data to analytics. Raw market data is collected from Finnhub and stored in MinIO, an S3-compatible object store. The data is then loaded into Snowflake and transformed into bronze, silver, and gold layers using a medallion architecture. Power BI connects to the gold datasets for reporting and visualization.

## Background

Stock market data can be valuable for analysis when it is collected reliably, retained in a staging layer, and organized into datasets that are ready for reporting. This project brings together API ingestion, object storage, a cloud data warehouse, transformation tooling, orchestration, and business intelligence in one workflow.

## Objectives

- Retrieve stock market data from the Finnhub API.
- Store raw ingested data in MinIO buckets.
- Load staged data into Snowflake.
- Apply medallion-style transformations with dbt.
- Publish gold-layer datasets for Power BI.
- Schedule and coordinate pipeline tasks with Apache Airflow.

## Architecture and data flow

<img width="1703" height="860" alt="Stock Streaming Architecture" src="https://github.com/user-attachments/assets/445df950-8676-4351-a07b-dac96ba7cb36" />


1. Airflow schedules the ingestion workflow.
2. The pipeline retrieves data from Finnhub and stages it in MinIO.
3. Staged data is loaded into Snowflake.
4. dbt models transform warehouse data through bronze, silver, and gold layers.
5. Power BI uses the gold datasets for visualization and reporting.

## Project dependencies

| Dependency | Purpose | Configuration needed |
| --- | --- | --- |
| Finnhub API | Stock market data source | API key and endpoint settings |
| MinIO | S3-compatible data staging | Endpoint, bucket, and access credentials |
| Snowflake | Data warehouse | Account, warehouse, database, schema, and credentials |
| dbt | Warehouse transformations | Project configuration and Snowflake connection |
| Apache Airflow | Scheduling and orchestration | Airflow environment and connections/secrets |
| Power BI | Reporting and visualization | Access to the Snowflake gold datasets |

## Technologies

- **Finnhub API** — market data source
- **MinIO** — S3-compatible object storage
- **Snowflake** — cloud data warehouse
- **dbt** — data modeling and medallion transformations
- **Apache Airflow** — workflow orchestration
- **Power BI** — dashboards and visualizations


# Stock Quotes Transformation Layer

This dbt project transforms raw stock quote data in Snowflake into structured, analytics-ready datasets for downstream analysis and visualization in a BI tool. Source records arrive as semi-structured JSON, including Snowflake `VARIANT` values, and are refined through Bronze, Silver, and Gold layers.

## Data flow

```text
Raw JSON / VARIANT → Bronze → Silver → Gold → BI
```

| Layer | Purpose |
| --- | --- |
| **Bronze** | Keeps a source-aligned replica of the raw data as-is, preserving the original JSON structure and values for traceability. |
| **Silver** | Extracts and structures fields, casts values to appropriate data types, renames columns consistently, and cleans or standardizes data. |
| **Gold** | Applies business logic and produces analytics-oriented datasets, such as daily stock summaries and weekly or monthly snapshots. |

The layers separate raw-data preservation, data quality and standardization, and business-specific reporting logic. Gold models are intended to be consumed by BI dashboards and other analytical workflows.

Each layer's schemas and models are tested against defined expectations, including checks for required fields, valid values, and data quality rules. These tests help catch unexpected changes and ensure the datasets meet their intended contracts before downstream use.

## Snowflake and dbt

Snowflake is the project warehouse. dbt models transform the source data in Snowflake, including extracting fields from `VARIANT` data and building progressively refined models for each layer.

## Example model organization

```text
models/
├── bronze/   # Raw, source-aligned data
├── silver/   # Typed, renamed, and cleaned data
└── gold/     # Business logic and reporting datasets
```

Model names, business rules, and the precise definitions of daily, weekly, and monthly outputs should follow the project's requirements.
