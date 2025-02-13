resource "aws_emr_cluster" "emr_cluster" {
  name          = var.cluster_name
  release_label = var.release_label
  applications  = var.applications
  log_uri       = "s3://${var.s3_log_bucket}/emr-logs/"
  service_role  = aws_iam_role.emr_service_role.arn

  ec2_attributes {
    key_name                          = var.key_name
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
    Project     = "Ecommerce-ETL"
  }
}
