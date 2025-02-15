resource "aws_glue_job" "glue_etl_job" {
  name         = "glue-etl-to-rds"
  role_arn     = aws_iam_role.glue_role.arn
  glue_version = "3.0"
  timeout      = 10
  max_capacity = 2

  command {
    script_location = "s3://sandbox-analytics-${random_id.unique_suffix.hex}/glue_etl.py"
    python_version  = "3"
  }

  default_arguments = {
    "--TempDir"       = "s3://sandbox-analytics-${random_id.unique_suffix.hex}/temp/"
    "--S3_INPUT_PATH" = "s3://raw-data-${random_id.unique_suffix.hex}/data/"
    "--RDS_ENDPOINT"  = module.rds_private.rds_endpoint
    "--RDS_USER"      = var.username
    "--RDS_PASSWORD"  = random_password.private_rds_password.result
    "--RDS_DATABASE"  = var.db_name
  }
}
