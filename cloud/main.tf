# Provider Configuration
provider "aws" {
  region = var.aws_region
}

# VPC Module
module "vpc" {
  source               = "./modules/vpc"
  name                 = "ecommerce-vpc"
  cidr_block           = var.vpc_cidr
  public_subnet_cidrs  = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs
  azs                  = ["ap-southeast-2a", "ap-southeast-2b"]
  environment          = var.environment
}

# Generate Random Suffix for Unique Resource Names
resource "random_id" "unique_suffix" {
  byte_length = 3 # 6-character hexadecimal
}

# S3 Buckets
# Sandbox Analytics Bucket (formerly Public Bucket)
resource "aws_s3_bucket" "sandbox_analytics_bucket" {
  bucket        = "sandbox-analytics-${random_id.unique_suffix.hex}"
  force_destroy = var.force_destroy

  tags = {
    Environment = var.environment
    Purpose     = "Sandbox Analytics"
  }
}

resource "aws_s3_bucket_public_access_block" "sandbox_analytics_bucket_block" {
  bucket                  = aws_s3_bucket.sandbox_analytics_bucket.id
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "sandbox_analytics_bucket_policy" {
  bucket = aws_s3_bucket.sandbox_analytics_bucket.id

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::${aws_s3_bucket.sandbox_analytics_bucket.id}/*"
    }
  ]
}
POLICY
}

# Raw Data Bucket
resource "aws_s3_bucket" "raw_data_bucket" {
  bucket        = "raw-data-${random_id.unique_suffix.hex}"
  force_destroy = var.force_destroy

  tags = {
    Environment = var.environment
    Purpose     = "Raw Data / Staging Zone"
  }
}

resource "aws_s3_bucket_public_access_block" "raw_data_bucket_block" {
  bucket                  = aws_s3_bucket.raw_data_bucket.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Curated Data Bucket
resource "aws_s3_bucket" "curated_data_bucket" {
  bucket        = "curated-data-${random_id.unique_suffix.hex}"
  force_destroy = var.force_destroy

  tags = {
    Environment = var.environment
    Purpose     = "Curated Data Zone"
  }
}

resource "aws_s3_bucket_public_access_block" "curated_data_bucket_block" {
  bucket                  = aws_s3_bucket.curated_data_bucket.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Transient Zone Bucket
resource "aws_s3_bucket" "transient_zone_bucket" {
  bucket        = "transient-zone-${random_id.unique_suffix.hex}"
  force_destroy = var.force_destroy

  tags = {
    Environment = var.environment
    Purpose     = "Transient Zone / Temp Zone"
  }
}

resource "aws_s3_bucket_public_access_block" "transient_zone_bucket_block" {
  bucket                  = aws_s3_bucket.transient_zone_bucket.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# EC2 Module
module "ec2_instance" {
  source               = "./modules/ec2"
  name                 = "ecommerce-ec2"
  ami_id               = var.ami_id
  instance_type        = var.instance_type
  subnet_id            = module.vpc.public_subnet_ids[0]
  vpc_id               = module.vpc.vpc_id
  rds_security_group_id = module.vpc.private_security_group_id
  private_rds_endpoint = module.rds_private.rds_endpoint
  private_rds_password = random_password.private_rds_password.result
  private_rds_username = var.username

  ssh_access_ip        = var.ssh_access_ip
}

# Generate Random Passwords for RDS
resource "random_password" "public_rds_password" {
  length           = 16
  special          = true
  override_special = "_-#$%^&*()+=!" # Exclude invalid characters
}

resource "random_password" "private_rds_password" {
  length           = 16
  special          = true
  override_special = "_-#$%^&*()+=!" # Exclude invalid characters
}

# Save RDS Passwords Locally
resource "local_file" "public_rds_password_file" {
  content  = random_password.public_rds_password.result
  filename = "${path.module}/public_rds_password.txt"
}

resource "local_file" "private_rds_password_file" {
  content  = random_password.private_rds_password.result
  filename = "${path.module}/private_rds_password.txt"
}

# Private RDS Module
module "rds_private" {
  source                = "./modules/rds"
  name                  = "ecommerce-private-db"
  allocated_storage     = var.allocated_storage
  max_allocated_storage = var.max_allocated_storage
  engine                = var.engine
  engine_version        = var.engine_version
  instance_class        = var.instance_class
  db_name               = var.db_name
  username              = var.username
  password              = random_password.private_rds_password.result
  publicly_accessible   = false
  skip_final_snapshot   = var.skip_final_snapshot
  security_group_id     = module.vpc.private_security_group_id
  subnet_ids            = module.vpc.private_subnet_ids
  environment           = var.environment
}

# Public RDS Module
module "rds_public" {
  source                = "./modules/rds"
  name                  = "ecommerce-public-db"
  allocated_storage     = var.allocated_storage
  max_allocated_storage = var.max_allocated_storage
  engine                = var.engine
  engine_version        = var.engine_version
  instance_class        = var.instance_class
  db_name               = var.db_name
  username              = var.username
  password              = random_password.public_rds_password.result
  publicly_accessible   = true
  skip_final_snapshot   = var.skip_final_snapshot
  security_group_id     = module.vpc.public_security_group_id
  subnet_ids            = module.vpc.public_subnet_ids
  environment           = var.environment
}

# Glue Module
module "glue" {
  source              = "./modules/glue"
  environment         = var.environment
  glue_script_name    = "test"  # Use job name without file extension
  glue_script_path    = "notebooks/test.ipynb"
  s3_bucket_name      = "sandbox-analytics-348eda"
}
