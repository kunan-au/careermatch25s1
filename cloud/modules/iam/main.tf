resource "aws_iam_policy" "glue_s3_access" {
  name        = "career-match-glue-s3-access"
  description = "Allows AWS Glue to read from Raw S3 and write to Curated S3"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["s3:GetObject", "s3:ListBucket"]
        Resource = [
          "arn:aws:s3:::${aws_s3_bucket.raw_data_bucket.id}",
          "arn:aws:s3:::${aws_s3_bucket.raw_data_bucket.id}/*"
        ]
      },
      {
        Effect   = "Allow"
        Action   = ["s3:PutObject", "s3:ListBucket"]
        Resource = [
          "arn:aws:s3:::${aws_s3_bucket.curated_data_bucket.id}",
          "arn:aws:s3:::${aws_s3_bucket.curated_data_bucket.id}/*"
        ]
      }
    ]
  })
}

# IAM Role for AWS Glue
resource "aws_iam_role" "glue_role" {
  name = "glue-job-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "glue.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role" "lambda_role" {
  name = "lambda-job-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}


# Attach Glue S3 Access Policy to the Role
resource "aws_iam_role_policy_attachment" "glue_s3_attachment" {
  role       = aws_iam_role.glue_etl_role.name
  policy_arn = aws_iam_policy.glue_s3_access.arn
}

# Attach AWS Managed Glue Service Role Policy for Additional Permissions
resource "aws_iam_role_policy_attachment" "glue_service_role_attachment" {
  role       = aws_iam_role.glue_etl_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}
