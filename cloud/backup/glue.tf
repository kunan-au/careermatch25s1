# Glue Job IAM Role
resource "aws_iam_role" "glue_job_role" {
  name = "glue-job-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action    = "sts:AssumeRole",
        Effect    = "Allow",
        Principal = {
          Service = "glue.amazonaws.com"
        }
      }
    ]
  })
}

# Glue Job Role Policies
resource "aws_iam_policy_attachment" "glue_job_policy_attachment_1" {
  name       = "glue-job-policy-attachment-1"
  roles      = [aws_iam_role.glue_job_role.name]
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

resource "aws_iam_policy_attachment" "glue_job_policy_attachment_2" {
  name       = "glue-job-policy-attachment-2"
  roles      = [aws_iam_role.glue_job_role.name]
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_iam_policy_attachment" "glue_job_policy_attachment_3" {
  name       = "glue-job-policy-attachment-3"
  roles      = [aws_iam_role.glue_job_role.name]
  policy_arn = "arn:aws:iam::aws:policy/AmazonRDSFullAccess"
}

# Glue Job Configuration
resource "aws_glue_job" "second_glue_job" {
  name     = "second-glue-job"
  role_arn = aws_iam_role.glue_job_role.arn

  command {
    name            = "glueetl"
    script_location = "s3://group-script1/script/"
    python_version  = "3"
  }

  default_arguments = {
    "--TempDir"              = "s3://groupwork-test-temp/temp/"
    "--job-bookmark-option"  = "job-bookmark-enable"
    "--enable-metrics"       = "true"
    "--enable-glue-datacatalog" = ""
    "--security-group-ids"      = aws_security_group.glue_sg.id
    "--subnet-id"               = aws_subnet.subnet_glue_s3.id
  }

  glue_version      = "3.0"
  timeout           = 10
  number_of_workers = 2
  worker_type       = "G.1X"

  depends_on = [
    aws_subnet.subnet_glue_s3,
    aws_security_group.glue_sg
  ]
}

resource "aws_glue_job" "third_glue_job" {
  name     = "third-glue-job"
  role_arn = aws_iam_role.glue_job_role.arn

  command {
    name            = "glueetl"
    script_location = "s3://group-script2/script/"
    python_version  = "3"
  }

  default_arguments = {
    "--TempDir"              = "s3://groupwork-test-temp/temp/"
    "--job-bookmark-option"  = "job-bookmark-enable"
    "--enable-metrics"       = "true"
    "--enable-glue-datacatalog" = ""
    "--security-group-ids"      = aws_security_group.glue_sg.id
    "--subnet-id"               = aws_subnet.subnet_glue_s3.id
  }

  glue_version      = "3.0"
  timeout           = 10
  number_of_workers = 2
  worker_type       = "G.1X"

  depends_on = [
    aws_subnet.subnet_glue_s3,
    aws_security_group.glue_sg
  ]
}

# Security Group for Glue Job and S3
resource "aws_security_group" "glue_sg" {
  name   = "glue-security-group"
  vpc_id = aws_vpc.vpc_glue_s3.id

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["10.1.1.0/24"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "glue-sg"
  }
  depends_on = [aws_vpc.vpc_glue_s3]
}

resource "aws_glue_crawler" "ml_crawler" {
  name                          = "ml-crawler"
  database_name                 = aws_glue_catalog_database.mldatabase.name
  role                          = aws_iam_role.glue_job_role.arn
  table_prefix                  = "ml_"
  s3_target {
    path = "s3://group-ml/user_features_1/"
  }
  s3_target {
    path = "s3://group-ml/user_features_2/"
  }
  s3_target {
    path = "s3://group-ml/up_features/"
  }
  s3_target {
    path = "s3://group-ml/prd_features/"
  }
  tags = {
    Name = "ml-crawler"
  }
}

resource "aws_glue_catalog_database" "mldatabase" {
  name = "mldatabase"
}
