output "emr_cluster_id" {
  value = aws_emr_cluster.emr_cluster.id
}

output "emr_master_dns" {
  value = aws_emr_cluster.emr_cluster.master_public_dns
}
