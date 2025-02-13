output "firehose_stream_name" {
  value = aws_kinesis_firehose_delivery_stream.firehose_stream.name
}

output "firehose_s3_bucket" {
  value = aws_s3_bucket.firehose_bucket.bucket
}
