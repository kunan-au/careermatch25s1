output "lambda_function_name" {
  description = "Name of the AWS Lambda function"
  value       = aws_lambda_function.trigger_glue_lambda.function_name
}

output "lambda_function_arn" {
  description = "ARN of the AWS Lambda function"
  value       = aws_lambda_function.trigger_glue_lambda.arn
}

output "lambda_role_arn" {
  description = "IAM Role ARN associated with Lambda"
  value       = aws_iam_role.lambda_role.arn
}

output "lambda_s3_bucket" {
  description = "S3 bucket where the Lambda function ZIP is stored"
  value       = "sandbox-analytics-${random_id.unique_suffix.hex}"
}

output "lambda_s3_key" {
  description = "S3 key (path) for the Lambda ZIP file"
  value       = "lambda_trigger_glue.zip"
}
