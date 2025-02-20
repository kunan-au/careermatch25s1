variable "lambda_function_name" {
  type = string
}

variable "lambda_handler" {
  type    = string
  default = "lambda_function.lambda_handler"
}

variable "lambda_runtime" {
  type    = string
  default = "python3.9"
}

variable "lambda_role_arn" {
  type        = string
  description = "IAM role ARN used by the Lambda function"
}

variable "lambda_s3_bucket" {
  type        = string
  description = "S3 bucket containing the Lambda ZIP code"
}

variable "lambda_s3_key" {
  type        = string
  description = "S3 object key for the Lambda ZIP code"
}

variable "glue_job_name" {
  type        = string
  description = "Glue job name that this Lambda triggers"
}

variable "glue_role_arn" {
  type        = string
  description = "Glue IAM role ARN (if needed in code or environment vars)"
}

variable "glue_script_path" {
  type        = string
  description = "Glue script path in S3"
}

variable "s3_bucket_name" {
  type        = string
  description = "Analytics S3 bucket name"
}

variable "s3_raw_data_path" {
  type        = string
  description = "S3 path for raw data"
}

variable "s3_curated_path" {
  type        = string
  description = "S3 path for curated data"
}

variable "s3_temp_path" {
  type        = string
  description = "S3 path for temp data"
}

variable "unique_suffix" {
  type        = string
  description = "Random suffix if needed"
}