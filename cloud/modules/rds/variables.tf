variable "name" {
  description = "Name of the RDS instance"
  type        = string
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
  description = "Version of the database engine"
  type        = string
  default     = "8.0"
}

variable "instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.micro"
}

variable "db_name" {
  description = "Name of the database"
  type        = string
}

variable "username" {
  description = "Master username for the RDS instance"
  type        = string
  default     = "admin"
}

variable "subnet_ids" {
  description = "List of subnet IDs for the RDS instance"
  type        = list(string)
}

variable "publicly_accessible" {
  description = "Whether the RDS instance is publicly accessible"
  type        = bool
  default     = false
}

variable "skip_final_snapshot" {
  description = "Skip final snapshot on RDS instance deletion"
  type        = bool
  default     = true
}

variable "security_group_id" {
  description = "Security group ID for the RDS instance"
  type        = string
}

variable "environment" {
  description = "Environment tag for the RDS instance"
  type        = string
}

variable "password" {
  description = "Master password for the RDS instance"
  type        = string
  sensitive   = true
}
