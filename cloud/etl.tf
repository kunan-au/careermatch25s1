data "aws_db_instance" "rds" {
  db_instance_identifier = module.rds_private.rds_instance_identifier  # ✅ Correct reference
}

resource "null_resource" "run_glue_etl" {
  depends_on = [module.rds_private.rds_instance_identifier]  # ✅ Correctly references RDS instance
}

