variable "glue_job_name" {
  type        = string
  default     = "glue-etl-to-rds"
  description = "Logical name for the Glue job"
}

variable "glue_script_name" {
  type        = string
  description = "Name of the script used for the Glue job"
}

variable "glue_script_path" {
  type        = string
  description = "S3 key for the ETL script"
}

variable "s3_bucket_name" {
  type        = string
  description = "S3 bucket where the Glue script is stored"
}

variable "s3_raw_data_path" {
  type        = string
  description = "S3 path where raw data is stored"
}

variable "s3_curated_path" {
  type        = string
  description = "S3 path where curated data is stored"
}

variable "s3_temp_path" {
  type        = string
  description = "S3 path for Glue temporary storage"
  default     = "temp/"
}

variable "rds_endpoint" {
  type        = string
  description = "RDS endpoint for the Glue script"
}

variable "rds_username" {
  type        = string
  description = "RDS username for the Glue script"
}

variable "rds_password" {
  type        = string
  description = "RDS password for the Glue script"
}

variable "rds_database" {
  type        = string
  description = "RDS DB name"
}

variable "glue_role_arn" {
  type        = string
  description = "IAM role ARN used by Glue"
}

variable "environment" {
  type        = string
  description = "Environment (e.g. dev, staging, prod)"
}
