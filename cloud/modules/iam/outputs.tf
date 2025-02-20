output "glue_role_arn" {
  value = aws_iam_role.glue_role.arn
}

output "lambda_role_arn" {
  description = "ARN of the newly created Lambda role"
  value       = aws_iam_role.lambda_role.arn
}
