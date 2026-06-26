\# Athlete Training Lakehouse



This project turns raw GPX running files into structured athlete training data for analytics.



\## Project Goal



Build a sports performance data pipeline using Python, AWS S3, Databricks, dbt, GitHub, and Terraform concepts.



\## Phase 1



Parse raw GPX files into two structured datasets:



\- `activities.csv` — one row per run

\- `trackpoints.csv` — one row per GPS point



\## Phase 1 Results



The initial Python ingestion pipeline parses raw GPX files into structured CSV outputs.



\### Outputs Created



\- `activities.csv`: all parsed activities, including duplicate flags

\- `activities\_clean.csv`: cleaned activity-level dataset excluding duplicate activities

\- `trackpoints.csv`: GPS trackpoint-level dataset

\- `pipeline\_run\_log.csv`: ingestion status log

\- `validation\_log.csv`: validation results for clean activity records



\### Current Run Summary



\- GPX files processed: 8

\- Clean activities created: 7

\- Duplicate activities flagged: 1

\- Validation checks run: 35

\- Validation checks passed: 35

\- Validation checks failed: 0



\### Data Quality Checks



The validation script checks:



\- `distance\_miles` is positive

\- `duration\_minutes` is positive

\- `trackpoint\_count` is positive

\- `distance\_miles` is within a reasonable running range

\- `duration\_minutes` is within a reasonable duration range



\### Pipeline Learning



During ingestion testing, one duplicate GPX activity was detected. The parser was updated to flag duplicate activities using athlete ID, activity start time, duration, and distance. This prevents duplicate raw files from inflating weekly mileage and training load metrics.



\## How to Run Phase 1



From the project root:



```bash

python src/gpx\_ingestion/parse\_gpx.py

python src/gpx\_ingestion/validate\_outputs.py

```



\## Data Source



Raw GPX running files exported from Strava/Garmin.

