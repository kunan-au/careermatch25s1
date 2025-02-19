variable "glue_script_name" {
  description = "Name of the Glue job (e.g., glue-etl-to-rds)"
  type        = string
}

variable "glue_script_path" {
  description = "Path to the script in the S3 bucket (e.g., scripts/glue_etl.py)"
  type        = string
}

variable "s3_bucket_name" {
  description = "Name of the S3 bucket where the Glue script is stored"
  type        = string
}

variable "s3_raw_data_path" {
  description = "S3 path where raw data is stored"
  type        = string
}

variable "s3_curated_path" {
  description = "S3 bucket path for curated data"
  type        = string
}


variable "s3_temp_path" {
  description = "S3 path for Glue temporary storage"
  type        = string
  default     = "temp/"
}

variable "rds_endpoint" {
  description = "RDS database endpoint"
  type        = string
}

variable "rds_username" {
  description = "RDS database username"
  type        = string
}

variable "rds_password" {
  description = "RDS database password"
  type        = string
}

variable "rds_database" {
  description = "RDS database name"
  type        = string
}

variable "environment" {
  description = "Environment for tagging (e.g., dev, staging, prod)"
  type        = string
}

variable "glue_role_arn" {
  description = "IAM Role for Glue"
  type        = string
}