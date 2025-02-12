# Generate a random password for the RDS instance
resource "random_password" "rds_password" {
  length           = 16
  special          = true
  override_special = "_-#$%^&*()+=!" # Exclude invalid characters
}

# Save the RDS password to a local file
resource "local_file" "rds_password_file" {
  content  = random_password.rds_password.result
  filename = "${path.module}/${var.name}_rds_password.txt"
}

# Create an RDS instance
resource "aws_db_instance" "rds_instance" {
  allocated_storage      = var.allocated_storage
  max_allocated_storage  = var.max_allocated_storage
  engine                 = var.engine
  engine_version         = var.engine_version
  instance_class         = var.instance_class
  db_name                = var.db_name
  username               = var.username
  password               = random_password.rds_password.result
  publicly_accessible    = var.publicly_accessible
  vpc_security_group_ids = [var.security_group_id]
  db_subnet_group_name   = aws_db_subnet_group.rds_subnet_group.name
  skip_final_snapshot    = var.skip_final_snapshot

  tags = {
    Name        = var.name
    Environment = var.environment
  }
}

# Define the RDS subnet group
resource "aws_db_subnet_group" "rds_subnet_group" {
  name       = "${var.name}-subnet-group"
  subnet_ids = var.subnet_ids

  tags = {
    Name = "${var.name}-subnet-group"
  }
}
