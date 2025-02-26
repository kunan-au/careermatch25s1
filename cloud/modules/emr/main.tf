# Generate a short random suffix to append to your key name
resource "random_id" "emr_key_suffix" {
  byte_length = 2
}

# Generate a new RSA private key
resource "tls_private_key" "emr_key" {
  algorithm = "RSA"
  rsa_bits  = 2048
}

# Create an AWS Key Pair from the generated public key
resource "aws_key_pair" "emr_key" {
  # Use var.key_name as a prefix, and then append our random suffix
  key_name   = "${var.key_name}-${random_id.emr_key_suffix.hex}"
  public_key = tls_private_key.emr_key.public_key_openssh
}

# Save the private key locally as a PEM file
resource "local_file" "emr_key_file" {
  content         = tls_private_key.emr_key.private_key_pem
  filename        = "${path.module}/${var.key_name}-${random_id.emr_key_suffix.hex}.pem"
  file_permission = "0400"  # restrict permissions
}

resource "aws_emr_cluster" "emr_cluster" {
  name          = var.cluster_name
  release_label = var.release_label
  applications  = var.applications
  log_uri       = "s3://${var.s3_log_bucket}/emr-logs/"
  service_role  = aws_iam_role.emr_service_role.arn

  ec2_attributes {
    # Use the newly-created key pair
    key_name                          = aws_key_pair.emr_key.key_name
    subnet_id                         = var.subnet_id
    instance_profile                  = aws_iam_instance_profile.emr_instance_profile.arn
    emr_managed_master_security_group = var.security_group
    emr_managed_slave_security_group  = var.security_group
  }

  master_instance_group {
    instance_type  = var.master_instance_type
    instance_count = 1
  }

  core_instance_group {
    instance_type  = var.core_instance_type
    instance_count = var.core_instance_count
  }

  configurations_json = file("${path.module}/emr-config.json")

  bootstrap_action {
    path = "s3://${var.s3_bootstrap}/bootstrap.sh"
  }

  tags = {
    Environment = "Production"
    Project     = "CareerMatch-PPL2"
  }
}

output "emr_cluster_id" {
  value = aws_emr_cluster.emr_cluster.id
}

output "emr_master_dns" {
  value = aws_emr_cluster.emr_cluster.master_public_dns
}