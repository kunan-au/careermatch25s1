resource "aws_iam_role" "glue_role" {
  name = "career-match-glue-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "glue.amazonaws.com"
      }
    }]
  })
}

resource "aws_glue_job" "glue_etl_job" {
  name     = "career-match-etl-job"
  role_arn = var.glue_role_arn  # ✅ Fix here

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
