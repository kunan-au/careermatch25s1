output "rds_public_endpoint" {
  value = module.rds_public.rds_endpoint
}

output "rds_private_endpoint" {
  value = module.rds_private.rds_endpoint
}

output "sandbox_analytics_bucket_name" {
  description = "Name of the Sandbox Analytics bucket"
  value       = aws_s3_bucket.sandbox_analytics_bucket.bucket
}

output "raw_data_bucket_name" {
  description = "Name of the Raw Data / Staging Zone bucket"
  value       = aws_s3_bucket.raw_data_bucket.bucket
}

output "curated_data_bucket_name" {
  description = "Name of the Curated Data Zone bucket"
  value       = aws_s3_bucket.curated_data_bucket.bucket
}

output "transient_zone_bucket_name" {
  description = "Name of the Transient Zone / Temp Zone bucket"
  value       = aws_s3_bucket.transient_zone_bucket.bucket
}

output "ec2_instance_public_ip" {
  description = "Public IP of the EC2 instance"
  value       = module.ec2_instance.public_ip
}

output "public_rds_password_file" {
  description = "File path of the public RDS password"
  value       = local_file.public_rds_password_file.filename
}

output "private_rds_password_file" {
  description = "File path of the private RDS password"
  value       = local_file.private_rds_password_file.filename
}

output "glue_job_name" {
  description = "Name of the Glue job"
  value       = module.glue.glue_job_name
}
