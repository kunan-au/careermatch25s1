variable "sagemaker_notebook_name" {
  description = "Name of the SageMaker Notebook Instance"
  type        = string
  default     = "my-sagemaker-notebook"
}

variable "sagemaker_instance_type" {
  description = "Instance type for the SageMaker Notebook"
  type        = string
  default     = "ml.t3.medium"
}

variable "sagemaker_role_name" {
  description = "Name of the IAM Role for SageMaker"
  type        = string
  default     = "sagemaker-role1"
}

variable "s3_policy_arn" {
  description = "ARN of the S3 access policy"
  type        = string
  default     = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

variable "local_notebook_path" {
  description = "The local path to the XG
