output "public_bucket_name" {
  description = "Name of the Public bucket"
  value       = aws_s3_bucket.public_bucket.bucket
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
