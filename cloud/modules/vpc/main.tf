# Provider Configuration
provider "aws" {
  region = var.aws_region
}

# Create the main VPC
resource "aws_vpc" "main_vpc" {
  cidr_block           = var.cidr_block
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name        = var.name
    Environment = var.environment
  }
}

# Create an Internet Gateway for public internet access
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main_vpc.id

  tags = {
    Name = "${var.name}-igw"
  }
}

# Create Public Subnets
resource "aws_subnet" "public_subnets" {
  count                   = length(var.public_subnet_cidrs)
  vpc_id                  = aws_vpc.main_vpc.id
  cidr_block              = element(var.public_subnet_cidrs, count.index)
  availability_zone       = element(var.azs, count.index % length(var.azs))
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.name}-public-subnet-${count.index + 1}"
  }
}

# Create Private Subnets
resource "aws_subnet" "private_subnets" {
  count             = length(var.private_subnet_cidrs)
  vpc_id            = aws_vpc.main_vpc.id
  cidr_block        = element(var.private_subnet_cidrs, count.index)
  availability_zone = element(var.azs, count.index % length(var.azs))

  tags = {
    Name = "${var.name}-private-subnet-${count.index + 1}"
  }
}

# Create a Public Route Table
resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.main_vpc.id

  tags = {
    Name = "${var.name}-public-rt"
  }
}

# Associate Public Subnets with the Public Route Table
resource "aws_route_table_association" "public_association" {
  count          = length(aws_subnet.public_subnets)
  subnet_id      = aws_subnet.public_subnets[count.index].id
  route_table_id = aws_route_table.public_rt.id
}

# Add a default route to the Internet Gateway for the Public Route Table
resource "aws_route" "public_internet_access" {
  route_table_id         = aws_route_table.public_rt.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.igw.id
}

# Create a Private Route Table
resource "aws_route_table" "private_rt" {
  vpc_id = aws_vpc.main_vpc.id

  tags = {
    Name = "${var.name}-private-rt"
  }
}

# Associate Private Subnets with the Private Route Table
resource "aws_route_table_association" "private_association" {
  count          = length(aws_subnet.private_subnets)
  subnet_id      = aws_subnet.private_subnets[count.index].id
  route_table_id = aws_route_table.private_rt.id
}

# Public EC2 Security Group
resource "aws_security_group" "ec2_public_sg" {
  name        = "${var.name}-public-ec2-sg"
  description = "Allow SSH and HTTP/S traffic for public EC2"
  vpc_id      = aws_vpc.main_vpc.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.ssh_access_ip] # Restrict SSH to your IP
  }

  ingress {
    from_port   = 80
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Allow HTTP/S from anywhere
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.name}-public-ec2-sg"
  }
}

# Private RDS Security Group
resource "aws_security_group" "private_rds_sg" {
  name        = "${var.name}-private-rds-sg"
  description = "Allow private RDS access"
  vpc_id      = aws_vpc.main_vpc.id

  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = var.private_subnet_cidrs # Allow private subnets
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.name}-private-rds-sg"
  }
}

# EC2 Private Security Group
resource "aws_security_group" "private_ec2_sg" {
  name        = "${var.name}-private-ec2-sg"
  description = "Allow EC2 traffic within private subnets"
  vpc_id      = aws_vpc.main_vpc.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = var.private_subnet_cidrs # Allow SSH within private subnets
  }

  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = var.private_subnet_cidrs # Allow DB traffic within private subnets
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.name}-private-ec2-sg"
  }
}
