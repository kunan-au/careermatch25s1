# First VPC (for RDS and Lambda)
resource "aws_vpc" "vpc_lambda_rds" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "vpc-lambda-rds"
  }
}

# Second VPC (for S3 Endpoint and Glue Job)
resource "aws_vpc" "vpc_glue_s3" {
  cidr_block           = "10.1.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "vpc-glue-s3"
  }
}

# Subnet (Lambda and RDS)
resource "aws_subnet" "subnet_lambda_rds" {
  vpc_id             = aws_vpc.vpc_lambda_rds.id
  cidr_block         = "10.0.1.0/24"
  availability_zone  = "ap-southeast-2a"

  tags = {
    Name = "subnet-lambda-rds"
  }
  depends_on = [aws_vpc.vpc_lambda_rds]
}

# Subnet (Glue and S3)
resource "aws_subnet" "subnet_glue_s3" {
  vpc_id             = aws_vpc.vpc_glue_s3.id
  cidr_block         = "10.1.1.0/24"
  availability_zone  = "ap-southeast-2a"

  tags = {
    Name = "subnet-glue-s3"
  }
  depends_on = [aws_vpc.vpc_glue_s3]
}

resource "aws_security_group" "lambda_sg" {
  vpc_id = aws_vpc.vpc_lambda_rds.id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "lambda-security-group"
  }
  depends_on = [aws_vpc.vpc_lambda_rds]
}

resource "aws_security_group" "rds_sg" {
  vpc_id = aws_vpc.vpc_lambda_rds.id

  ingress {
    from_port       = 3306
    to_port         = 3306
    protocol        = "tcp"
    security_groups = [aws_security_group.lambda_sg.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "rds-security-group"
  }
  depends_on = [aws_vpc.vpc_lambda_rds]
}

# Route Table for VPC of Lambda and RDS
resource "aws_route_table" "route_table_lambda_rds" {
  vpc_id = aws_vpc.vpc_lambda_rds.id

  tags = {
    Name = "route-table-lambda-rds"
  }
  depends_on = [aws_vpc.vpc_lambda_rds]
}

# VPC Endpoint (Glue and S3)
resource "aws_vpc_endpoint" "s3_endpoint_glue" {
  vpc_id            = aws_vpc.vpc_glue_s3.id
  service_name      = "com.amazonaws.ap-southeast-2.s3"
  vpc_endpoint_type = "Gateway"

  route_table_ids = [aws_route_table.route_table_glue_s3.id]

  tags = {
    Name = "s3-endpoint-glue"
  }
  depends_on = [aws_route_table.route_table_glue_s3]
}

# VPC Endpoint (Lambda and S3)
resource "aws_vpc_endpoint" "s3_endpoint_lambda" {
  vpc_id            = aws_vpc.vpc_lambda_rds.id
  service_name      = "com.amazonaws.ap-southeast-2.s3"
  vpc_endpoint_type = "Gateway"

  route_table_ids = [aws_route_table.route_table_lambda_rds.id]

  tags = {
    Name = "s3-endpoint-lambda"
  }
  depends_on = [aws_route_table.route_table_lambda_rds]
}

# Connect Subnet and Route Table (Lambda and RDS)
resource "aws_route_table_association" "subnet_route_association_lambda_rds" {
  subnet_id      = aws_subnet.subnet_lambda_rds.id
  route_table_id = aws_route_table.route_table_lambda_rds.id

  depends_on = [
    aws_subnet.subnet_lambda_rds,
    aws_route_table.route_table_lambda_rds
  ]
}

# Route Table for VPC of Glue and S3
resource "aws_route_table" "route_table_glue_s3" {
  vpc_id = aws_vpc.vpc_glue_s3.id

  tags = {
    Name = "route-table-glue-s3"
  }
  depends_on = [aws_vpc.vpc_glue_s3]
}

# Connect Subnet and Route Table (Glue and S3)
resource "aws_route_table_association" "subnet_route_association_glue_s3" {
  subnet_id      = aws_subnet.subnet_glue_s3.id
  route_table_id = aws_route_table.route_table_glue_s3.id

  depends_on = [
    aws_subnet.subnet_glue_s3,
    aws_route_table.route_table_glue_s3
  ]
}
