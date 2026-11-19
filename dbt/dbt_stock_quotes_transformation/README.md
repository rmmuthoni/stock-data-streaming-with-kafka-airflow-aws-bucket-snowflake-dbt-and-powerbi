# Stock Quotes Transformation

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
