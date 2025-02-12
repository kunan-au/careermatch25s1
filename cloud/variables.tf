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

variable "username" {
  description = "Master username for the RDS instance"
  type        = string
  default     = "admin"
}

variable "skip_final_snapshot" {
  description = "Skip the final snapshot when RDS is deleted"
  type        = bool
  default     = true
}

variable "ssh_access_ip" {
  description = "IP address or range allowed to SSH into EC2 instances"
  type        = string
  default     = "0.0.0.0/0" # Replace with your IP for security
}

variable "publicly_accessible" {
  description = "Whether the RDS instance should be publicly accessible"
  type        = bool
  default     = false
}

variable "tags" {
  description = "Additional tags for all resources"
  type        = map(string)
  default     = {
    Project = "Ecommerce"
    Owner   = "DevOps"
  }
}

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