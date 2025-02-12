# AWS Region
variable "aws_region" {
  description = "AWS region to deploy resources"
  default     = "ap-southeast-2"
}

# CIDR Block for VPC
variable "cidr_block" {
  description = "CIDR block for the VPC"
  default     = "10.0.0.0/16"
}

# Public Subnets
variable "public_subnet_cidrs" {
  description = "List of CIDR blocks for public subnets"
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

# Private Subnets
variable "private_subnet_cidrs" {
  description = "List of CIDR blocks for private subnets"
  default     = ["10.0.3.0/24", "10.0.4.0/24"]
}

# Availability Zones
variable "azs" {
  description = "List of availability zones"
  default     = ["ap-southeast-2a", "ap-southeast-2b"]
}

# Name Tag
variable "name" {
  description = "Name tag for resources"
  default     = "ecommerce-vpc"
}

# Environment
variable "environment" {
  description = "Environment tag for resources"
  default     = "dev"
}

# SSH Access IP
variable "ssh_access_ip" {
  description = "Your IP address for SSH access"
  default     = "0.0.0.0/0" # Replace with your IP for better security
}
