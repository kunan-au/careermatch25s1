# Glue IAM Role
resource "aws_iam_role" "glue_role" {
  name               = "${var.glue_script_name}-role"
  assume_role_policy = data.aws_iam_policy_document.glue_assume_role_policy.json
}

# Glue Role Policy Attachment
resource "aws_iam_policy_attachment" "glue_policy_attachment" {
  name       = "${var.glue_script_name}-policy-attachment"
  roles      = [aws_iam_role.glue_role.name]
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

# Custom IAM Policy for S3 Access
resource "aws_iam_policy" "glue_custom_policy" {
  name        = "GlueCustomPolicy"
  description = "Additional permissions for Glue jobs"
  policy      = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow"
        Action   = [
          "s3:GetObject",
          "s3:ListBucket"
        ]
        Resource = [
          "arn:aws:s3:::${var.s3_bucket_name}",
          "arn:aws:s3:::${var.s3_bucket_name}/*"
        ]
      }
    ]
  })
}

resource "aws_iam_policy_attachment" "glue_custom_policy_attachment" {
  name       = "GlueCustomPolicyAttachment"
  roles      = [aws_iam_role.glue_role.name]
  policy_arn = aws_iam_policy.glue_custom_policy.arn
}

# Glue Job
resource "aws_glue_job" "python_script_job" {
  name     = "${var.glue_script_name}-job"
  role_arn = aws_iam_role.glue_role.arn

  command {
    script_location = "s3://${var.s3_bucket_name}/${var.glue_script_path}"
    python_version  = "3"
  }

  glue_version      = "3.0"
  number_of_workers = 2
  worker_type       = "G.1X"

  tags = {
    Environment = var.environment
  }
}

# IAM Policy for Glue Role
data "aws_iam_policy_document" "glue_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["glue.amazonaws.com"]
    }
  }
}
