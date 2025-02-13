variable "stream_name" {
  description = "Name of the Firehose stream"
  default     = "ecommerce-firehose-stream"
}

variable "s3_bucket_name" {
  description = "Name of the S3 bucket for Firehose"
  default     = "ecommerce-firehose-data"
}
