# Launch an EC2 instance
resource "aws_instance" "ec2_instance" {
  ami           = var.ami_id
  instance_type = var.instance_type
  subnet_id     = var.subnet_id
  vpc_security_group_ids = [aws_security_group.ec2_sg.id]
  key_name      = aws_key_pair.ec2_key_pair.key_name

  # User data script to connect to RDS
  user_data = <<-EOF
                #!/bin/bash
                yum update -y
                yum install -y mysql
                echo "Connecting to RDS: ${var.private_rds_endpoint}" >> /var/log/user_data.log
                mysql -h ${var.private_rds_endpoint} -u ${var.private_rds_username} -p${var.private_rds_password} -e "SHOW DATABASES;" >> /var/log/user_data.log 2>&1
              EOF

  tags = {
    Name = var.name
  }
}

# Attach an Elastic IP to the EC2 instance
resource "aws_eip" "ec2_eip" {
  instance = aws_instance.ec2_instance.id
}

# Generate a private key for the EC2 instance
resource "tls_private_key" "ec2_key" {
  algorithm = "RSA"
  rsa_bits  = 2048
}

# Create an AWS key pair using the generated private key
resource "aws_key_pair" "ec2_key_pair" {
  key_name   = "${var.name}-key-pair"
  public_key = tls_private_key.ec2_key.public_key_openssh
}

# Save the private key locally
resource "local_file" "private_key" {
  content  = tls_private_key.ec2_key.private_key_pem
  filename = "${path.module}/ec2_private_key.pem"
}

# Security Group for EC2
resource "aws_security_group" "ec2_sg" {
  name_prefix = "${var.name}-sg"
  description = "Allow SSH and HTTP access"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.ssh_access_ip] # Restrict SSH access to your IP
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Allow HTTP from anywhere
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.name}-security-group"
  }
}

# Allow EC2 to connect to RDS
resource "aws_security_group_rule" "allow_rds_access" {
  type                     = "ingress"
  from_port                = 3306
  to_port                  = 3306
  protocol                 = "tcp"
  security_group_id        = aws_security_group.ec2_sg.id
  source_security_group_id = var.rds_security_group_id
}
