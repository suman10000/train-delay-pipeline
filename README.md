# Train Delay Analytics Data Engineering Pipeline

## Overview

This project builds a data engineering pipeline that collects train prediction data from the MBTA V3 API, validates incoming records, transforms the raw data into a structured format, and prepares it for analytical queries.

The project focuses on core data engineering concepts, including API ingestion, data validation, JSON processing, timestamp handling, transformation logic, SQL data modelling, automated testing, and reliable error handling.

## Project Objectives

- Ingest train prediction data from a public REST API.
- Store timestamped raw JSON snapshots for traceability.
- Validate incoming API responses before processing.
- Transform nested JSON records into structured analytical datasets.
- Calculate arrival delay in seconds when both predicted and scheduled arrival times are available.
- Design a relational schema for storing prediction observations.
- Develop SQL queries for delay analysis.
- Test data validation and transformation logic.

## Technology Stack

- **Language:** Python
- **API Integration:** REST API, Requests
- **Data Format:** JSON
- **Data Validation and Testing:** Pytest
- **Data Modelling and Analytics:** SQL
- **Version Control:** Git and GitHub
- **Planned Extensions:** PostgreSQL, Apache Airflow, PySpark, AWS S3, and a dashboard

## Data Source

The project uses the [MBTA V3 API](https://www.mbta.com/developers/v3-api), a public API providing transit information.

The current ingestion configuration targets predictions for the `CR-Fitchburg` commuter rail route and requests associated schedule records.

**Important:** Prediction records represent predicted service times, not necessarily actual arrival times. The calculated delay in this project is the difference between a predicted arrival time and its associated scheduled arrival time.

## Pipeline Architecture

Current workflow:

1. **Data Ingestion:** Fetch prediction records from the MBTA API.
2. **Raw Storage:** Save timestamped JSON snapshots under `data/raw/`.
3. **Data Validation:** Check the API response structure and required record fields.
4. **Data Transformation:** Extract relevant fields from nested JSON and associate predictions with schedule records.
5. **Processed Storage:** Save transformed records as JSON under `data/processed/`.
6. **SQL Modelling:** Define relational tables and an analytical query for average arrival delay.
7. **Automated Testing:** Verify validation, transformation, and API retry behaviour.

Planned workflow extensions include PostgreSQL loading, workflow orchestration with Airflow, distributed processing with PySpark, and cloud storage using AWS S3.

## Project Structure

```text
train-delay-data-engineering-pipeline/
├── data/
│   ├── raw/                    # Raw API snapshots
│   └── processed/              # Transformed JSON records
├── scripts/
│   ├── check_data_source.py    # Initial API connectivity check
│   ├── run_ingestion.py        # Runs the ingestion pipeline
│   └── inspect_raw_data.py     # Inspects a raw snapshot
├── src/
│   ├── api_client.py           # API requests and retry handling
│   ├── ingestion.py            # Ingestion and raw snapshot storage
│   ├── validation.py           # API payload validation
│   └── transformations.py      # Transformation and delay calculation
├── sql/
│   ├── schema.sql              # Relational database schema
│   └── analytics.sql           # Delay analysis query
├── tests/
│   ├── test_api_client.py      # API client tests
│   ├── test_validation.py      # Payload validation tests
│   └── test_transformations.py # Transformation tests
├── .gitignore
├── requirements.txt
└── README.md
```

## Implemented Features

### 1. API Ingestion

- Retrieves train prediction data through HTTP requests.
- Uses request timeouts to avoid waiting indefinitely.
- Implements retry handling for transient request failures and selected HTTP status codes.
- Logs ingestion activity and errors.

### 2. Raw Data Storage

- Saves API responses as timestamped JSON snapshots.
- Records metadata such as the source, endpoint, ingestion timestamp, and record count.
- Preserves the original payload for later inspection and reprocessing.

### 3. Data Validation

- Checks that the API response is a dictionary containing a `data` list.
- Verifies that individual records have the expected structure.
- Rejects malformed payloads before transformation.

### 4. Data Transformation

- Extracts prediction, trip, stop, route, and schedule identifiers.
- Parses predicted and scheduled arrival and departure timestamps.
- Normalizes valid timestamps to UTC.
- Calculates arrival delay in seconds when both arrival timestamps are available.
- Handles missing or invalid timestamps without calculating an invalid delay.
- Saves transformed records as JSON files.

### 5. SQL Data Modelling

The SQL schema defines:

- `dim_route` — route identifiers.
- `dim_stop` — stop identifiers.
- `dim_trip` — trip identifiers and their associated routes.
- `fact_prediction_observation` — timestamped prediction observations and related schedule information.

The fact table uses a composite primary key consisting of `prediction_id` and `ingested_at`, allowing the same prediction to be represented in multiple ingestion snapshots.

The analytical SQL query calculates average non-null predicted arrival delays by route.

**Current limitation:** The SQL schema and query have been defined, but the pipeline does not yet load transformed records into PostgreSQL. The dimension tables must also be populated before the analytical query can run against a populated database.

## Setup and Installation

### Prerequisites

- Python 3.10 or later
- Git
- Internet access to reach the MBTA API

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/train-delay-data-engineering-pipeline.git
cd train-delay-data-engineering-pipeline
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a virtual environment

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

## Running the Pipeline

### Step 1: Check API connectivity

```bash
python scripts/check_data_source.py
```

This checks whether the configured API endpoint can return prediction data.

### Step 2: Run ingestion

```bash
python scripts/run_ingestion.py
```

A successful run should save a raw JSON snapshot in `data/raw/`.

### Step 3: Inspect the raw snapshot

```bash
python scripts/inspect_raw_data.py
```

This displays information about the latest raw snapshot and sample records.

### Step 4: Transform the raw data

```bash
python -m src.transformations
```

A successful run should create a transformed JSON file under `data/processed/`.

The transformation depends on the structure of the actual API response. Missing schedule relationships or timestamps can result in null fields or unavailable delay calculations.

### Step 5: Run the tests

```bash
python -m pytest -v
```

The test suite covers payload validation, API client behaviour, retry handling, and transformation logic.

## Analytical Use Cases

Once the database loading and reporting stages are implemented, the dataset can support questions such as:

- Which routes have the highest average predicted arrival delay?
- How do predicted delays vary across ingestion snapshots?
- Which trips or stops frequently have larger predicted delays?
- How do prediction records change over time?

These analyses concern predicted delays unless actual arrival data is added from a suitable source.

## Current Limitations

- The pipeline currently processes the latest raw snapshot rather than maintaining a complete historical processing workflow.
- PostgreSQL integration and automated database loading are not yet implemented.
- Airflow orchestration, PySpark processing, and AWS S3 storage are planned extensions.
- No streaming or change data capture (CDC) implementation is included yet.
- Delay calculations depend on the availability and correctness of the associated schedule timestamps.
- The average-delay query requires populated dimension and fact tables.

## Future Enhancements

1. Load transformed records into PostgreSQL.
2. Implement idempotent loading, duplicate handling, and data integrity checks.
3. Add historical processing across multiple snapshots.
4. Introduce Apache Airflow for scheduling, orchestration, and failure monitoring.
5. Use PySpark for scalable data transformation.
6. Move raw and processed datasets to AWS S3 using a Bronze–Silver–Gold layout.
7. Add data quality checks, structured logging, and pipeline monitoring.
8. Build a dashboard to explore route-level and time-based delay trends.
9. Evaluate streaming ingestion and other distributed data technologies where they add value.

## Learning Outcomes

This project provides practical experience with API-based data ingestion, raw data preservation, data validation, JSON transformation, timestamp normalization, basic analytical modelling, SQL, automated testing, and version control.

As the planned components are implemented, the project will expand into a more complete data engineering workflow.

## Disclaimer

This is an independent learning project using publicly accessible transit data. API availability, returned fields, and schedule relationships may vary. Results should be interpreted as predicted arrival delays, not verified real-world service delays.
