variable "cluster_name" {
  description = "Name of the EMR cluster"
  default     = "ecommerce-etl-cluster"
}

variable "release_label" {
  description = "EMR release version"
  default     = "emr-6.7.0"
}

variable "applications" {
  description = "List of applications to install on EMR"
  type        = list(string)
  default     = ["Spark", "Hive"]
}

variable "s3_log_bucket" {
  description = "S3 bucket for EMR logs"
}

variable "s3_bootstrap" {
  description = "S3 bucket for bootstrap scripts"
}

variable "key_name" {
  description = "Key pair name for SSH access"
}

variable "subnet_id" {
  description = "Subnet ID where EMR will be deployed"
}

variable "security_group" {
  description = "Security group for EMR instances"
}

variable "master_instance_type" {
  description = "Instance type for the master node"
  default     = "m5.xlarge"
}

variable "core_instance_type" {
  description = "Instance type for core nodes"
  default     = "m5.xlarge"
}

variable "core_instance_count" {
  description = "Number of core nodes"
  default     = 2
}
