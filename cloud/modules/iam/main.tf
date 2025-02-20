# For Glue:
data "aws_iam_policy_document" "glue_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["glue.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "glue_role" {
  name               = var.glue_role_name
  assume_role_policy = data.aws_iam_policy_document.glue_assume_role.json
  tags = {
    Purpose = "Glue ETL role"
  }
}

# Attach standard AWSGlueServiceRole policy, plus our custom S3
resource "aws_iam_role_policy_attachment" "glue_service_attach" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
  role       = aws_iam_role.glue_role.name
}

resource "aws_iam_role_policy" "glue_s3_policy" {
  name   = "${var.glue_role_name}-s3-policy"
  role   = aws_iam_role.glue_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ]
        Effect   = "Allow"
        Resource = [
          var.raw_data_bucket_arn,
          "${var.raw_data_bucket_arn}/*",
          var.curated_data_bucket_arn,
          "${var.curated_data_bucket_arn}/*"
        ]
      }
    ]
  })
}

# For Lambda:
data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "lambda_role" {
  name               = var.lambda_role_name
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
  tags = {
    Purpose = "Lambda role"
  }
}

# Attach basic AWSLambdaBasicExecutionRole
resource "aws_iam_role_policy_attachment" "lambda_basic_attach" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.lambda_role.name
}

# This policy can call Glue
resource "aws_iam_role_policy" "lambda_glue_call" {
  name = "${var.lambda_role_name}-glue-policy"
  role = aws_iam_role.lambda_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "glue:StartJobRun",
          "glue:GetJobRun",
          "glue:GetJobRuns"
        ]
        Effect   = "Allow"
        Resource = "*"
      }
    ]
  })
}

