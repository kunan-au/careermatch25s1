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
  description = "IAM Role ARN to assign to Lambda"
  type        = string
}

variable "lambda_s3_bucket" {
  description = "S3 bucket where the Lambda ZIP is stored"
  type        = string
}

variable "lambda_s3_key" {
  description = "S3 key (path) for the Lambda ZIP file"
  type        = string
}

variable "glue_job_name" {
  description = "Name of the AWS Glue job triggered by Lambda"
  type        = string
}
