variable "aws_region" {
  description = "AWS region where the S3 bucket will be created"
  type        = string
  default     = "us-east-1"
}

variable "bucket_name" {
  description = "Name of the S3 bucket for the athlete training lakehouse"
  type        = string
  default     = "athlete-training-lakehouse-alan-webb-2026"
}

variable "environment" {
  description = "Project environment"
  type        = string
  default     = "dev"
}