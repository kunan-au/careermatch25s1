output "glue_job_name" {
  description = "Name of the Glue job"
  value       = aws_glue_job.glue_etl_job.name
}

output "glue_role_arn" {
  description = "IAM Role ARN for the Glue job"
  value       = aws_iam_role.glue_role.arn
}

output "glue_script_s3_path" {
  description = "S3 path of the Glue script"
  value       = "s3://${var.s3_bucket_name}/${var.glue_script_path}"
}

output "glue_temp_dir" {
  description = "Temporary directory for Glue job"
  value       = "s3://${var.s3_bucket_name}/temp/"
}
