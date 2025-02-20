# Create or configure your Glue Job
resource "aws_glue_job" "this" {
  name     = var.glue_job_name
  role_arn = var.glue_role_arn

  command {
    name            = "glueetl"
    python_version  = "3"
    script_location = "s3://${var.s3_bucket_name}/${var.glue_script_path}"
  }

  default_arguments = {
    "--job-bookmark-option"         = "job-bookmark-disable"
    "--TempDir"                     = "s3://${var.s3_bucket_name}/${var.s3_temp_path}/"
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-metrics"                     = "true"

    # pass in RDS connection info
    "--rds_endpoint"  = var.rds_endpoint
    "--rds_username"  = var.rds_username
    "--rds_password"  = var.rds_password
    "--rds_database"  = var.rds_database

    # pass in S3 paths
    "--raw_data_path"    = var.s3_raw_data_path
    "--curated_data_path"= var.s3_curated_path
  }

  # Just a small example, adjust to your needs
  glue_version      = "3.0"
  max_retries       = 1
  max_capacity      = 2
  execution_property {
    max_concurrent_runs = 1
  }
  tags = {
    Environment = var.environment
  }
}

# Export the job name so the caller can reference it
output "glue_job_name" {
  value = aws_glue_job.this.name
}
