variable "glue_role_name" {
  description = "IAM Role Name for AWS Glue"
  type        = string
}

variable "lambda_role_name" {
  description = "IAM Role Name for AWS Lambda"
  type        = string
}

variable "raw_data_bucket_arn" {
  description = "ARN of the raw data S3 bucket"
  type        = string
}

variable "curated_data_bucket_arn" {
  description = "ARN of the curated data S3 bucket"
  type        = string
}
