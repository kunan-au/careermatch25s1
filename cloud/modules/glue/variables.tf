variable "glue_script_name" {
  description = "Name of the Glue job (e.g., test)"
  type        = string
}

variable "glue_script_path" {
  description = "Path to the script in the S3 bucket (e.g., notebooks/test.ipynb)"
  type        = string
}

variable "s3_bucket_name" {
  description = "Name of the S3 bucket where the Glue script is stored"
  type        = string
}

variable "environment" {
  description = "Environment for tagging (e.g., dev, staging, prod)"
  type        = string
}
