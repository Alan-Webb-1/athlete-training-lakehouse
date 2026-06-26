\# Terraform Infrastructure



This folder contains Terraform configuration for the Athlete Training Lakehouse project.



\## Purpose



The Terraform configuration defines an AWS S3 bucket to serve as the cloud landing zone for raw GPX files and processed lakehouse outputs.



\## S3 Layout



```text

s3://athlete-training-lakehouse/

├── raw/

│   └── gpx/

├── bronze/

├── silver/

├── gold/

└── logs/

