variable "force_destroy" {
  description = "Whether to allow bucket destruction"
  type        = bool
  default     = false
}

variable "environment" {
  description = "Environment tag (e.g., dev, staging, prod)"
  type        = string
}
