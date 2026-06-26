terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_s3_bucket" "athlete_training_lakehouse" {
  bucket = var.bucket_name

  tags = {
    Project     = "athlete-training-lakehouse"
    Environment = var.environment
    Owner       = "Alan Webb"
  }
}

resource "aws_s3_bucket_versioning" "athlete_training_lakehouse_versioning" {
  bucket = aws_s3_bucket.athlete_training_lakehouse.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "athlete_training_lakehouse_encryption" {
  bucket = aws_s3_bucket.athlete_training_lakehouse.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_object" "raw_gpx_prefix" {
  bucket  = aws_s3_bucket.athlete_training_lakehouse.id
  key     = "raw/gpx/"
  content = ""
}

resource "aws_s3_object" "bronze_prefix" {
  bucket  = aws_s3_bucket.athlete_training_lakehouse.id
  key     = "bronze/"
  content = ""
}

resource "aws_s3_object" "silver_prefix" {
  bucket  = aws_s3_bucket.athlete_training_lakehouse.id
  key     = "silver/"
  content = ""
}

resource "aws_s3_object" "gold_prefix" {
  bucket  = aws_s3_bucket.athlete_training_lakehouse.id
  key     = "gold/"
  content = ""
}

resource "aws_s3_object" "logs_prefix" {
  bucket  = aws_s3_bucket.athlete_training_lakehouse.id
  key     = "logs/"
  content = ""
}