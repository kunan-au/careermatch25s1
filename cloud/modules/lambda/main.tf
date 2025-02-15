resource "aws_lambda_function" "trigger_glue_lambda" {
  filename      = "lambda_trigger_glue.zip"
  function_name = "trigger-glue-etl"
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.9"

  s3_bucket = "sandbox-analytics-${random_id.unique_suffix.hex}"
  s3_key    = "lambda_trigger_glue.zip"

  environment {
    variables = {
      GLUE_JOB_NAME = module.glue.glue_job_name
    }
  }
}
