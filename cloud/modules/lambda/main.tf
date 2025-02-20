# Create the Lambda function
resource "aws_lambda_function" "trigger_glue_lambda" {
  function_name = var.lambda_function_name
  handler       = var.lambda_handler
  runtime       = var.lambda_runtime
  role          = var.lambda_role_arn

  s3_bucket = var.lambda_s3_bucket
  s3_key    = var.lambda_s3_key

  # optional environment variables
  environment {
    variables = {
      GLUE_JOB_NAME      = var.glue_job_name
      GLUE_SCRIPT_PATH   = var.glue_script_path
      GLUE_ROLE_ARN      = var.glue_role_arn
      S3_BUCKET_NAME     = var.s3_bucket_name
      S3_RAW_DATA_PATH   = var.s3_raw_data_path
      S3_CURATED_PATH    = var.s3_curated_path
      S3_TEMP_PATH       = var.s3_temp_path
    }
  }
}

# (Optionally create a CloudWatch Event or trigger to run this Lambda)
