resource "aws_glue_job" "glue_etl_job" {
  name     = "career-match-etl-job"
  role_arn = aws_iam_role.glue_role.arn

  command {
    script_location = "s3://${var.s3_bucket_name}/${var.glue_script_path}"
  }

  default_arguments = {
    "--job-language"   = "python"
    "--s3_raw_data_path" = "s3://${var.s3_raw_data_path}"
    "--s3_curated_path"  = "s3://${var.s3_curated_path}"
  }

  max_retries   = 2
  timeout       = 30
  glue_version  = "3.0"
}
