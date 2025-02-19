output "glue_etl_role_arn" {
  value = aws_iam_role.glue_etl_role.arn
}

output "lambda_role_arn" {
  description = "IAM Role ARN for the Lambda function"
  value       = aws_iam_role.lambda_role.arn
}
