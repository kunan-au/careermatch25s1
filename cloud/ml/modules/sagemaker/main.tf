resource "aws_sagemaker_notebook_instance" "example" {
  name                   = var.sagemaker_notebook_name
  instance_type          = var.sagemaker_instance_type
  role_arn               = aws_iam_role.sagemaker_role1.arn
  direct_internet_access = "Enabled"
}

resource "aws_iam_role" "sagemaker_role1" {
  name = var.sagemaker_role_name

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "sagemaker.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "s3_access" {
  role       = aws_iam_role.sagemaker_role1.name
  policy_arn = var.s3_policy_arn
}

resource "local_file" "notebook_reference" {
  filename = var.local_notebook_path
  content  = "This is the local path to the XGBoost notebook used with SageMaker: ${var.local_notebook_path}"
}
