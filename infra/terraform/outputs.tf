output "bucket_name" {
  description = "Name of the S3 bucket"
  value       = aws_s3_bucket.athlete_training_lakehouse.bucket
}

output "bucket_arn" {
  description = "ARN of the S3 bucket"
  value       = aws_s3_bucket.athlete_training_lakehouse.arn
}

output "raw_gpx_path" {
  description = "S3 path for raw GPX files"
  value       = "s3://${aws_s3_bucket.athlete_training_lakehouse.bucket}/raw/gpx/"
}

output "bronze_path" {
  description = "S3 path for bronze lakehouse data"
  value       = "s3://${aws_s3_bucket.athlete_training_lakehouse.bucket}/bronze/"
}

output "silver_path" {
  description = "S3 path for silver lakehouse data"
  value       = "s3://${aws_s3_bucket.athlete_training_lakehouse.bucket}/silver/"
}

output "gold_path" {
  description = "S3 path for gold analytics data"
  value       = "s3://${aws_s3_bucket.athlete_training_lakehouse.bucket}/gold/"
}