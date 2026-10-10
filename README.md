# Train Delay Data Engineering Pipeline

A data engineering project that collects commuter-rail prediction data, preserves raw API responses, validates incoming records, and prepares the foundation for downstream analytics.

## Current Features

- Fetches train prediction data from the MBTA V3 API.
- Retries requests after selected network and server failures.
- Validates the structure of API responses.
- Saves timestamped JSON snapshots with ingestion metadata.
- Logs ingestion progress and failures.
- Includes automated tests for validation and API client behavior.

## Technology Stack

- Python
- REST APIs and JSON
- Requests
- pytest
- Git and GitHub

## Project Structure

```text
scripts/
    run_ingestion.py

src/
    api_client.py
    ingestion.py
    validation.py

tests/
    test_api_client.py
    test_validation.py

data/
    raw/
```

## Setup

Create a virtual environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Run the ingestion pipeline:

```powershell
python scripts/run_ingestion.py
```

Run the tests:

```powershell
python -m pytest -v
```

## Data Source

The project currently uses the MBTA V3 API to inspect commuter-rail predictions.

API documentation: https://www.mbta.com/developers/v3-api

Prediction data is not assumed to represent actual train arrival times.

## Planned Development

- Data cleaning and quality checks
- SQL data modelling and analytical queries
- Amazon S3 storage
- PySpark transformations
- Apache Airflow orchestration
- Monitoring and pipeline recovery
- Additional Hadoop ecosystem exercises

Features will be marked complete after implementation and testing.

## Limitations

The current version is an initial ingestion pipeline. It does not yet provide a production deployment, a historical actual-arrival dataset, or a verified train-delay prediction model.
