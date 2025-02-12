# Output the RDS endpoint
output "rds_endpoint" {
  description = "Endpoint of the RDS instance"
  value       = aws_db_instance.rds_instance.endpoint
}

# Output the file path of the saved RDS password
output "rds_password_file" {
  description = "File path of the saved RDS password"
  value       = local_file.rds_password_file.filename
}
