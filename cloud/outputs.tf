# RDS Outputs
output "rds_public_endpoint" {
  description = "Public RDS endpoint"
  value       = module.rds_public.rds_endpoint
}

output "rds_private_endpoint" {
  description = "Private RDS endpoint"
  value       = module.rds_private.rds_endpoint
}

# S3 Buckets
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

# EC2 Instance Outputs
output "ec2_instance_id" {
  description = "EC2 instance ID"
  value       = module.ec2_instance.instance_id
}

output "ec2_instance_public_ip" {
  description = "Public IP of the EC2 instance"
  value       = module.ec2_instance.public_ip
}

# Glue Outputs
output "glue_job_name" {
  description = "AWS Glue job name"
  value       = module.glue.glue_job_name
}

# Lambda Outputs
output "lambda_function_name" {
  description = "Lambda function name"
  value       = module.lambda.lambda_function_name
}

# Password Files (Local)
output "public_rds_password_file" {
  description = "File path of the public RDS password"
  value       = local_file.public_rds_password_file.filename
}

output "private_rds_password_file" {
  description = "File path of the private RDS password"
  value       = local_file.private_rds_password_file.filename
}
