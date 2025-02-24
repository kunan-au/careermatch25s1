#################################
# Provider Configuration
#################################
provider "aws" {
  region = var.aws_region
}

#################################
# VPC Module
#################################
module "vpc" {
  source               = "./modules/vpc"
  name                 = "career-match-vpc"
  cidr_block           = var.vpc_cidr
  public_subnet_cidrs  = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs
  azs                  = ["ap-southeast-2a", "ap-southeast-2b"]
  environment          = var.environment
}

#################################
# Generate Random Suffix
#################################
resource "random_id" "unique_suffix" {
  byte_length = 3
}

#################################
# S3 Buckets
#################################

# (1) Sandbox/Analytics Bucket
resource "aws_s3_bucket" "sandbox_analytics_bucket" {
  bucket        = "career-match-analytics-${random_id.unique_suffix.hex}"
  force_destroy = var.force_destroy

  tags = {
    Environment = var.environment
    Purpose     = "Career Match Analytics"
  }
}

# Raw Data Bucket
resource "aws_s3_bucket" "raw_data_bucket" {
  bucket        = "career-match-raw-data-${random_id.unique_suffix.hex}"
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
  bucket        = "career-match-curated-data-${random_id.unique_suffix.hex}"
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
  bucket        = "career-match-transient-zone-${random_id.unique_suffix.hex}"
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

#################################
# EC2 Module
#################################
module "ec2_instance" {
  source                = "./modules/ec2"
  name                  = "career-match-ec2"
  ami_id                = var.ami_id
  instance_type         = var.instance_type
  subnet_id             = module.vpc.public_subnet_ids[0]
  vpc_id                = module.vpc.vpc_id
  rds_security_group_id = module.vpc.private_security_group_id
  private_rds_endpoint  = module.rds_private.rds_endpoint
  private_rds_password  = random_password.private_rds_password.result
  private_rds_username  = var.rds_username
  ssh_access_ip         = var.ssh_access_ip
}

#################################
# Generate Random RDS Passwords
#################################
resource "random_password" "public_rds_password" {
  length           = 16
  special          = true
  override_special = "_-#$%^&*()+=!"
}

resource "random_password" "private_rds_password" {
  length           = 16
  special          = true
  override_special = "_-#$%^&*()+=!"
}

#################################
# Save RDS Passwords Locally
#################################
resource "local_file" "public_rds_password_file" {
  content  = random_password.public_rds_password.result
  filename = "${path.module}/public_rds_password.txt"
}

resource "local_file" "private_rds_password_file" {
  content  = random_password.private_rds_password.result
  filename = "${path.module}/private_rds_password.txt"
}

#################################
# Private RDS Module
#################################
module "rds_private" {
  source                = "./modules/rds"
  name                  = "career-match-private-db"
  allocated_storage     = var.allocated_storage
  max_allocated_storage = var.max_allocated_storage
  engine                = var.engine
  engine_version        = var.engine_version
  instance_class        = var.instance_class
  db_name               = var.db_name
  username              = var.rds_username
  password              = random_password.private_rds_password.result
  publicly_accessible   = false
  skip_final_snapshot   = var.skip_final_snapshot
  security_group_id     = module.vpc.private_security_group_id
  subnet_ids            = module.vpc.private_subnet_ids
  environment           = var.environment
}

#################################
# Public RDS Module
#################################
module "rds_public" {
  source                = "./modules/rds"
  name                  = "career-match-public-db"
  allocated_storage     = var.allocated_storage
  max_allocated_storage = var.max_allocated_storage
  engine                = var.engine
  engine_version        = var.engine_version
  instance_class        = var.instance_class
  db_name               = var.db_name
  username              = var.rds_username
  password              = random_password.public_rds_password.result
  publicly_accessible   = true
  skip_final_snapshot   = var.skip_final_snapshot
  security_group_id     = module.vpc.public_security_group_id
  subnet_ids            = module.vpc.public_subnet_ids
  environment           = var.environment
}

#################################
# Upload Glue Script to S3
#################################
resource "aws_s3_object" "glue_script_upload" {
  bucket = aws_s3_bucket.sandbox_analytics_bucket.bucket
  key    = "scripts/glue_etl_script.py"
  source = "/home/kunan/careermatch25s1/cloud/modules/glue/scripts/glue_etl_script.py"

  etag = filemd5("/home/kunan/careermatch25s1/cloud/modules/glue/scripts/glue_etl_script.py")
}

#################################
# Upload Lambda ZIP to S3
#################################
resource "aws_s3_object" "lambda_trigger_glue_zip" {
  bucket = aws_s3_bucket.sandbox_analytics_bucket.bucket
  key    = "lambda_trigger_glue.zip"
  source = "/home/kunan/careermatch25s1/cloud/modules/lambda/lambda_trigger_glue.zip"

  etag = filemd5("/home/kunan/careermatch25s1/cloud/modules/lambda/lambda_trigger_glue.zip")
}

#################################
# Deploy AWS Glue
#################################
module "glue" {
  source           = "./modules/glue"
  glue_script_name = "glue-etl-to-rds"

  # The S3 script references remain the same
  glue_script_path = aws_s3_object.glue_script_upload.key
  s3_bucket_name   = aws_s3_bucket.sandbox_analytics_bucket.bucket
  s3_raw_data_path = aws_s3_bucket.raw_data_bucket.bucket
  s3_curated_path  = aws_s3_bucket.curated_data_bucket.bucket
  s3_temp_path     = aws_s3_bucket.transient_zone_bucket.bucket

  # RDS info remains the same
  rds_endpoint  = module.rds_private.rds_endpoint
  rds_username  = var.rds_username
  rds_password  = random_password.private_rds_password.result
  rds_database  = var.db_name
  environment   = var.environment

  # Use the existing Glue service role
  glue_role_arn = var.existing_glue_role_arn
}

#################################
# Deploy AWS Lambda
#################################

/*

module "lambda" {
  source                = "./modules/lambda"
  lambda_function_name  = "trigger-career-match-glue-etl"
  lambda_handler        = "lambda_function.lambda_handler"
  lambda_runtime        = "python3.9"
  lambda_role_arn       = var.existing_lambda_role_arn

  lambda_s3_bucket      = aws_s3_bucket.sandbox_analytics_bucket.bucket
  lambda_s3_key         = aws_s3_object.lambda_trigger_glue_zip.key

  glue_job_name         = module.glue.glue_job_name
  # glue_role_arn = module.iam.glue_role_arn   # commented out
  glue_script_path      = aws_s3_object.glue_script_upload.key

  s3_bucket_name        = aws_s3_bucket.sandbox_analytics_bucket.bucket
  s3_raw_data_path      = aws_s3_bucket.raw_data_bucket.bucket
  s3_curated_path       = aws_s3_bucket.curated_data_bucket.bucket
  s3_temp_path          = aws_s3_bucket.transient_zone_bucket.bucket
  unique_suffix         = random_id.unique_suffix.hex
}

*/

#################################
# EMR Cluster
#################################
resource "aws_emr_cluster" "emr_cluster" {
  name          = var.cluster_name
  release_label = var.release_label
  applications  = var.applications

  log_uri = "s3://${aws_s3_bucket.sandbox_analytics_bucket.bucket}/emr-logs/"
  service_role = var.emr_service_role_arn

  ec2_attributes {
    key_name         = var.key_name
    subnet_id        = module.vpc.private_subnet_ids[0]
    instance_profile = var.emr_instance_profile_arn

    emr_managed_master_security_group = module.vpc.private_security_group_id
    emr_managed_slave_security_group  = module.vpc.private_security_group_id
  }

  master_instance_group {
    instance_type  = var.master_instance_type
    instance_count = 1
  }

  core_instance_group {
    instance_type  = var.core_instance_type
    instance_count = 1
  }

  # Updated file path: points to the file within the modules/emr folder.
  configurations_json = file("${path.module}/modules/emr/emr-config.json")
  
  bootstrap_action {
    name = "bootstrap-script"
    path = "s3://${aws_s3_bucket.sandbox_analytics_bucket.bucket}/bootstrap/bootstrap.sh"
  }

  tags = {
    Environment = var.environment
    Project     = "CareerMatch-ETL"
  }
}
