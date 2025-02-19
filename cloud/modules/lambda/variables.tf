variable "lambda_function_name" {
  description = "Name of the Lambda function"
  type        = string
  default     = "trigger-glue-etl"
}

variable "lambda_handler" {
  description = "Handler for the Lambda function"
  type        = string
  default     = "lambda_function.lambda_handler"
}

variable "lambda_runtime" {
  description = "Runtime environment for Lambda"
  type        = string
  default     = "python3.9"
}

variable "lambda_role_arn" {
  description = "IAM Role ARN for the Lambda function"
  type        = string
}

variable "lambda_s3_bucket" {
  description = "S3 bucket where Lambda code is stored"
  type        = string
}

variable "lambda_s3_key" {
  description = "S3 key (path) for the Lambda ZIP file"
  type        = string
}

variable "glue_job_name" {
  description = "AWS Glue Job Name"
  type        = string
}

variable "glue_role_arn" {
  description = "IAM Role ARN for AWS Glue"
  type        = string
}

variable "s3_bucket_name" {
  description = "S3 bucket for storing ETL scripts"
  type        = string
}

variable "glue_script_path" {
  description = "Path of the Glue script in S3"
  type        = string
}

variable "s3_temp_path" {
  description = "Temporary S3 storage path for Glue"
  type        = string
}

variable "s3_raw_data_path" {
  description = "S3 path where raw data is stored"
  type        = string
}

variable "s3_curated_path" {
  description = "S3 path for curated data"
  type        = string
}

variable "lambda_role_name" {
  type        = string
  description = "IAM Role Name for Lambda"
}

variable "unique_suffix" {
  type        = string
  description = "Random suffix for unique resource names"
}