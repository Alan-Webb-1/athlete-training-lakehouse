# Athlete Training Lakehouse

This project turns raw GPX running files into structured athlete training data for analytics.

## Project Goal

Build a sports performance data pipeline using Python, AWS S3, Databricks, dbt, GitHub, and Terraform concepts.

## Phase 1

Parse raw GPX files into two structured datasets:

- `activities.csv` — one row per run
- `trackpoints.csv` — one row per GPS point

## Phase 1 Results

The initial Python ingestion pipeline parses raw GPX files into structured CSV outputs.

### Outputs Created

- `activities.csv`: all parsed activities, including duplicate flags
- `activities_clean.csv`: cleaned activity-level dataset excluding duplicate activities
- `trackpoints.csv`: GPS trackpoint-level dataset
- `pipeline_run_log.csv`: ingestion status log
- `validation_log.csv`: validation results for clean activity records

### Current Run Summary

- GPX files processed: 8
- Clean activities created: 7
- Duplicate activities flagged: 1
- Validation checks run: 35
- Validation checks passed: 35
- Validation checks failed: 0

### Data Quality Checks

The validation script checks:

- `distance_miles` is positive
- `duration_minutes` is positive
- `trackpoint_count` is positive
- `distance_miles` is within a reasonable running range
- `duration_minutes` is within a reasonable duration range

### Pipeline Learning

During ingestion testing, one duplicate GPX activity was detected. The parser was updated to flag duplicate activities using athlete ID, activity start time, duration, and distance. This prevents duplicate raw files from inflating weekly mileage and training load metrics.

## How to Run Phase 1

From the project root:

```bash
python src/gpx_ingestion/parse_gpx.py
python src/gpx_ingestion/validate_outputs.py
```

## Data Source

Raw GPX running files exported from Strava/Garmin.

## Phase 2: AWS S3 + Terraform Infrastructure

Phase 2 adds an infrastructure-as-code layer using Terraform.

The Terraform configuration defines an AWS S3 lakehouse-style landing zone with the following layout:

- `raw/gpx/` — raw GPX source files
- `bronze/` — parsed raw outputs
- `silver/` — cleaned and validated datasets
- `gold/` — analytics-ready tables
- `logs/` — pipeline and validation logs

This phase demonstrates exposure to AWS and Terraform-based infrastructure practices.