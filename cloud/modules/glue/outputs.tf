output "glue_job_name" {
  description = "Name of the Glue job"
  value       = aws_glue_job.python_script_job.name
}

output "glue_role_arn" {
  description = "IAM Role ARN for the Glue job"
  value       = aws_iam_role.glue_role.arn
}
