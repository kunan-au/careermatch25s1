output "security_group_id" {
  description = "ID of the security group associated with the EC2 instance"
  value       = aws_security_group.ec2_sg.id
}

output "instance_id" {
  description = "ID of the created EC2 instance"
  value       = aws_instance.ec2_instance.id
}

output "public_ip" {
  description = "Public IP of the created EC2 instance"
  value       = aws_instance.ec2_instance.public_ip
}
