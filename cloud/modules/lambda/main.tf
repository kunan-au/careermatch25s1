resource "aws_lambda_function" "trigger_glue_lambda" {
  function_name = var.lambda_function_name
  role          = aws_iam_role.lambda_role.arn
  runtime       = var.lambda_runtime
  handler       = var.lambda_handler

  s3_bucket = "sandbox-analytics-${var.unique_suffix}" # ✅ Fix this
  s3_key    = var.lambda_s3_key

  environment {
    variables = {
      GLUE_JOB_NAME = module.glue.glue_job_name
    }
  }
}
