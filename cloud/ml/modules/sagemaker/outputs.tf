output "sagemaker_notebook_arn" {
  description = "The ARN of the SageMaker Notebook Instance"
  value       = aws_sagemaker_notebook_instance.example.arn
}

output "sagemaker_notebook_url" {
  description = "The URL of the SageMaker Notebook Instance"
  value       = aws_sagemaker_notebook_instance.example.url
}

output "iam_role_arn" {
  description = "The ARN of the IAM Role for SageMaker"
  value       = aws_iam_role.sagemaker_role1.arn
}

output "local_notebook_path" {
  description = "The local path to the XGBoost Jupyter Notebook"
  value       = var.local_notebook_path
}
