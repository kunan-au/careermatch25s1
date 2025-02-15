# Provider Configuration
provider "aws" {
  region = var.aws_region
}

# **Ensure RDS is Created Before Running ETL**
data "aws_rds_cluster" "rds" {
  db_cluster_identifier = module.rds_private.name
}

# **Trigger AWS Glue Job**
resource "null_resource" "run_glue_etl" {
  provisioner "local-exec" {
    command = <<EOT
      aws glue start-job-run --job-name ${module.glue.glue_job_name}
    EOT
  }

  depends_on = [data.aws_rds_cluster.rds]
}
