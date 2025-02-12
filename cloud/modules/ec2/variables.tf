variable "name" {
  description = "Name of the EC2 instance"
  type        = string
}

variable "ami_id" {
  description = "AMI ID for the EC2 instance"
  type        = string
}

variable "instance_type" {
  description = "Instance type for the EC2 instance"
  type        = string
}

variable "subnet_id" {
  description = "Subnet ID where the EC2 instance will be deployed"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID for the EC2 instance"
  type        = string
}

variable "private_rds_endpoint" {
  description = "Endpoint of the private RDS instance"
  type        = string
}

variable "private_rds_password" {
  description = "Password for the private RDS instance"
  type        = string
  sensitive   = true
}

variable "private_rds_username" {
  description = "Username for the private RDS instance"
  type        = string
}

variable "rds_security_group_id" {
  description = "Security group ID of the RDS instance"
  type        = string
}

variable "ssh_access_ip" {
  description = "Your IP address for SSH access"
  type        = string
}
