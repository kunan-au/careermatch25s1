# Glue IAM Role
resource "aws_iam_role" "glue_role" {
  name = var.glue_role_name
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = { Service = "glue.amazonaws.com" }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role" "glue_etl_role" {
  name               = var.glue_role_name
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "Service": "glue.amazonaws.com" },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

# Glue IAM Policy
resource "aws_iam_policy" "glue_s3_access" {
  name        = "glue_s3_access"
  description = "Allows Glue to access S3"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["s3:GetObject", "s3:ListBucket"]
        Resource = [
          "${var.raw_data_bucket_arn}",
          "${var.raw_data_bucket_arn}/*"
        ]
      },
      {
        Effect   = "Allow"
        Action   = ["s3:PutObject", "s3:ListBucket"]
        Resource = [
          "${var.curated_data_bucket_arn}",
          "${var.curated_data_bucket_arn}/*"
        ]
      }
    ]
  })
}

# Attach IAM Policy to Glue Role
resource "aws_iam_role_policy_attachment" "glue_service_role_attachment" {
  role       = aws_iam_role.glue_role.name
  policy_arn = aws_iam_policy.glue_s3_access.arn
}

resource "aws_iam_role" "lambda_role" {
  name = var.lambda_role_name

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "Service": "lambda.amazonaws.com" },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

# Lambda IAM Policy
resource "aws_iam_policy" "lambda_s3_access" {
  name        = "lambda_s3_access"
  description = "Allows Lambda to access S3 and invoke Glue"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["s3:GetObject", "s3:ListBucket"]
        Resource = [
          "${var.raw_data_bucket_arn}",
          "${var.raw_data_bucket_arn}/*"
        ]
      },
      {
        Effect   = "Allow"
        Action   = ["glue:StartJobRun"]
        Resource = "*"
      }
    ]
  })
}

# Attach IAM Policy to Lambda Role
resource "aws_iam_role_policy_attachment" "lambda_service_role_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_s3_access.arn
}
