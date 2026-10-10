# Train Delay Data Engineering Pipeline

An end-to-end data engineering project that collects public commuter-rail data, preserves raw API responses, validates and transforms records, and produces analytical datasets.

## Project objectives

- Ingest schedule and prediction data from a public API.
- Preserve timestamped raw data for reproducibility.
- Build reliable data cleaning and validation workflows.
- Store raw and processed datasets in Amazon S3.
- Use PySpark for scalable transformations.
- Orchestrate the pipeline with Apache Airflow.
- Produce SQL-based train performance analytics.

## Technology stack

- Python
- REST APIs and JSON
- SQL and PostgreSQL
- Amazon S3
- PySpark
- Apache Airflow
- Git and GitHub

## Current status

Stage 1: API connectivity and raw data ingestion.

Later stages will be documented as their implementations and tests are completed.

## Data source

MBTA V3 API: https://www.mbta.com/developers/v3-api

This project is intended for learning and portfolio demonstration. Predictions are not assumed to represent actual arrival times.

## Run locally

Create and activate a Python virtual environment, install the dependencies, and run:

```powershell
python -m pip install -r requirements.txt
python scripts/check_data_source.py
```
