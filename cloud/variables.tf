# EC2 Configuration
variable "ami_id" {
  description = "AMI ID for the EC2 instance"
  type        = string
  default     = "ami-0a1f33f1492ad1c30"
}

variable "instance_type" {
  description = "Instance type for the EC2 instance"
  type        = string
  default     = "t3.micro"
}

# Networking (VPC & Subnets)
variable "environment" {
  description = "Deployment environment (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
  description = "List of CIDR blocks for public subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnet_cidrs" {
  description = "List of CIDR blocks for private subnets"
  type        = list(string)
  default     = ["10.0.3.0/24", "10.0.4.0/24"]
}

# RDS Database Configuration
variable "allocated_storage" {
  description = "Allocated storage for the RDS instance in GB"
  type        = number
  default     = 20
}

variable "max_allocated_storage" {
  description = "Maximum allocated storage for the RDS instance"
  type        = number
  default     = 100
}

variable "engine" {
  description = "Database engine for RDS"
  type        = string
  default     = "mysql"
}

variable "engine_version" {
  description = "Database engine version for RDS"
  type        = string
  default     = "8.0"
}

variable "instance_class" {
  description = "Instance class for the RDS instance"
  type        = string
  default     = "db.t3.micro"
}

variable "db_name" {
  description = "Database name for RDS"
  type        = string
  default     = "mydatabase"
}

variable "rds_username" {
  description = "Master username for the RDS instance"
  type        = string
  default     = "admin"
}

variable "skip_final_snapshot" {
  description = "Skip the final snapshot when RDS is deleted"
  type        = bool
  default     = true
}

variable "publicly_accessible" {
  description = "Whether the RDS instance should be publicly accessible"
  type        = bool
  default     = false
}

# Security
variable "ssh_access_ip" {
  description = "IP address or range allowed to SSH into EC2 instances"
  type        = string
  default     = "0.0.0.0/0" # Replace with your IP for security
}

# S3 Buckets
variable "acl" {
  description = "ACL for the buckets"
  type        = string
  default     = "private"
}

variable "force_destroy" {
  description = "Whether to allow bucket destruction"
  type        = bool
  default     = false
}

# Tags for Resources
variable "tags" {
  description = "Additional tags for all resources"
  type        = map(string)
  default     = {
    Project = "Ecommerce"
    Owner   = "DevOps"
  }
}

# AWS Glue
variable "glue_script_name" {
  description = "Name of the Glue job (e.g., glue-etl-to-rds)"
  type        = string
  default     = "glue-etl-to-rds"
}

variable "glue_script_path" {
  description = "Path to the script in the S3 bucket (e.g., scripts/glue_etl.py)"
  type        = string
  default     = "scripts/glue_etl.py"
}

variable "s3_temp_path" {
  description = "S3 path for Glue temporary storage"
  type        = string
  default     = "temp/"
}

variable "existing_glue_role_arn" {
  type        = string
  description = "ARN of the existing Glue service role"
  default     = "arn:aws:iam::423623841608:role/service-role/AWSGlueServiceRole-kun"
}

variable "existing_lambda_role_arn" {
  type        = string
  description = "Use an existing Lambda execution role"
  default     = "arn:aws:iam::423623841608:role/some-existing-lambda-role"
}

#################################
# EMR Variables
#################################

# Name of the EMR cluster
variable "cluster_name" {
  type        = string
  description = "Name of the EMR cluster"
  default     = "career-match-emr"
}

# EMR release label (e.g., emr-6.7.0)
variable "release_label" {
  type        = string
  description = "Release version for EMR"
  default     = "emr-6.7.0"
}

# List of EMR applications to install (e.g. Spark, Hive, etc.)
variable "applications" {
  type        = list(string)
  description = "List of applications to install on EMR"
  default     = ["Spark", "Hive"]
}

# ARN of the IAM role for the EMR service
variable "emr_service_role_arn" {
  type        = string
  description = "IAM service role ARN used by EMR"
  default     = ""
}

# ARN of the instance profile attached to EMR core/master instances
variable "emr_instance_profile_arn" {
  type        = string
  description = "IAM instance profile ARN for EMR nodes"
  default     = ""
}

# Key pair name for SSH access to EMR master node
variable "key_name" {
  type        = string
  description = "Key pair name for EMR cluster"
  default     = ""
}

# Master instance type (e.g., m5.xlarge)
variable "master_instance_type" {
  type        = string
  description = "Instance type for the EMR master node"
  default     = "m5.xlarge"
}

# Core instance type (e.g., m5.xlarge)
variable "core_instance_type" {
  type        = string
  description = "Instance type for EMR core nodes"
  default     = "m5.xlarge"
}
