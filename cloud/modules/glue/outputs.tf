output "glue_script_s3_path" {
  description = "S3 path of the Glue script"
  value       = "s3://${var.s3_bucket_name}/${var.glue_script_path}"
}

output "glue_temp_dir" {
  description = "Temporary directory for Glue job"
  value       = "s3://${var.s3_bucket_name}/temp/"
}
