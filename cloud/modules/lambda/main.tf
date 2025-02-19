resource "aws_glue_job" "glue_etl_job" {
  name     = "career-match-etl"
  role_arn = var.glue_role_arn

  command {
    script_location = "s3://${var.s3_bucket_name}/${var.glue_script_path}"
    python_version  = "3"
  }

  default_arguments = {
    "--TempDir"          = "s3://${var.s3_temp_path}/tmp/"
    "--s3_raw_data_path" = "s3://${var.s3_raw_data_path}/"
    "--s3_curated_path"  = "s3://${var.s3_curated_path}/"
  }

  execution_property {
    max_concurrent_runs = 1
  }
}

resource "aws_lambda_function" "trigger_glue_lambda" {
  function_name    = var.lambda_function_name
  role            = var.lambda_role_arn
  handler        = var.lambda_handler
  runtime        = var.lambda_runtime

  s3_bucket      = var.lambda_s3_bucket
  s3_key         = var.lambda_s3_key

  environment {
    variables = {
      GLUE_JOB_NAME = var.glue_job_name
    }
  }
}

resource "aws_iam_role" "lambda_role" {
  name = var.lambda_role_name

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "Service": "lambda.amazonaws.com" },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}
