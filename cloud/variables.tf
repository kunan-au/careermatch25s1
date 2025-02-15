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

variable "s3_bucket_name" {
  description = "S3 bucket where the Glue script is stored"
  type        = string
}

variable "s3_raw_data_path" {
  description = "S3 path where raw data is stored"
  type        = string
}

variable "s3_temp_path" {
  description = "S3 path for Glue temporary storage"
  type        = string
  default     = "temp/"
}

variable "username" {
  description = "Database username"
  type        = string
}

variable "glue_job_name" {
  description = "AWS Glue Job Name"
  type        = string
}
