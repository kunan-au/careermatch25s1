# Generate a random 6-character suffix for unique bucket names
resource "random_id" "unique_suffix" {
  byte_length = 3
}

# Public Bucket
resource "aws_s3_bucket" "public_bucket" {
  bucket        = "public-bucket-${random_id.unique_suffix.hex}"
  force_destroy = var.force_destroy

  tags = {
    Environment = var.environment
    Purpose     = "Public"
  }
}

resource "aws_s3_bucket_acl" "public_bucket_acl" {
  bucket = aws_s3_bucket.public_bucket.id
  acl    = "public-read"
}

# Raw Data / Staging Zone Bucket
resource "aws_s3_bucket" "raw_data_bucket" {
  bucket        = "raw-data-${random_id.unique_suffix.hex}"
  force_destroy = var.force_destroy

  tags = {
    Environment = var.environment
    Purpose     = "Raw Data / Staging Zone"
  }
}

resource "aws_s3_bucket_acl" "raw_data_bucket_acl" {
  bucket = aws_s3_bucket.raw_data_bucket.id
  acl    = "private"
}

# Curated Data Zone Bucket
resource "aws_s3_bucket" "curated_data_bucket" {
  bucket        = "curated-data-${random_id.unique_suffix.hex}"
  force_destroy = var.force_destroy

  tags = {
    Environment = var.environment
    Purpose     = "Curated Data Zone"
  }
}

resource "aws_s3_bucket_acl" "curated_data_bucket_acl" {
  bucket = aws_s3_bucket.curated_data_bucket.id
  acl    = "private"
}

# Transient Zone / Temp Zone Bucket
resource "aws_s3_bucket" "transient_zone_bucket" {
  bucket        = "transient-zone-${random_id.unique_suffix.hex}"
  force_destroy = var.force_destroy

  tags = {
    Environment = var.environment
    Purpose     = "Transient Zone / Temp Zone"
  }
}

resource "aws_s3_bucket_acl" "transient_zone_bucket_acl" {
  bucket = aws_s3_bucket.transient_zone_bucket.id
  acl    = "private"
}
